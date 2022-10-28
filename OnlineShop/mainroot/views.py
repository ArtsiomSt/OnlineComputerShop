from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, F, Q, Max, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views import View
from .forms import UserSingUp, UserSignIn, UserOrderForm, FilterForm
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AdminUserMixin


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
    label = 'Add To Packet'
    current_product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        if request.user in current_product.ordered_by.all():
            label = 'Delete from packet'
    model = get_model_by_cat(current_product.category.title)
    cur_object = model.objects.get(pk=product_id)
    context = {
        "fields": cur_object.get_field_for_page(),
        "object": cur_object,
        "label_for_but": label,
    }
    return render(request, 'mainroot/detailview.html', context)


class Products_by_cat(View):
    def get(self, request, cat_name):
        list_of_products = Product.objects.filter(category__title=cat_name)
        form = FilterForm()
        context = {
            'title': Category.objects.get(title=cat_name).title,
            'products': list_of_products,
            'form': form,
        }
        return render(request, 'mainroot/products_by_cat.html', context)

    def post(self, request, cat_name):
        model = get_model_by_cat(cat_name)
        form = FilterForm(request.POST)
        if form.is_valid():
            empty_keys = []
            for key, value in form.cleaned_data.items():
                if value is None:
                    empty_keys.append(key)
            for item in empty_keys:
                form.cleaned_data.pop(item)
            manufact_form = form.cleaned_data.get('manufactor')
            if manufact_form is not None:
                form.cleaned_data['manufactor'] = [manufact_form.pk]
            all_manufs = list(map(lambda x: x['id'], Manufact.objects.values('id')))
            max_price_in_prod_q = model.objects.values('price')
            max_price_in_prod = 0
            for item in max_price_in_prod_q:
                cur = int(item.get('price'))
                if cur > max_price_in_prod:
                    max_price_in_prod = cur
            print(max_price_in_prod)
            print(form.cleaned_data)
            list_of_products = model.objects.filter(Q(title__contains=form.cleaned_data.get('title', '')) & Q(
                manuf_id__in=form.cleaned_data.get('manufactor', all_manufs)) & Q(
                price__gt=form.cleaned_data.get('min_price', 0)) & Q(
                price__lt=form.cleaned_data.get('max_price', max_price_in_prod)))
        context = {
            'title': Category.objects.get(title=cat_name).title,
            'products': list_of_products,
            'form': form,
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
        'form': form,
    }
    return render(request, 'mainroot/registration.html', context)


def sign_in_user(request):
    if request.method == "POST":
        form = UserSignIn(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            try:
                login(request, user)
                return redirect('home')
            except:
                return redirect('signin')
    else:
        form = UserSignIn()
    context = {
        'form': form
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
    cur_product.add_remove_user_to_pocket(cur_user)
    return redirect(cur_product)


class Users_products(View):
    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('signin')
        cur_user = self.request.user
        user_products = cur_user.product_set.select_related('category').all()
        user_spents = count_spents(user_products)
        context = {
            'products': user_products,
            'title': 'Packet',
            'user_spents': user_spents,
        }
        return render(self.request, 'mainroot/users_packet.html', context)


class Ordering_view(View):
    context = {
        'title': 'Ordering Process'
    }

    def get(self, request):
        form = UserOrderForm()
        self.context['form'] = form
        return render(self.request, 'mainroot/ordering.html', self.context)

    def post(self, request):
        form = UserOrderForm(self.request.POST)
        if form.is_valid():
            order = Users_order.objects.create(**form.cleaned_data, user=self.request.user,
                                               full_price=count_spents(self.request.user.product_set.all()))
            for item in self.request.user.product_set.all():
                order.users_products.add(item)
            order.save()
            return redirect('home')


class AdminPanel(AdminUserMixin, View):
    def get(self, request):
        products = Product.objects.all().annotate(users_amount=Count('ordered_by')).filter(users_amount__gt=0)
        sum_price_of_orders = 0
        for item in products:
            sum_price_of_orders += item.users_amount * int(item.price)
        users = User.objects.all().prefetch_related()
        user_and_spents = {}
        for item in users:
            users_sum = 0
            for prod in item.product_set.all():
                users_sum += int(prod.price)
            user_and_spents[item.username] = users_sum
        context = {
            'ordered_products': products,
            'title': 'AdminPanel',
            'sum_price': sum_price_of_orders,
            'user_spent': user_and_spents,
        }
        return render(request, 'mainroot/adminpanel.html', context)


def count_spents(query_set):
    users_packet_price = 0
    for item in query_set:
        users_packet_price += int(item.price)
    return users_packet_price


def get_model_by_cat(cat):
    models_dict = {
        'Videocard': Videocard,
        'Processor': Proccessor,
        'Memory': Memory,
        'PC': Computer,
    }
    return models_dict.get(cat, Product)


def random_videocard():
    for_title = ['RTX', 'GTX', 'GT']
    for_title1 = ['20', '30', '40', '10']
    for_title3 = ['30', '50', '70', '50 TI', '70', '90', '80', '80 TI']
    category = Category.objects.get(title='Videocard')
    manuf = Manufact.objects.all()
    memory_type = ['GDDR6', 'GDDR5', 'GDDR4']
    provs = Provider.objects.all()
    for item in range(20):
        title = for_title[random.randrange(0, len(for_title))] + ' ' + for_title1[
            random.randrange(0, len(for_title1))] + for_title3[random.randrange(0, len(for_title3))]
        Videocard.objects.create(title=title, category=category, price=random.randrange(0, 300),
                                 remain_in_stock=random.randrange(0, 200), amount_ordered=0,
                                 weight=random.randrange(0, 2000), provider=provs[random.randrange(0, len(provs))],
                                 manuf=manuf[random.randrange(0, len(manuf))], freq=random.randrange(3000, 9000),
                                 v_memory=random.randrange(5, 10),
                                 memory_type=memory_type[random.randrange(0, len(memory_type))])
