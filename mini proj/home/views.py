
from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import CustomUser,UserProfile


# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def userpage(request):
    # Your view logic goes here
    return render(request, 'userpage.html') 

# def register(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         username = request.POST.get('username')
#         phoneNumber=request.POST.get('phoneNumber')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         cpassword=request.POST.get('cpassword')
#         my_user = User.objects.create_user(username=username, email=email, password=password)
#         my_user.save()
#         return redirect('/login')
    
#     return render(request,'register.html')

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         if email and password:
#             user = authenticate(request, email=email, password=password)
            
#             if user is not None:
#                 auth_login(request, user)

                
#                 if user.is_customer:
#                     return redirect('userpage')  # Redirect to customer index page
#                 # Add an elif condition for seller if needed
                
#             else:
#                 error_message = "Invalid login credentials."
#                 messages.error(request, error_message)
                
#         else:
#             error_message = "Email and password are required fields."
#             messages.error(request, error_message)
    
#     return render(request, 'login.html')

# def logout_user(request):
#     logout(request)  # Logout the user
#     return redirect('login')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phoneNumber', None)
        password = request.POST.get('password', None)    
        confirm_password = request.POST.get('cpassword', None)
        # role = CustomUser.CUSTOMER
        if name and username and email and phone and password:
            # if CustomUser.objects.filter(email=email,username=username).exists():
            #     # error_message = "Email is already registered."
            #     return render(request, 'register.html')
            # elif password!=confirm_password:
            #     # error_message = "Password's Don't Match, Enter correct Password"
            #     return render(request, 'register.html')
            # else:
                user = CustomUser(name=name, username=username, email=email, phone=phone)
                user.set_password(password)  # Set the password securely
                user.is_active=False
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()
                # activateEmail(request, user, email)
                return redirect('login')  
            
    return render(request, 'register.html')


# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST["email"]
#         password = request.POST["password"]
#         user = authenticate(request, email=email , password=password)
#         if user is not None:
#             auth_login(request, user)
#             return redirect('/userpage')
#         else:
#            messages.success(request,("Invalid credentials."))
#         # print(username)  # Print the email for debugging
#         # print(password)  # Print the password for debugging

#         # if email and password:
#         # user = authenticate(request, email=email , password=password)
#         # if user is not None:
#         #     auth_login(request,user)
#         #     return redirect('/userpage')
#         #         # if request.user.role==CustomUser.EMPLOYER:
                
#         #         #     return redirect('/userpage')
#         #         # # elif request.user.user_typ == CustomUser.VENDOR:
#         #         # #     print("user is therapist")
#         #         # #     return redirect(reverse('therapist'))
#         #         # elif request.user.role == CustomUser.ADMIN:
#         #         #     print("user is admin")                   
#         #         #     return redirect('http://127.0.0.1:8000/')
#         #         # else:
#         #         #     print("user is normal")
#         #         #     return redirect('')

#         # else:
#         #         messages.success(request,("Invalid credentials."))
#         # else:
#         #     messages.success(request,("Please fill out all fields."))
        
#     return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

        if username and password:
            user = authenticate(request, username=username, password=password)
            print("authenticated")

            if user is not None:
               
                auth_login(request, user)
                # Redirect based on user_type
                if user.role == CustomUser.ADMIN:
                    return redirect('http://127.0.0.1:8000/admin/login/?next=/admin/')
                elif user.role == CustomUser.AGENT:
                    return redirect(reverse('index'))
                elif user.role == CustomUser.EMPLOYER:
                    return redirect('userpage')
                else:
                    return redirect('/userpage')
                
            else:
                return HttpResponseRedirect(reverse('login') + '?alert=invalid_credentials')
        else:
            return HttpResponseRedirect(reverse('login') + '?alert=fill_fields')

    # For GET requests or if authentication fails, display the login form
    return render(request, 'login.html')
def userLogout(request):
    logout(request)
    return redirect('userpage') 



