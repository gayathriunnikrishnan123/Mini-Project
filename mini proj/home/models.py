from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    EMPLOYER = 1
    AGENT = 2
    POLICE = 3
    ADMIN = 4

    USER_TYPES = (
        (EMPLOYER, 'Employer'),
        (AGENT, 'Agent'),
        (POLICE, 'Police'),
        (ADMIN,'Admin'),
    )

    
    name = models.CharField(max_length=50, null = True, blank = True)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, null=True, blank = True)
    password = models.CharField(max_length=128)
    #password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=USER_TYPES, blank=True, null=True)


    is_admin = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_employer = models.BooleanField(default=False)
    is_police = models.BooleanField(default=False)

    def str(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    # country = models.CharField(max_length=15, default="India", blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)


    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    age = property(calculate_age)


    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender)

    def str(self):
        return self.user.email
    
    def get_role(self): 
        if self.role == 1:
            user_role = 'Employer'
        elif self.role == 2:
            user_role = 'Agent'
        elif self.role == 3:
            user_role = 'Police'
        return user_role


