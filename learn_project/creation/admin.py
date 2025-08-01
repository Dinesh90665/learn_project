from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','get_email','phone','address')
    search_fields=('user__username','phone','user__email')


    def get_email(self,obj):
        return obj.user.email
    get_email.short_description='Email'
# from django.contrib import admin
# from .models import Profile

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'get_email', 'phone', 'address')
#     search_fields = ('user__username', 'phone', 'user__email')

#     def get_email(self, obj):
#         return obj.user.email
#     get_email.short_description = 'Email'