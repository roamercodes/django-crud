from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, ProductForm, RegisterForm, CustomerForm
from .filters import OrderFilter
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import tolakhalaman_ini, ijinkan_pengguna, pilihan_login

# Create your views here.

@login_required(login_url='login')
# @ijinkan_pengguna(yang_diizinkan=['admin'])
@pilihan_login
def home(request):
    list_custumer = Customer.objects.all()
    # list_order = Order.objects.all()
    list_order = Order.objects.order_by('-id')
    total_orders = list_order.count()
    delivered = list_order.filter(status = 'Delivered').count()
    pending = list_order.filter(status = 'Pending').count()

    context = {
        'judul': 'Halaman Beranda',
        'menu': 'home',
        'customer':list_custumer,
        'order':list_order,
        'data_total_orders': total_orders,
        'data_delivered' : delivered,
        'data_pending' : pending,
    }
    
    return render(request, 'data/dashboard.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def product(request):
    list_product = Product.objects.order_by('-id')
    context = {
        'judul': 'Halaman Product',
        'menu': 'products',
        'product': list_product,

    }
    return render(request, 'data/product.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin']) 
def customer(request, pk):
    detailcustomer = Customer.objects.get(id=pk)
    order_customer = detailcustomer.order_set.all()
    total_order_customer = order_customer.count()
    filter_order = OrderFilter(request.GET, queryset=order_customer)
    # order_custumer=filter_order.qs
    order_customer=filter_order.qs

    halaman_tampil = Paginator(order_customer, 2)
    halaman_url = request.GET.get('halaman',1)
    halaman_order = halaman_tampil.get_page(halaman_url)

    if halaman_order.has_previous():
        url_previous = f'?halaman={halaman_order.previous_page_number()}'
    else:
        url_previous = ''
    if halaman_order.has_next():
        url_next = f'?halaman={halaman_order.next_page_number()}'
    else:
        url_next = ''

    context={ 
        'judul' : 'Halaman customer',
        'menu' : 'customer',
        'customer' : detailcustomer,
        'data_order_customer':order_customer,
        'halaman_order_custumer':halaman_order,
        'data_total_customer': total_order_customer,
        'filter_data_order': filter_order,
        'previous' : url_previous,
        'next' : url_next
    }
    return render(request, 'data/customer.html', context)

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['admin'])
def createOrder(request):
    formorder = OrderForm()
    if request.method == 'POST':
        # print('Cetak POST: ', request.POST)
        formsimpan = OrderForm(request.POST)
        if formsimpan.is_valid:
            formsimpan.save()
            return redirect('/')
    context = {
        'judul': 'Form Order',
        'form': formorder
    }
    return render(request, 'data/order_form.html', context)

@ijinkan_pengguna(yang_diizinkan=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    formorder = OrderForm(instance=order)
    if request.method == 'POST':
        formedit = OrderForm(request.POST, instance=order)
        if formedit.is_valid:
            formedit.save()
            return redirect('/')
    context = {
        'judul': 'Edit Order',
        'form': formorder
    }
    return render(request, 'data/order_form.html', context)

@ijinkan_pengguna(yang_diizinkan=['admin'])
def deleteOrder(request, pk):
    orderhapus = Order.objects.get(id=pk)
    if request.method == 'POST':
        orderhapus.delete()
        return redirect('/')
    context = {
        'judul': 'Hapus Data Order',
        'dataorderdelete': orderhapus
    }
    return render(request, 'data/delete_form.html', context)

def createProduct(request):
    forProduct = ProductForm()
    if request.method == 'POST':
    #    print('Cetak POST:', request.POST)
         formsimpan = ProductForm(request.POST)
         if formsimpan.is_valid:
            formsimpan.save()
            return redirect('product')
    context = {
        'judul': 'Form Product',
        'form' : forProduct,
    }
    return render(request, 'data/product_form.html', context)

def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    forproduct = ProductForm(instance=product)
    if request.method=='POST':
        formEdit = ProductForm(request.POST, instance=product)
        if formEdit.is_valid:
            formEdit.save()
            return redirect('product')
    context = {
        'judul': 'Edit Product',
        'form': forproduct,
    }
    return render(request, 'data/Product_form.html', context)

def deleteProduct(request, pk):
    deleteProduct = Product.objects.get(id=pk)
    if request.method == 'POST':
        deleteProduct.delete()
        return redirect('product')
        
    context = {
        'judul': 'Hapus Data Produk',
        'dataproductdelete' : deleteProduct,     
    }
    return render(request, 'data/delete_product.html', context)

@tolakhalaman_ini
def loginPage (request):
    formlogin = AuthenticationForm
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        cocokan = authenticate(request, username=username, password=password )
        if cocokan is not None:
            login(request, cocokan)
            return redirect('home')
    context = {
            'judul': 'Halaman Login',
            'menu': 'login',
            'tampillogin' : formlogin
    }
    return render(request, 'data/login.html', context)

@tolakhalaman_ini
def registerPage (request):
    formregister = RegisterForm()
    if request.method == 'POST':
        formregister = RegisterForm(request.POST)
        if formregister.is_valid():
            nilaiusername = formregister.cleaned_data.get('username')
            messages.success(request, f'Username Anda adalah {nilaiusername}')
            group_custumer = formregister.save()
            grup = Group.objects.get(name='custumer')
            group_custumer.groups.add(grup)
            Customer.objects.create(
                user=group_custumer,
                name=group_custumer.username)
            return redirect('login')
    context = {
        'judul': 'Halaman Register',
        'menu': 'register',
        'tampilregister' : formregister
    }
    return render(request, 'data/register.html', context)

def logoutPage(request):
 logout(request)
 return redirect('login')

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['custumer'])
def userPage(request):
    order_customer = request.user.customer.order_set.all()
    total_orders = order_customer.count()
    delivered = order_customer.filter(status='Delivered').count()
    pending = order_customer.filter(status='Pending').count()

    context = {
        'data_order_customer': order_customer,
        'data_total_orders': total_orders,
        'data_delivered': delivered,
        'data_pending': pending,
    }
    return render(request, 'data/user.html', context)

def pilihan_login(fungsi_awal):
    def perubahan_halaman(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'custumer' :
                return redirect()
        if group == 'admin' :
            return fungsi_awal(request, *args, **kwargs)
            
    return perubahan_halaman

@login_required(login_url='login')
@ijinkan_pengguna(yang_diizinkan=['custumer'])
def accountSetting(request):
    datacustomer = request.user.customer
    form = CustomerForm(instance = datacustomer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=datacustomer)
        if form.is_valid:
            form.save() 
    context = {
        'menu': 'settings',
        'formcustomer': form
    }
    return render(request, 'data/account_setting.html', context)