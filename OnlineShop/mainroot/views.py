from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import UserSingUp, UserSignIn

def homepage(request):
    message = ''
    if 'message' in request.GET.keys():
        message = request.GET['message']
    cats = Category.objects.annotate(num_of_prod=Count('product'))
    cats_for_template = []
    for item in cats:
        if item.num_of_prod:
            cats_for_template.append(item)
    context = {
        "message": message,
        "products": Product.objects.filter(remain_in_stock__gt=0),
        'categories': cats_for_template,
    }
    return render(request, 'mainroot/index.html', context)


def detailpage(request, product_id):
    allowed_fields = {
        'title': 'Title',
        'freq': 'Frequency',
        'socket':'Socket',
        'c_memory':'Cash memory',
        'weight':'Weight',
        'memory_type':'Memory type',
        'remain_stock':'In stock',
        'v_memory':'Video memory'
    }
    label = 'Add To Packet'
    current_product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        if request.user in current_product.ordered_by.all():
            label = 'Delete from packet'
    if current_product.category.id == 1:
        object = Videocard.objects.get(pk=product_id)
    elif current_product.category.id == 2:
        object = Proccessor.objects.get(pk=product_id)
    elif current_product.category.id == 4:
        object = Computer.objects.get(pk=product_id)
    elif current_product.category.id == 3:
        object = Memory.objects.get(pk=product_id)
    else:
        object = current_product
    fields_for_iter = object.__dict__
    fields_for_stats = {}
    for key, value in fields_for_iter.items():
        if key not in allowed_fields.keys():
            continue
        else:
            fields_for_stats[allowed_fields[key]] = fields_for_iter[key]

    context = {
        "fields": fields_for_stats,
        "object": object,
        "label_for_but": label,
    }
    return render(request, 'mainroot/detailview.html', context)


def get_products_by_cat(request, cat_name):
    list_of_products = Product.objects.filter(category__title=cat_name)
    context = {
        'title': Category.objects.get(title=cat_name).title,
        'products': list_of_products,
    }
    return render(request, 'mainroot/products_by_cat.html', context)


def sing_up_user(request):
    if request.method == "POST":
        form = UserSingUp(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/?message=Registrated successfully")
    else:
        form = UserSingUp()
    context = {
        'form':form,
    }
    return render(request, 'mainroot/registration.html', context)


def sign_in_user(request):
    if request.method == "POST":
        form = UserSignIn(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password=password)
            try:
                login(request, user)
                return redirect('home')
            except:
                return redirect('signin')
    else:
        form = UserSignIn()
    context = {
        'form':form
    }
    return render(request, 'mainroot/signin.html', context)


def signout(request):
    logout(request)
    return redirect('home')


def product_to_pocket(request, product_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    cur_user = request.user
    cur_product = get_object_or_404(Product, pk=product_id)
    if not cur_product.remain_in_stock >0:
        return redirect('home')
    if cur_user not in cur_product.ordered_by.all():
        cur_product.ordered_by.add(cur_user)
        cur_product.remain_in_stock = F('remain_in_stock')-1
        cur_product.save()
    else:
        cur_product.ordered_by.remove(cur_user)
        cur_product.remain_in_stock = F('remain_in_stock')+1
        cur_product.save()
    print(cur_product.ordered_by.all())
    return redirect(cur_product)


def users_packet(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    cur_user = request.user
    user_products = cur_user.product_set.all()
    print(user_products)
    context = {
        'products':user_products,
        'title':'Packet',
    }
    return render(request, 'mainroot/users_packet.html', context)

