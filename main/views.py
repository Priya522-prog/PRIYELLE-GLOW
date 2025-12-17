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
                image=image
            )

            result = analyze_image(analysis.image.path)

            analysis.skin_type = result["skin_type"]
            analysis.concerns = result["concerns"]
            analysis.save()

            # ---------- FEEDBACK GENERATION (ADDED) ----------
            skin_type = result.get("skin_type")
            concerns = result.get("concerns", [])

            if not skin_type:
                messages.error(
                    request,
                    "Face not clearly detected. Please ensure good lighting and face the camera."
                )
            else:
                # Build readable concerns text
                if concerns:
                    concerns_text = ", ".join(concerns)
                else:
                    concerns_text = "no major skin issues"

                # Recommendation summary (simple & extendable)
                recommendations = {
                    "Oily": "Use oil-free cleansers and lightweight moisturizers.",
                    "Dry": "Use gentle cleansers and rich hydrating moisturizers.",
                    "Combination": "Use balanced skincare and target oily and dry areas separately."
                }

                recommendation = recommendations.get(
                    skin_type,
                    "Maintain a consistent skincare routine."
                )

                messages.success(
                    request,
                    f"Your skin appears to be {skin_type.lower()} with {concerns_text}. {recommendation}"
                )
            # ========== END FEEDBACK SYSTEM ==========

            products = Product.objects.filter(
                skin_type=analysis.skin_type
            )           

            return render(request, "analyze.html", {
                "analysis": analysis,
                "products": products
            })

    return render(request, "analyze.html")   

