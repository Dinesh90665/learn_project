from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    phone=forms.CharField(max_length=15, required=False)
    address=forms.CharField(widget=forms.Textarea,required=False)

class Meta:
    model=User
    fields= ['username','email','phone','address','password1','password2']


class LoginForm(AuthenticationForm):
    username=forms.CharField(max_length=150)
    password=forms.CharField(widget=forms.PasswordInput)



# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     phone = forms.CharField(max_length=15, required=False)
#     address = forms.CharField(widget=forms.Textarea, required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'phone', 'address', 'password1', 'password2']


# from django.contrib.auth.forms import AuthenticationForm

# # Login form (username + password only usually)
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(max_length=150)
#     password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    class Meta:
        model=Restaurant
        fields=['name','place','description','facility','image']

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'place':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'facility':forms.TextInput(attrs={'class':'form-control'}),
        }