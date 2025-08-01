from django.shortcuts import render,redirect, HttpResponse


from .models  import Profile,User
def login_view(request):
    if(request.method=='POST'):
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')

        try:
            user=User.objects.get(username=username,email=email)
        except User.DoesNotExist:
            messages.error(request,'invalid username or email')
            return render(request,'login.html')
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f"Welcome back, {user.username}!")
            return redirect('about')
        else:
            messages.error(request,"Incorrect password")
    return render(request,'login.html')
from django.contrib.auth.decorators import login_required
        
@login_required
def about(request):
    profile=request.user.profile
    return render(request,'about.html')
    


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
                      


def about(request):
    return render(request,'about.html')


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