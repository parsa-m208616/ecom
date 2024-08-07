from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import *
from .forms import SignUpForm

def category(request, name):
    name = name.replace('_', ' ')
    category = get_object_or_404(Category, name=name)
    products = Product.objects.filter(category=category)

    context = {
        'products': products,
        'category': category,
        'categories': Category.objects.all()
    }
    return render(request, 'category.html', context)

def index(request):
    products = Product.objects.all()

    context = {'products': products, 'categories': Category.objects.all()}
    return render(request, 'index.html', context)

def product(request, pk):
    product = get_object_or_404(Product, id=pk)

    return render(request, 'product.html', {"product": product, "categories": Category.objects.all()})

def about(request):

    return render(request, 'about.html', {'categories': Category.objects.all()})


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')

    return render(request, 'signup.html', {'form': form})

def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('index')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('index')
