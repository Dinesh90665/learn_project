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
from .models import MenuItem,Order,OrderItem
from django.templatetags.static import static
from django.utils.html import format_html

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display=('id','name','price','description','image','image_preview')
    search_fields=('id','name')
    ordering=('id',)

    def image_preview(self,obj):
        if obj.image:
            url=static(f'creation/images/{obj.image}')
            return format_html('<img src="{}" width="50" height="50"/>',url)
        return "No Image"
    image_preview.short_description='Image'







class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','name','phone','created_at','total')
    list_filter=('created_at',)
    search_fields=('name','phone','address')
    inlines=[OrderItemInline]
from django.contrib import admin
from .models import OrderItem

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'restaurant_name', 'order_id', 'order_phone', 'quantity', 'price')
    search_fields = ('menu_item__name', 'order__id', 'order__phone')

    def order_id(self, obj):
        return obj.order.id
    order_id.admin_order_field = 'order'
    order_id.short_description = 'Order ID'

    def order_phone(self, obj):
        return obj.order.phone
    order_phone.short_description = 'Order Phone'

    def restaurant_name(self, obj):
        return obj.menu_item.restaurant.name
    restaurant_name.short_description = 'Restaurant'

from .models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display=('id','name','description','place','facility','image','image_tag')
    search_fields=('id','name')
    ordering=('id',)


    def image_tag(self,obj):
        if obj.image:
            url=static(f'creation/images/{obj.image}')
            return format_html('<img src="{}" width="50",height="50" />',url)
        return "No Image"
    
    image_tag.short_description='Image'

