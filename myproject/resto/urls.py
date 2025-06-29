from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('submit-review/', views.submit_review, name='submit_review'),# type: ignore
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('increase-quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('payment/', views.payment, name='payment'),
    path('payment-handler/', views.payment_handler, name='payment_handler'),
   
]

