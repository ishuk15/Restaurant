from django.db import models

from django.utils import timezone 
from django.contrib.auth.models import User
 # This should print the id of the order

class Item_list(models.Model):
    category_name = models.CharField(max_length=20)
    ITEM_CAT_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
       
    ]
    item_cat = models.CharField(max_length=20, choices=ITEM_CAT_CHOICES, default='Breakfast')
        

    def __str__(self):
        return self.category_name

class Item(models.Model):
    item_name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Item_list, related_name = "items" ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=False, null=False)


    def __str__(self):
        return f"{self.item_name} - {self.category.category_name} - {self.price} - {self.description} - {self.image}"    


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
     


    def __str__(self):
        return f"{self.item.item_name} - {self.quantity} - {self.user.username} - {self.date_added}"

  
class Contact(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.message} - {self.subject}"
   
   

    
class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    contact = models.CharField(max_length=15)
    num_people = models.IntegerField()
    request_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.email} - {self.date} - {self.time} - {self.contact} - {self.num_people} - {self.request_type}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.message} - {self.created_at}"
    
    