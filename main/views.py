from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile


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


# skin Analysis
@login_required
def analyze(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            analysis_data = analyze_image(request.FILES['image'])
            SkinAnalysis.objects.create(
                user=request.user,
                image=request.FILES['image'],
                skin_type=analysis_data['skin_type'],
                skincare_advice=analysis_data['skincare'],
                makeup_advice=analysis_data['makeup']
            )
            return redirect('dashboard')
    else:
        form = ImageUploadForm()
    return render(request, 'analyze.html', {'form': form})


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

            products = Product.objects.filter(
                skin_type=analysis.skin_type
            )

            return render(request, "analyze", {
                "analysis": analysis,
                "products": products
            })

    return render(request, "analyze.html")
