from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

@login_required(login_url='login')
def userpage(request):
    # Your view logic goes here
    return render(request, 'userpage.html') 

def worker_list(request):
    # Your view logic goes here
    return render(request, 'worker_list.html')

from django.shortcuts import get_object_or_404, redirect
from home.models import CustomUser 

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'GET':
        user.delete()
        return redirect('adminpanel')  

    
    return render(request, 'adminpanel.html', {'user': user})






from  django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from .tokens import account_activation_token
from .models import CustomUser, UserProfile  # Make sure to import your models
from django.contrib.sites.models import Site

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if the user is already active
        if user.is_active:
            messages.warning(request, "Your account is already activated. You can log in.")
            return redirect('login')

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Thank you for confirming your email. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or has expired. Please request a new one.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Activation link is invalid. Please request a new one.")

    return redirect('login')
def activateEmail(request, user):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    to_email = user.email  # Get the user's email from the user object
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user.username}</b>, please go to your email <b>{to_email}</b> inbox and click on \
                the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')



from .models import CustomUser, UserProfile  # Import your models

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phoneNumber', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('cpassword', None)
        role = request.POST.get('user_type', None)  # Updated field name

        if name and username and email and phone and password and role:
            # Assuming you have constants for user type choices in your CustomUser model
            # Replace CustomUser.EMPLOYER, CustomUser.AGENT, etc., with actual constants
            if role == CustomUser.EMPLOYER:
                is_employer = True
                is_agent = False
                is_police = False
            elif role == CustomUser.AGENT:
                is_employer = False
                is_agent = True
                is_police = False
            elif role == CustomUser.POLICE:
                is_employer = False
                is_agent = False
                is_police = True
            else:
                # Handle an invalid role here, e.g., show an error message
                return render(request, 'register.html', {'error': 'Invalid user type'})

            user = CustomUser(
                name=name,
                username=username,
                email=email,
                phone=phone,
                is_employer=is_employer,  # Set the user type-specific attributes
                is_agent=is_agent,
                is_police=is_police,
                user_type=role,
            )
            user.set_password(password)  # Set the password securely
            user.is_active = False
            user.save()
            user_profile = UserProfile(user=user)
            user_profile.save()
            # Assuming you have a function to send an activation email
            activateEmail(request, user)

            return redirect('login')

    return render(request, 'register.html')




def registration_success(request):
    return render(request, 'registration_success.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

        if username and password:
            user = authenticate(request, username=username, password=password)
            print("authenticated")

            if user is not None:
                request.session['username']=username 
                auth_login(request, user)
                # Redirect based on user_type
                if user.is_admin==True:
                    return redirect('/adminpanel')
                elif user.is_agent==True:
                    return redirect('agentpage')
                elif user.is_employer==True:
                    return redirect('userpage')
                elif user.is_police==True:
                    return redirect('policepage')
                # else:
                #     return redirect('/userpage')
                
            else:
                return HttpResponseRedirect(reverse('login') + '?alert=invalid_credentials')
        else:
            return HttpResponseRedirect(reverse('login') + '?alert=fill_fields')

    # For GET requests or if authentication fails, display the login form
    return render(request, 'login.html')



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def agentpage(request):
    # Your view logic goes here
    return render(request, 'agentpage.html') 
from django.core.files.uploadedfile import InMemoryUploadedFile


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MigratoryWorker
from django.db import transaction

def addworker(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        dob = request.POST.get('dob_0')
        nationality = request.POST.get('nationality')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        passport_number = request.POST.get('passport_number')
        profile_image = request.FILES.get('profile_image')
        document = request.FILES.get('document')

        # You should perform validation and additional checks here before saving

        worker = MigratoryWorker(
            agent=request.user,
            first_name=first_name,
            dob=dob,
            nationality=nationality,
            address=address,
            contact_number=contact_number,
            passport_number=passport_number,
            profile_image=profile_image,
            document=document
        )
        worker.save()

        # Redirect to a success page or another URL
        
        return redirect('viewworker')  # Redirect to the worker list page

    return render(request, 'addworker.html')






def viewworker(request):
    workers = MigratoryWorker.objects.all()  # Query your model to get the workers
    
    return render(request, 'viewworker.html', {'workers': workers}) 
from .models import MigratoryWorker

def update_worker(request, worker_id):
    # Get the worker object to update
    worker = get_object_or_404(MigratoryWorker, id=worker_id)

    if request.method == 'POST':
        # If the request method is POST, it means the user submitted an update
        worker.first_name = request.POST['first_name']
        worker.dob = request.POST['dob']
        worker.nationality = request.POST['nationality']
        worker.address = request.POST['address']
        worker.contact_number = request.POST['contact_number']
        worker.passport_number = request.POST['passport_number']
        worker.save()
        # You can also add a success message here if you're using Django messages framework
        return redirect('viewworker')  # Redirect to the worker list page

    return render(request, 'update_worker.html', {'worker': worker})

from django.shortcuts import render, redirect, get_object_or_404

def delete_worker(request, worker_id):
   
    worker = get_object_or_404(MigratoryWorker, id=worker_id)
    if request.method == 'GET':
       
        worker.delete()
       
        return redirect('viewworker')  

    return render(request, 'viewworker.html', {'worker': worker})



def policepage(request):
    # Your view logic goes here
    return render(request, 'policepage.html') 
@login_required(login_url='login')
def adminpanel(request):
    users = CustomUser.objects.all()
    user_count = users.count()  # Calculate the count of users
   
    context = {
        'users': users,
        'user_count': user_count, 
       # Pass the user count to the template
        
    }
    return render(request,'adminpanel.html',context)

from rest_framework.generics import ListAPIView
from .models import CustomUser


class PoliceOfficerViewSet(ListAPIView):
    queryset = CustomUser.objects.all()

    

    def list(self, request, *args, **kwargs):

       
        queryset = self.get_queryset()
        
        return render(request,'worker_list.html',{'worker_list':queryset})
    

    from django.shortcuts import render, redirect
from .models import MigratoryWorker
from django.contrib import messages

