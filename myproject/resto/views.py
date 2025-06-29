from http import client
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from .models import  CartItem, Contact, Item, Item_list, Booking, Review
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import razorpay  # type: ignore
from django.views.decorators.csrf import csrf_exempt

def home(request):
    items = Item.objects.all()
    lists = Item_list.objects.all()
    categories = Item_list.objects.prefetch_related('items').all()
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'items': items, 'lists': lists, 'categories': categories, 'reviews': reviews})

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def menu(request):
    items = Item.objects.all()
    lists = Item_list.objects.all()
    categories = Item_list.objects.prefetch_related('items').all()
    return render(request, 'menu.html', {'items': items, 'lists': lists, 'categories': categories})

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)
   
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})
    # Check the total price
     
@login_required
def add_to_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    cart_item, created = CartItem.objects.get_or_create(item=item, user=request.user)

    print(f"Created: {created}, Current Quantity: {cart_item.quantity}")

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('view_cart')
 
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity <= 1:
      cart_item.delete()
    else:  
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')


def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
    

def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity -= 1
    cart_item.save()
    return redirect('view_cart')

def payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.item.price * item.quantity for item in cart_items)
    total_price_paise = int(total_price * 100) # Razorpay needs paise
    
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    payment = client.order.create({
       'amount': total_price_paise,
       'currency': 'INR',
       'payment_capture': '1',  # Auto capture
    })
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'order_id': payment['id'],
        'amount': total_price_paise
    }
    return render(request, 'payment.html', context)

@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id")
            order_id = request.POST.get("razorpay_order_id")
            signature = request.POST.get("razorpay_signature")
            
            
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
              
            # This will raise a SignatureVerificationError if verification fails
            client.utility.verify_payment_signature(params_dict) # type: ignore

            # (Optional) You can verify the signature here

            # Clear cart after successful payment
            CartItem.objects.filter(user=request.user).delete()

            return render(request, 'payment_success.html')
        except:
            return HttpResponseBadRequest()
    return HttpResponseBadRequest("Invalid request")

def booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date = request.POST.get('date')
        time = request.POST.get('time')
        contact = request.POST.get('number')
        num_people = request.POST.get('people')
        request_type = request.POST.get('request')

        full_message = f"Name: {name}\nContact: {contact}\nEmail: {email}\nRequest: {request_type}\nDate: {date}\nTime: {time}\nNumber of People: {num_people}"
        Booking.objects.create(
            name=name,
            email=email,
            date=date,
            time=time,
            contact=contact,
            num_people=int(num_people),
            request_type=request_type
        )
        email_message = EmailMessage(
            subject=f"Booking Request For Dinner: {request_type}",
            body=full_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[admin[1] for admin in settings.ADMINS],
            reply_to=[email]
        )
        email_message.send(fail_silently=False)
        messages.success(request, 'Your booking has been made successfully!')
        return redirect('home')
    return render(request, 'booking.html')

def team(request):
    return render(request, 'team.html')


def submit_review(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        Review.objects.create(user=request.user, message=message)
        messages.success(request, 'Your review has been submitted successfully!')
        return redirect('testimonial')

def testimonial(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'testimonial.html', {'reviews': reviews})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Name: {name}\nSubject: {subject}\nEmail: {email}\nMessage: {message}"

        Contact.objects.create(name=name, subject=subject, email=email, message=message)

        email_message = EmailMessage(
            subject=f"Contact Message: {subject}",
            body=full_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[admin[1] for admin in settings.ADMINS],
            reply_to=[email]
        )
        email_message.send(fail_silently=False)
        messages.success(request, 'Your message has been sent successfully!')
        return render(request, 'contact.html')
    return redirect('home')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

        return redirect('login')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        email = request.POST.get('email').strip()
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if password != cpassword:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('signup')

        name_parts = name.split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('login')
    return render(request, 'signup.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


