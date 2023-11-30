from django.shortcuts import redirect, render,HttpResponse
from app.models import Category, Order,Product,ContactPage,Brand
from django.contrib.auth import authenticate,login,logout
from app.forms import LoginForm, UsercreateForm
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def Master(request):
    return render(request,'master.html')

def Index(request):
    category=Category.objects.all()
    categoryID=request.GET.get('category')
    brand=Brand.objects.all()
    brandID=request.GET.get('brand')  
      
    if categoryID:
        product=Product.objects.filter(sub_category=categoryID).order_by('-id')
        
    elif brandID:
        product=Product.objects.filter(brand=brandID).order_by('-id')
        
    else:
        product=Product.objects.all()

    context={
        'category':category,
        'product':product,
        'brand':brand
    }
    return render(request,'index.html',context)

def signupPage(request):
    if request.method == "POST":
        form = UsercreateForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations !! ✔✔👍')
            form.save()
        else:
            messages.error(request,"InValid Password or Username or This username has been taken.")
    else:
        form = UsercreateForm()
    return render(request,'registration/signup.html',{'form':form})

def loginPage(request):
    
        if request.method =='POST':
            form = LoginForm(request=request,data= request.POST)
            if form.is_valid:
                uname = request.POST.get('username')
                upass = request.POST.get('password')
                user = auth.authenticate(request,username = uname,password = upass)
                if user != None:
                    auth.login(request,user)
                    messages.success(request,'You have successfully logged in 😁😁👍')
                    return redirect('index')
                else:
                    messages.error(request,'Username or password invalid')
                    return redirect('loginPage')
        else:
            form = LoginForm()
        return render(request,'registration/login.html',{'form':form})
    

def logoutPage(request):
    logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('loginPage')
   

#add to cart
@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

#Contact Page
def ContactP(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
        contact=ContactPage(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()
    return render(request,'registration/contact.html')

#Checkout
def CheckOut(request):
    if request.method=='POST':
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        pincode=request.POST.get('pincode')
        cart=request.session.get('cart')
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(pk=uid)
        print(cart)
        
        for i in cart:
            a=(int(cart[i]['price']))
            b=cart[i]['quantity']
            total=a*b
            order=Order(
                user=user,
                product=cart[i]['name'],
                price=cart[i]['price'],
                quantity=cart[i]['quantity'],
                image=cart[i]['image'],
                address=address,
                phone=phone,
                pincode=pincode,
                total=total,
            )
            order.save()
        request.session['cart']={}
        return redirect('index')
    return HttpResponse('this is checkout page')

def Your_Order(request):
    uid=request.session.get('_auth_user_id')
    user=User.objects.get(pk=uid)
    
    order=Order.objects.filter(user=user)
    context={
        'order':order
    }
    return render(request,'order.html',context)

def Product_page(request):
    category=Category.objects.all()
    brand=Brand.objects.all()
    brandID=request.GET.get('brand')
    categoryID=request.GET.get('category')  
      
    if categoryID:
        product=Product.objects.filter(sub_category=categoryID).order_by('-id')
        
    elif brandID:
        product=Product.objects.filter(brand=brandID).order_by('-id')
        
    else:
        product=Product.objects.all()

    
    context={
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(request,'product.html',context)


def Product_Detail(request,id):
    product=Product.objects.filter(id=id).first()
    
    category=Category.objects.all()
    context={
        'category':category,
        'product':product,
        
    }
    
    context={
        'product':product
    }
    return render(request,'product_detail.html',context)

def Search(request):
    # query=request.GET['query']
    product=Product.objects.filter()
    context={
        'product':product
    }
    return render(request,'search.html',context)

def Ops(request):
    return render(request,'404.html')