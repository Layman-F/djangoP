from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


def home(request):
	if not request.user.is_authenticated:
		return redirect('login')
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	Pending = orders.filter(status='pending').count()
	context = {'orders':orders,'customers':customers,'total_customers':total_customers,
	'total_orders':total_orders,'delivered':delivered,'Pending':Pending}
	return render(request,'accounts/dashboard.html',context)


def products(request):
	products = Product.objects.all()
	return render(request,'accounts/products.html',{'products':products})


def customer(request,pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	order_count = orders.count()
	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs 
	context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
	return render(request,'accounts/customer.html',context)

def createOrder(request):
	form = OrderForm
	if request.method =='POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')

	context = {'form':form}
	return render(request,'accounts/order_form.html',context)



def updateOrder(request,pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method =='POST':
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	context = {'form':form}
	return render(request,'accounts/order_form.html',context)



def deleteOrder(request,pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return HttpResponseRedirect('/')
	context = {'item':order}
	return render(request,'accounts/delete.html',context)

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method=='POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')
				messages.success(request,'Account was created for '+username)
				return redirect('login')
		context ={'form':form}
		return render(request,'accounts/register.html',context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method =='POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request,username=username,password=password)
			if user is not None:
				login(request,user)
				return redirect('home')
			else:
				messages.info(request,'username OR password is incorrect')
		context = {}
		return render(request,'accounts/login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('login')