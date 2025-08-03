from django.shortcuts import get_object_or_404, render,redirect, HttpResponse


from .models  import Profile,User
def login_view(request):
    if(request.method=='POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')

        # try:
        #     user=User.objects.get(username=username)
        # except User.DoesNotExist:
        #     messages.error(request,'invalid username or email')

        #     return render(request,'login.html')
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f"Welcome back, {user.username}!")
            return redirect('about')
        else:
            messages.error(request,"Incorrect password")
    return render(request,'login.html')
from django.contrib.auth.decorators import login_required
        


# def about(request):
#     profiles=Profile.objects.all()
#     return render(request,'about.html',{'profiles':profiles})



    


from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages



def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone=form.cleaned_data.get('phone')
        profile.address=form.cleaned_data.get('address')
        profile.save()
        messages.success(request,'Account created successfully!please log in.')
        return redirect('login')
    else:
        form=RegisterForm()
        return render(request,'register.html',{'form':form})
                      

from .models import Restaurant
from .models import MenuItem
@login_required
def restaurant(request):
    restaurants=Restaurant.objects.all()
    return render(request,'restaurant.html',{'restaurants':restaurants})

@login_required
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items =MenuItem.objects.filter(restaurant=restaurant)

    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })



























# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate,login,logout
# from django.contrib import messages
# from .forms import RegisterForm
# from .models import Profile,User

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()

#             # Access or create the profile after user is saved
#             profile, created = Profile.objects.get_or_create(user=user)
#             profile.phone = form.cleaned_data.get('phone')
#             profile.address = form.cleaned_data.get('address')
#             profile.save()

#             messages.success(request, 'Account created successfully! Please log in.')
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})




# from django.contrib.auth.forms import AuthenticationForm

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')

#         try:
#             user = User.objects.get(username=username, email=email)
#         except User.DoesNotExist:
#             messages.error(request, "Invalid username or email.")
#             return render(request, 'login.html')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome back, {user.username}!")
#             return redirect('about')  # replace 'home' with your homepage route
#         else:
#             messages.error(request, "Incorrect password.")
#     return render(request, 'login.html')


# def about(request):
#     return render(request,'about.html')

from .models import MenuItem
@login_required
def about(request):
    items=MenuItem.objects.all()
    return render(request,'about.html',{'items':items})


def add_to_cart(request):
    if request.method=='POST':
        cart=request.session.get('cart',{})
        if not isinstance(cart,dict):
            cart={}
        
        for key, value in request.POST.items():
            if key.startswith('item_'):
                item_id=key.split('_')[1]
                try:
                    qty=int(value)
                except:
                    qty=0
                if(qty>0):
                    cart[item_id]=qty
                elif item_id in cart:
                    del cart[item_id]

        request.session['cart']=cart
        return redirect('cart_view')
    


from .models import MenuItem
def cart_view(request):
    cart=request.session.get('cart',{})   
    items=[]
    total=0
    for item_id,qty in cart.items():
        try:
            menu_item=MenuItem.objects.get(id=item_id)
            items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'quantity': qty,
                'image' :menu_item.image,
            })
            total+=menu_item.price*qty
        except MenuItem.DoesNotExist:
            pass
    return render(request,'cart.html',{'cart':items,'total':total})



def update_cart(request):
    if request.method=='POST':
        cart={}
        for key, value in request.POST.items():
            if key.startswith('item_'):
                item_id=key.split('_')[1]
                try:
                    qty=int(value)
                except ValueError:
                    qty=0
                if qty>0:
                    cart[item_id]=qty
        address=request.POST.get('address','').strip()

        if not address:
            messages.error(request,"please provide a delivery address")
            return redirect('cart_view')
        request.session['cart']=cart
        request.session['address']=address
        return redirect('cart_summary')
    else:
        return redirect('cart_view')
    

def cart_summary(request):
    cart=request.session.get('cart',{})
    address=request.session.get('address','')
    items=[]
    total=0

    for item_id, qty in cart.items():
        try:
            menu_item=MenuItem.objects.get(id=item_id)
            items.append({
                'name':menu_item.name,
                'price':menu_item.price,
                'quantity':qty,
                'image':menu_item.image,
            })
            total+=menu_item.price*qty
        except MenuItem.DoesNotExist:
            continue
    try:
        profile=request.user.profile
        phone=profile.phone
    except Profile.DoesNotExist:
        phone=''

    return render(request,'cart_summary.html',{
        'items':items,
        'total': total,
        'address':address,
        'user':request.user,
        'name':request.user.get_full_name ()or request.user.username,
        'phone':phone,
    })
  
from .models import Order,OrderItem,Profile
from django.conf import settings
from django.core.mail import send_mail

def place_order(request):
    if request.method=='POST':
        cart=request.session.get('cart',{})
        address=request.session.get('address','')
        if not cart or not address:
            messages.error(request,"Cart or address missing.")
            return redirect('cart_view')
        

        total=0
        profile=request.user.profile

        order=Order.objects.create(
            user=request.user,
            name=request.user.username,
            phone=profile.phone,
            address=address,
            total=0
        )
        for item_id,qty in cart.items():
            menu_item=MenuItem.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                price=menu_item.price
            )
            total+=menu_item.price*qty

        order.total=total
        order.save()

        request.session['çart']={}
        request.session['address']=''

        send_mail(
            subject='Order Confirmation -Dmeal',
            message="your order is delivered",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["dineshayadi584@gmal.com"],
            fail_silently=False,
        ) 
        return redirect('order_success')
    else:
        return redirect('cart_view')
    





def order_success(request):
    return render(request,'order_success.html')

