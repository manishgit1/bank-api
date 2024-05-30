from django.contrib.auth import  login, logout
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken
from knox.auth import TokenAuthentication

from .serializers import ( UserLoginSerializer, 
UserRegisterSerializer,
UserSerializer)
from rest_framework import permissions, status
from .models import AppUser

#logic for registering user


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():

           validated_data = serializer.validated_data

            # Save user data in session
            # request.session['user_data'] = validated_data
            # request.session.set_expiry(300)  # Set session expiry to 5 minutes

               # Send OTP to the user
           otp = AppUser.send_otp(validated_data['phone_number'])
   
           AppUser.objects.create_user(
                    email=validated_data['email'],
                    password=validated_data['password'],
                    name=validated_data['name'],
                    phone_number=validated_data['phone_number'],
                    account_number=validated_data['account_number'],
                    transaction_pin=validated_data['transaction_pin'],
                    is_verified=False,
                    otp_token = otp
                )
          

           return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        else:
             return HttpResponse(serializer.error_messages, status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    permission_classes = [permissions.AllowAny,]
    def post(self, request):

        otp_entered = request.data.get('otp_entered')
        email = request.data.get('email')

        user = AppUser.objects.get(email=email)

        print(user)
        # print("USER REGISTERED RECENTLY ",user.name)

        otp_token = user.otp_token
        print("Otp token: ", otp_token)
        print("OTP entered by user: ", otp_entered)  # Debugging line

        if otp_token == otp_entered:
                
                user.is_verified = True
                user.save()

                return Response({'message': 'OTP verification successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)








class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)


        if serializer.is_valid(raise_exception=True):
            user = serializer.validate(serializer.data)
               
              
            try:
                 login(request,user)
                 _, token  = AuthToken.objects.create(user=user)

                 return Response({
                    'email': user.email,
                    'account_number': user.account_number,
                    'access_token': token
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



#logout view logic here
class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


#return the state of user with user data
class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
    
	authentication_classes = (TokenAuthentication,)
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
          



        


      



