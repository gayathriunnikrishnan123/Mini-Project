from django.shortcuts import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import *
from django.views.decorators.cache import *

@never_cache
@login_required(login_url='login')
def verify_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method=='POST':
        user.is_active=True
        user.is_verified = True
        user.save()
    
    return render(request, 'varify_user.html', {'user': user})

def agentprofile(request):
    # Get or create a CustomUser instance based on the user's ID
    user_pro, created = CustomUser.objects.get_or_create(id=request.user.id)
    
    # Fetch the user profile based on the user's ID
    user = CustomUser.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        user.save()

    # Render the 'agentprofile.html' template with the 'user' context
    return render(request, 'agentprofile.html', {'user': user})





def verifyuser(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.is_active=True
        user.is_verified = True
        user.save()
       
        return redirect('users') 

    return render(request, 'varifyuser.html', {'user': user})

def rejectuser(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.is_active=False
        user.is_verified = False
        user.is_rejected = True  
        user.save()
        
        return redirect('users') 




# Create your views here.
def index(request):
    return render(request,'index.html')


def about(request):
    return render(request,'about.html')


def services(request):
    return render(request,'services.html')

@never_cache
@login_required(login_url='login')
def users(request):
    users = CustomUser.objects.all()
    user_count = users.count()  # Calculate the count of users
   
    context = {
        'users': users,
        'user_count': user_count, 
       # Pass the user count to the template
        
    }
    return render(request,'users.html',context)



from django.shortcuts import render
from django.http import JsonResponse
from .models import WorkCategory
from django.views.decorators.csrf import csrf_exempt

@never_cache
@login_required(login_url='login')
def workcategory(request):
    if request.method == 'POST':
        name = request.POST.get('category-name')
        description = request.POST.get('category-description')
        
        if name:  
            category = WorkCategory(name=name, description=description)
            category.save()
            return redirect("workcategory") 
        
    
    categories = WorkCategory.objects.all()
    return render(request, 'workcategory.html', {'categories': categories})

@never_cache
@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(WorkCategory, pk=category_id)
    if request.method == 'GET':
        category.delete()
        return redirect('workcategory')  # Redirect to the workcategory view after deletion

    return render(request, 'workcategory.html', {'categories': WorkCategory.objects.all()})

@never_cache
@login_required(login_url='login')
def edit_category(request, category_id):
    category = get_object_or_404(WorkCategory, pk=category_id)
    
    if request.method == 'POST':
        # Assuming you have form fields with 'name' and 'description'
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        # Update category fields
        category.name = name
        category.description = description
        category.save()
        
        return redirect('workcategory')  # Redirect to workcategory view after editing
    
    return render(request, 'edit_category.html', {'category': category})
    



@never_cache
@login_required(login_url='login')
def userpage(request):
    # Your view logic goes here
    return render(request, 'userpage.html')

from .models import UserProfile  # Import the UserProfile model

from django.core.files.uploadedfile import InMemoryUploadedFile
@never_cache
@login_required(login_url='login')
def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        state = request.POST.get('state')
        district = request.POST.get('district')
        gender = request.POST.get('gender')
        pincode = request.POST.get('pincode')

        # Update the profile fields
        user_profile.fullname = fullname
        user_profile.phone = phone
        user_profile.state = state
        user_profile.district = district
        user_profile.gender = gender
        user_profile.pincode = pincode

        user_profile.save()
        return redirect('user_profile')
    return render(request, 'user_profile.html', {'user_profile': user_profile})
 
@never_cache
@login_required(login_url='login')
def worker_list(request):
       
    return render(request, 'worker_list.html', {'workers': MigratoryWorker.objects.all()})

   
from django.shortcuts import get_object_or_404, redirect
from home.models import CustomUser 
@never_cache
@login_required(login_url='login')
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



from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import CustomUser, UserProfile  # Import your models




from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        role = request.POST.get('user_type')

        adhar_number = request.POST.get('adharNumber')
        license_number = request.POST.get('licenseNumber')
        police_id = request.POST.get('policeId')
        uploaded_file = request.FILES.get('imageToUpload')

       

        if uploaded_file:
            try:

                # Determine role
                is_employer = role == 'employer'
                is_agent = role == 'agent'
                is_police = role == 'police'

                

                # Assuming CustomUser is an extension of the Django User model
                custom_user = CustomUser(
                    name=name,
                    username=username,
                    email=email,
                    phone=phone,
                    user_type=role,
                    is_employer=is_employer,
                    is_agent=is_agent,
                    is_police=is_police,
                    is_active=False,
                    adhar_number=adhar_number,
                    license_number=license_number,
                    police_id=police_id,
                    uploaded_file= uploaded_file
                )
                custom_user.set_password(password)  # Hash the password
                custom_user.save()

                user_profile = UserProfile(user=custom_user)
                user_profile.save()

                # activateEmail(request, user)

                return redirect('login')
            except Exception as e:
                print(f"Registration failed: {e}")
                return render(request, 'register.html', {'error': 'Registration failed'})
        else:
            return render(request, 'register.html', {'error': 'No file uploaded'})

    return render(request, 'register.html')





def registration_success(request):
    return render(request, 'registration_success.html')


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
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


@never_cache
@login_required(login_url='login')
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@never_cache
@login_required(login_url='login')
def agentpage(request):
    # Your view logic goes here
    return render(request, 'agentpage.html') 
from django.core.files.uploadedfile import InMemoryUploadedFile


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MigratoryWorker
from django.db import transaction
@never_cache
@login_required(login_url='login')
def addworker(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        dob = request.POST.get('dob_0')
        nationality = request.POST.get('nationality')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        adhar_number = request.POST.get('adhar_number')

        category_id = request.POST.get('work_assign')
        category = WorkCategory.objects.get(id=category_id) if category_id else None

        profile_image = request.FILES.get('profile_image')
        document = request.FILES.get('document')

        worker = MigratoryWorker(
            agent=request.user,
            first_name=first_name,
            dob=dob,
            nationality=nationality,
            address=address,
            contact_number=contact_number,
            adhar_number=adhar_number,
            category=category,
            profile_image=profile_image,
            document=document,
        )
        worker.save()
        return redirect('viewworker')

    categories = WorkCategory.objects.all()
    return render(request, 'addworker.html', {'categories': categories})

    

    

@never_cache
@login_required(login_url='login')
def workerprofile(request):
    workers = MigratoryWorker.objects.all()  # Query your model to get the workers
    
    return render(request, 'workerprofile.html', {'workers': workers}) 
@never_cache
@login_required(login_url='login')
def viewprofile(request,worker_id):
    worker = MigratoryWorker.objects.get(id=worker_id)  # Fetch the worker by ID from the database
    
    return render(request, 'viewprofile.html', {'worker': worker})




@never_cache
@login_required(login_url='login')
def viewworker(request):
    # Assuming 'agent' field in MigratoryWorker model represents the user who added the worker
    user = request.user
    workers = MigratoryWorker.objects.filter(agent=user)  # Filter workers added by the logged-in user
    categories = WorkCategory.objects.all()
    return render(request, 'viewworker.html', {'workers': workers, 'categories': categories})


def verify_worker(request, worker_id):
    worker = get_object_or_404(MigratoryWorker, id=worker_id)
    worker.is_verified = True
    worker.is_rejected = False
    worker.save()
    return HttpResponse("Worker has been verified successfully.")

def reject_worker(request, worker_id):
    worker = get_object_or_404(MigratoryWorker, id=worker_id)
    worker.is_verified = False
    worker.is_rejected = True
    worker.save()
    return HttpResponse("Worker has been rejected.")




@never_cache
@login_required(login_url='login')
def update_worker(request, worker_id):
    worker = get_object_or_404(MigratoryWorker, id=worker_id)

    categories = WorkCategory.objects.all()

    if request.method == 'POST':

        worker.first_name = request.POST['first_name']
        worker.dob = request.POST['dob']
        worker.nationality = request.POST['nationality']
        worker.address = request.POST['address']
        worker.contact_number = request.POST['contact_number']
        worker.adhar_number = request.POST['adhar_number']

        category_id = request.POST.get('work_assign')
        selected_category = WorkCategory.objects.get(pk=category_id)
        worker.category = selected_category

        worker.gender = request.POST.get('gender')

        if 'profile_image' in request.FILES:
            worker.profile_image = request.FILES['profile_image']

        if 'document' in request.FILES:
            worker.document = request.FILES['document']

        worker.save()
        return redirect('viewworker')
    return render(request, 'update_worker.html', {'worker': worker, 'categories': categories})

from django.shortcuts import render, redirect, get_object_or_404
@never_cache
@login_required(login_url='login')
def delete_worker(request, worker_id):
   
    worker = get_object_or_404(MigratoryWorker, id=worker_id)
    if request.method == 'GET':
       
        worker.delete()
       
        return redirect('viewworker')  

    return render(request, 'viewworker.html', {'worker': worker})


@never_cache
@login_required(login_url='login')
def policepage(request):
    # Your view logic goes here
    return render(request, 'policepage.html') 

def incidentreported(request):
    total_added = MigratoryWorker.objects.count()  # Total number of workers added
    total_verified = MigratoryWorker.objects.filter(is_verified=True).count()  # Total number of workers verified
    total_rejected = MigratoryWorker.objects.filter(is_rejected=True).count()  # Total number of workers rejected

    return render(request, 'incidentreported.html', {
        'total_added': total_added,
        'total_verified': total_verified,
        'total_rejected': total_rejected
    })
   

def activeofficers(request):
    # Fetch all police officers
    police_officers = CustomUser.objects.filter(user_type='police')


    return render(request, 'activeofficers.html', {'police_officers': police_officers})
    


@never_cache
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


class WorkerListView(ListAPIView):
    queryset = MigratoryWorker.objects.all()
    template_name = 'worker_list.html'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
       

 

