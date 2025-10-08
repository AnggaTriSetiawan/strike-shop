from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all") 
    
    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'app_name' : 'Strike Shop',
        'name': 'Angga Tri Setiawan',
        'class': 'PBP F',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form,
        "product": product
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, description_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price' : product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'product_views': product.views,
            'stock' : product.stock,
            'brand' : product.brand,
            'views' : product.views,
            'rating' : product.rating,
            'user_id': product.user_id,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
    try:
        product_list = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_list)
        return HttpResponse(xml_data, description_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price' : product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'product_views': product.views,
            'stock' : product.stock,
            'rating' : product.rating,
            'brand' : product.brand,
            'views' : product.views,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = strip_tags(request.POST.get("name")) 
    description = strip_tags(request.POST.get("description")) 
    price = request.POST.get("price")
    thumbnail = request.POST.get("thumbnail")
    category = request.POST.get("category")
    is_featured = request.POST.get("is_featured") == 'on'  
    stock = request.POST.get("stock")
    brand = request.POST.get("brand")
    user = request.user

    new_product = Product(
        name=name, 
        price=price,
        description=description,
        thumbnail=thumbnail,
        category=category,
        is_featured=is_featured,
        stock=stock,
        brand=brand,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

def ajax_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                "success": True,
                "message": "Login successful!"
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "Invalid username or password."
            }, status=400)

    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    }, status=405)

def ajax_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username or not password1 or not password2:
            return JsonResponse({
                "success": False,
                "message": "All fields are required."
            }, status=400)

        if password1 != password2:
            return JsonResponse({
                "success": False,
                "message": "Passwords do not match."
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "success": False,
                "message": "Username already exists."
            }, status=400)

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        return JsonResponse({
            "success": True,
            "message": "Account created successfully!"
        })

    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    }, status=405)

def ajax_edit_product(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "message": "Product updated successfully!"
            })
        else:
            return JsonResponse({
                "success": False,
                "message": "Please fix the errors below.",
                "errors": form.errors
            }, status=400)

    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    }, status=405)

@login_required
def ajax_delete_product(request, id):
    if request.method == "DELETE":
        try:
            product = Product.objects.get(pk=id, user=request.user)
            product.delete()
            return JsonResponse({"success": True, "message": "Product deleted successfully!"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found."}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

def ajax_logout(request):
    logout(request)
    return JsonResponse({
        "success": True,
        "message": "Logged out successfully!"
    })

@csrf_exempt
def increment_views_ajax(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product.increment_views()  
        product.refresh_from_db() 
        return JsonResponse({"success": True, "views": product.views})
    except Product.DoesNotExist:
        return JsonResponse({"success": False, "message": "Product not found"}, status=404)

