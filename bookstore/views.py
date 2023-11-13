from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from regex import F
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from django.conf import settings
import requests

# Create your views here.

@login_required(login_url='login')
@for_admins
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = Order.objects.all().count()
    pending_orders = Order.objects.all().filter(status='Pending').count()
    delivered_orders = Order.objects.all().filter(status='Delivered').count()
    in_progress_orders = Order.objects.all().filter(status='In Progress').count()
    out_of_orders = Order.objects.all().filter(status='Out of order').count()

    context = {'customers' : customers,'orders' : orders , 'total_orders' : total_orders,
               'pending_orders' : pending_orders, 'delivered_orders' : delivered_orders,
               'in_progress_orders' : in_progress_orders,'out_of_orders' : out_of_orders}
   
    return render(request,'bookstore/index.html', context)


@login_required(login_url='login')
@for_admins
def books(request):
    books = Book.objects.all()
    total_books = books.count()
    return render(request,'bookstore/books.html',{'books' : books, 'total_books' : total_books})


def about(request):
    return HttpResponse('about page')


@login_required(login_url='login')
@for_admins
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    print(customer)
    customer_orders = customer.order_set.all()
    print(customer_orders)

    orders_number = customer_orders.count()
    pending_orders = customer_orders.filter(status='Pending').count()
    delivered_orders = customer_orders.filter(status='Delivered').count()
    in_progress_orders = customer_orders.filter(status='In Progress').count()
    out_of_orders = customer_orders.filter(status='Out of order').count()
    
    # order_filter = OrderFilter(request.GET, queryset= customer_orders)
    # customer_orders = order_filter.qs
    search_query = request.GET.get('query','')
    # Use filters to search for books with titles or authors matching the query
    order_filter = customer_orders.filter(
            models.Q(book__name__icontains=search_query) |
            models.Q(book__category__icontains=search_query)|
            models.Q(creation_date__icontains=search_query) | 
            models.Q(status__icontains=search_query)
        )
    customer_orders = order_filter
    context = {'customer' : customer, 'customer_orders' : customer_orders,
               'orders_number': orders_number,'pending_orders' : pending_orders,
               'delivered_orders': delivered_orders, 'in_progress_orders' : in_progress_orders,
               'out_of_orders': out_of_orders, 'order_filter' : order_filter}
    
    return render(request,'bookstore/customer.html', context)


def contact(request):
    return render(request,'bookstore/tail.html')


@login_required(login_url='login')
@for_admins
def create_order(request):
    
    if request.method == 'POST':
        # print(request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = OrderForm()
    context= {'form': form}
    return render(request, 'bookstore/order_form.html', context)

@login_required(login_url='login')
@for_admins
def multi_create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('book','status'), extra=5)
    customer = Customer.objects.get(id= pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance= customer)

    if request.method == 'POST':
        # print(request.POST)
        formset = OrderFormSet(request.POST, instance= customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
            
    context= {'formset': formset}
    return render(request, 'bookstore/order_form.html', context)

@login_required(login_url='login')
@for_admins
def update_order(request, pk):
    order= Order.objects.get(id= pk)
    form = OrderForm(instance= order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance= order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}

    return render(request, 'bookstore/order_form.html', context)

#this code doesn't use the delete_form template if you want to it you need to change logic of this view
@login_required(login_url='login')
@for_admins
def delete_order(request, pk):
    order = Order.objects.get(id= pk)
    order.delete()
    return redirect('/')

@login_required(login_url='login')
@for_admins
def create_customer(request):
    
    if request.method == 'POST':
        form= RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form= RegisterForm()
    context= {'form': form}
    return render(request,'bookstore/customer_form.html',context)

@login_required(login_url='login')
@for_admins
def update_customer(request, pk):
    customer= Customer.objects.get(id=pk)
    user= customer.user
    
    if request.method == 'POST':
        user_form= UserForm(request.POST, instance=user)
        customer_form= CustomerForm(request.POST, request.FILES, instance=customer)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            my_form= customer_form.save(commit=False)
            my_form.user=user
            my_form.save()
            return redirect('/')

    customer_form= CustomerForm(instance=customer)
    user_form= UserForm(instance=user)
    context= {'customer_form':customer_form, 'user_form':user_form,}
    return render(request, 'bookstore/customer_form.html', context)

#this code doesn't use the delete_form template if you want to it you need to change logic of this view
@login_required(login_url='login')
@for_admins
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()
    return redirect('/')



@is_logged
def register(request):
    
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            g_recaptcha_response = request.POST.get('g-recaptcha-response')
            data = { 'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                     'response': g_recaptcha_response }
            g_result = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data) 
            result = g_result.json()
            if result['success']:
                form.save()
                username= form.cleaned_data.get('username') 
                messages.success(request, username + ' Created Successfully !')
                return redirect('login')   
            
    form = RegisterForm()
    context= {'form' : form}
    return render(request, 'bookstore/register.html', context)

@is_logged
def user_login(request):

    context = {}
    
    if request.method == 'POST':   
        logins= request.POST.get('login')
        password= request.POST.get('password')
        user = authenticate(request,username= logins.strip(), password= password)

        if user is not None:
            context = {'user' : user}
            login(request,user)
            return redirect('/')
        else: 
            messages.info(request,' username or password is incorrect')
    return render(request, 'bookstore/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(['customer'])
def user_profile(request):
    customer_orders = request.user.customer.order_set.all()
    print(customer_orders)
    total_orders = customer_orders.count()
    print(total_orders)
    pending_orders = customer_orders.filter(status='Pending').count()
    delivered_orders = customer_orders.filter(status='Delivered').count()
    in_progress_orders = customer_orders.filter(status='In Progress').count()
    out_of_orders = customer_orders.filter(status='Out of order').count()

    context = {'customer_orders': customer_orders , 'total_orders' : total_orders,
               'pending_orders' : pending_orders, 'delivered_orders' : delivered_orders,
               'in_progress_orders' : in_progress_orders,'out_of_orders' : out_of_orders}

    return render(request, 'bookstore/profile.html', context)


@login_required(login_url='login')
@allowed_users(['customer'])
def profile_info(request):

    customer= request.user.customer
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            User.objects.all().filter(username=request.user.username).update(first_name=request.POST['first_name']
                          ,last_name=request.POST['last_name'], username=request.POST['username'], email=request.POST['email'])
            form.save()
            return redirect('profile_info')

    form = CustomerForm(instance=customer)
    context = {'form':form}

    return render(request, 'bookstore/profile_info.html', context)
