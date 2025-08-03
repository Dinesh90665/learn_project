from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username
# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15, blank=True)
#     address = models.TextField(blank=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

#     def __str__(self):
#         return self.user.username



    class Meta:
        ordering=['id',]
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    phone =models.CharField(max_length=20)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(max_digits=10,decimal_places=2)


    def __str__(self):
        return f"Order #{self.id} by {self.name}"
    


class Restaurant(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.CharField(max_length=200)
    place=models.CharField(max_length=100)
    facility=models.TextField(max_length=225)

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.name
    
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('restaurant', 'name')

    def __str__(self):
        return f"{self.name}({self.restaurant.name})"
    



class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    menu_item=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name}*{self.quantity}"


    
