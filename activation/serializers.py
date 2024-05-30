from rest_framework import serializers 
from django.contrib.auth import  authenticate

from .validations import custom_validation
from .models import AppUser, BankAccount
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from rest_framework.response import Response




#Serializer for user registration

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    account_number = serializers.CharField(write_only=True)
    transaction_pin = serializers.CharField(max_length=4)

    class Meta:
        model = AppUser
        fields = ['email', 'name', 'password', 'phone_number', 'account_number', 'transaction_pin']

    def validate_account_number(self, value):
        try:
            BankAccount.objects.get(account_number=value)
        except BankAccount.DoesNotExist:
            raise serializers.ValidationError('Invalid account number')
        return value

    def validate(self, data):
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Check if email is provided and unique
        if not email or AppUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Please provide a valid and unique email address')

        # Check if password meets minimum length requirement
        if not password or len(password) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')

        # Check if transaction_pin is provided
        transaction_pin = data.get('transaction_pin')
        if transaction_pin is None:
            raise serializers.ValidationError("Transaction Pin is required")

        # Additional custom validations can be added here

        return data


        
    
#Serializer for user login
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
    phone_number = serializers.CharField(required=False)

    def validate(self, data):
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not (email or phone_number):
            raise serializers.ValidationError('Either email or phone number is required.')

        user = None

        if email:
            #user = authenticate(username=email, password=password)
            user = AppUser.objects.get(email=email)

            print("USER: ", user)
        elif phone_number:
            try:
                user_instance = AppUser.objects.get(phone_number=phone_number)
                user = authenticate(username=user_instance.email, password=password)
            except AppUser.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials!')

        if user is None:
            raise serializers.ValidationError('Invalid credentials!')

        #self.data['user'] = user
        return user 

#Serializer for user details
            
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('email', 'name', 'phone_number', 'account_number', 'account_balance')

class OtpSerializer(serializers.ModelSerializer):

     class Meta:
        model = AppUser
        fields = ['otp_token']   





