from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile

from django.contrib import messages

from .models import Product, SkinAnalysis
from .forms import ProductForm, ImageUploadForm
from .utils import analyze_image
from .mpesa import stk_push

# Authentication
def register(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')


@login_required
def dashboard(request):
    # If dashboard form posts an image, handle it (supports dashboard camera flow)
    if request.method == 'POST':
        image_data = request.POST.get('captured_image')
        if not image_data:
            messages.error(request, 'No image submitted. Please capture an image and try again.')
            analyses = SkinAnalysis.objects.filter(user=request.user)
            return render(request, 'dashboard.html', {'analyses': analyses})

        try:
            format, imgstr = image_data.split(';base64,')
            image = ContentFile(base64.b64decode(imgstr), name='analysis.png')

            analysis = SkinAnalysis.objects.create(
                user=request.user,
                image=image,
                skin_type='normal',
                concerns=''
            )

            result = analyze_image(analysis.image.path)

            analysis.skin_type = result.get('skin_type', 'normal')
            analysis.concerns = result.get('concerns', '')
            analysis.skincare_recommendation = ', '.join(result.get('skincare', []))
            analysis.makeup_recommendation = ', '.join(result.get('makeup', []))
            analysis.save()

            skin_type = result.get('skin_type', 'normal')
            concerns = result.get('concerns', '')

            messages.success(request, f"Your skin appears to be {skin_type}.")

            return redirect('analysis_results', analysis_id=analysis.id)
        except Exception as e:
            messages.error(request, 'Failed to process the image. Please try again with better lighting.')
            analyses = SkinAnalysis.objects.filter(user=request.user)
            return render(request, 'dashboard.html', {'analyses': analyses})

    analyses = SkinAnalysis.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'analyses': analyses})





# Product(STAFF ONLY)

@user_passes_test(lambda u: u.is_staff)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


@user_passes_test(lambda u: u.is_staff)
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'product_form.html', {'form': form})


# MPESA payment
@login_required
def mpesa_pay(request):
    if request.method == "POST":
        stk_push(request.POST['phone'], 500)
        return render(request, 'mpesa_wait.html')
    return render(request, 'mpesa_pay.html')


def home(request):
    return render(request, 'home.html')


@login_required
def analyze(request):
    if request.method == "POST":
        image_data = request.POST.get("captured_image")

        if image_data:
            format, imgstr = image_data.split(';base64,')
            image = ContentFile(
                base64.b64decode(imgstr),
                name="analysis.png"
            )

            analysis = SkinAnalysis.objects.create(
                user=request.user,
                image=image,
                skin_type='normal',
                concerns=''
            )

            result = analyze_image(analysis.image.path)

            analysis.skin_type = result["skin_type"]
            analysis.concerns = result.get("concerns", "")
            analysis.skincare_recommendation = ", ".join(result.get("skincare", []))
            analysis.makeup_recommendation = ", ".join(result.get("makeup", []))
            analysis.save()

            # Show success message with feedback
            skin_type = result.get("skin_type", "normal")
            concerns = result.get("concerns", "")

            if not skin_type:
                messages.error(
                    request,
                    "Face not clearly detected. Please ensure good lighting and face the camera."
                )
                return render(request, "analyze.html")
            else:
                # Build readable concerns text
                if concerns:
                    concerns_text = concerns if isinstance(concerns, str) else ", ".join(concerns)
                else:
                    concerns_text = "no major skin issues"

                # Recommendation summary
                recommendations = {
                    "oily": "Use oil-free cleansers and lightweight moisturizers.",
                    "dry": "Use gentle cleansers and rich hydrating moisturizers.",
                    "combination": "Use balanced skincare and target oily and dry areas separately.",
                    "normal": "Maintain a consistent skincare routine.",
                    "sensitive": "Use hypoallergenic and gentle skincare products."
                }

                recommendation = recommendations.get(
                    skin_type,
                    "Maintain a consistent skincare routine."
                )

                messages.success(
                    request,
                    f"Your skin appears to be {skin_type.title()} with {concerns_text}. {recommendation}"
                )

            # Redirect to results page
            return redirect('analysis_results', analysis_id=analysis.id)

    return render(request, "analyze.html")   

@login_required
def analysis_results(request, analysis_id):
    analysis = get_object_or_404(SkinAnalysis, id=analysis_id, user=request.user)

    # Filter products by skin type and category
    skincare_products = Product.objects.filter(
        skin_type=analysis.skin_type,
        category='skincare'
    ).order_by('country')
    
    makeup_products = Product.objects.filter(
        skin_type=analysis.skin_type,
        category='makeup'
    ).order_by('country')

    feedback_message = (
        f"Your skin appears to be {analysis.skin_type}. "
        f"Detected concerns: {analysis.concerns}. "
        f"Follow the recommended products below."
    )

    return render(request, 'analysis_result.html', {
        'analysis': analysis,
        'skincare_products': skincare_products,
        'makeup_products': makeup_products,
        'feedback_message': feedback_message
    })


