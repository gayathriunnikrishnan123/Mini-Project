from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

from django.conf import settings


class CustomUser(AbstractUser):
    
    EMPLOYER = 'employer'
    AGENT = 'agent'
    POLICE = 'police'
    ADMIN = 'admin'
    
    USER_TYPE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (AGENT, 'Agent'),
        (POLICE, 'Police'),
        (ADMIN, 'Admin'),
    ]

    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    adhar_number = models.CharField(max_length=12, null=True, blank=True)
    license_number = models.CharField(max_length=10, null=True, blank=True)
    police_id = models.CharField(max_length=6, null=True, blank=True)
    uploaded_file = models.FileField(upload_to='uploaded_files/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.pk:  
            if self.user_type == self.ADMIN:
                self.is_verified = True 
            else:
                self.is_verified = False 
        
        super().save(*args, **kwargs)
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=EMPLOYER  # Set a default role if needed
    )

    is_employer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_police = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)

    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    age = property(calculate_age)

    def __str__(self):
        return self.user.email

    def get_role(self):
        user_role = 'Unknown'
        if self.user.user_type == CustomUser.EMPLOYER:
            user_role = 'Employer'
        elif self.user.user_type == CustomUser.AGENT:
            user_role = 'Agent'
        elif self.user.user_type == CustomUser.POLICE:
            user_role = 'Police'
        return user_role

class WorkCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.name

class MigratoryWorker(models.Model):
    
    first_name = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    passport_number = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/')
    document = models.FileField(upload_to='documents')
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    police = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='police_workers', limit_choices_to={'is_police': True},blank=True, null=True)
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agent_workers', limit_choices_to={'is_agent': True})
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employer_workers', limit_choices_to={'is_employer': True},blank=True, null=True)

    def __str__(self):
        return self.first_name
    
class Police(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    badge_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100, blank=True, null=True)
    rank = models.CharField(max_length=50, blank=True, null=True)
    service_years = models.PositiveIntegerField(blank=True, null=True)
    station_name = models.CharField(max_length=100, blank=True, null=True)
    station_address = models.CharField(max_length=150, blank=True, null=True)
    station_contact = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.badge_number
