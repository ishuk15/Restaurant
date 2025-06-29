from django.contrib import admin
from .models import CartItem, Contact, Item, Item_list,Booking, Review

admin.site.register(Item)
admin.site.register(Item_list)
admin.site.register(Contact)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(CartItem)


