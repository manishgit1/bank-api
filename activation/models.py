
from django.db import models
from django.http import HttpResponse
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from pyotp import TOTP
from django.utils.crypto import get_random_string
from twilio.rest import Client
from backend import settings
import vonage

class AppUserManager(BaseUserManager):
    def create_user(self, email, name, password, phone_number, account_number, transaction_pin, is_verified, otp_token):
        if not email:
            raise ValueError('An email is required.')
        if not name:
            raise ValueError('A username is required.')
        if not password:
            raise ValueError('A password is required.')
        if not phone_number:
            raise ValueError('A phone number is required.')
        if not account_number:
            raise ValueError('An account number is required.')
        if not transaction_pin:
            raise ValueError('A transaction pin is required.')
        

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, account_number=account_number, transaction_pin=transaction_pin, is_verified=is_verified, otp_token=otp_token)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, phone_number, account_number):
        if not email:
            raise ValueError('An email is required.')
        if not name:
            raise ValueError('A username is required.')
        if not password:
            raise ValueError('A password is required.')
        if not phone_number:
            raise ValueError('A phone number is required.')
        if not account_number:
            raise ValueError('An account number is required.')

        user = self.create_user(email, name, password, phone_number, account_number)
        user.is_superuser = True
        user.save()
        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, default='', blank=True, null=True)
    account_number = models.CharField(max_length=30, default='', unique=True, blank=True, null=True)
    account_balance= models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_pin = models.CharField( null=False, max_length = 4)
    otp_token= models.CharField(max_length = 10, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'account_number', 'transaction_pin']
    objects = AppUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='appuser_groups',
        related_query_name='appuser_group',
        blank=True,
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='appuser_user_permissions',
        related_query_name='appuser_user_permission',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.name
    
    # def is_otp_valid(self, otp):
    #     totp = TOTP(self.otp)
    #     return totp.verify(otp, self.otp_expiry)
    
    
    @staticmethod
    def send_otp(phone_number):
      
      otp = get_random_string(allowed_chars=['0245'], length=1)

      

    #   subject = 'Your OTP Verification Code'
    #   message = f'Your OTP is {otp}'

      
      client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

      message = client.messages \
                .create(
                     body= f"Your OTP code for internet banking verification is {otp}",
                     from_='+12097582997',
                     to='+9779844795071'
                 )

      return otp
     
    #   if responseData["messages"][0]["status"] == "0":
    #       print("Message sent successfully.")
          
    #       return otp
    #       #responseData.set_cookie("otp", otp)
    #   else:
    #       print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
     

      

class BankAccount(models.Model):
     
     account_holder_name = models.CharField(max_length=25)
     account_number = models.CharField( max_length=30,unique=True)







    

     
         
