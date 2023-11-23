from django.shortcuts import render
from .serializer  import UserSerializer,OTPverificationSerializer,UserLoginSerializer,UserDetailsSerializer,ForgotPasswordSerializer, VerifySerializer,ConfirmpasswordSerializer,ForgotOTPverificationSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
import random
from smtplib import SMTPException
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import User
from django.utils import timezone
from django.core.mail import send_mail
from carpool import settings
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def send_otp_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER  # Use the configured email address
    to_email = email

    try:
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
    except SMTPException as e:
        print(f"Email sending failed: {e}")
    except Exception as e:
        return Response({"message": "Failed to send OTP via email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = user.generate_new_otp()
            user.otp = otp
            user.otp_timestamp = timezone.now()
            user.last_resend_time = None
            user.save()
            email = user.email
            send_otp_email(email, otp)
            request.session['email'] = email
            email = request.session.get('email')
            return Response({"message": "User registered. Please check your email for OTP"})
        else:
            errors = serializer.errors
            return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp =request.data.get("otp")
        if email and otp is None:
            user = User.objects.get(email=email)
            print("here i am printing the user",user)

            if user.resend_count < 3:
                otp = user.generate_new_otp()
                user.otp = otp
                user.otp_timestamp = timezone.now()
                user.resend_count += 1
                user.save()
                send_otp_email(email, otp)
                return Response({"message": "New OTP sent. Please check your email"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You've reached the resend limit for OTP. Please register again."}, status=status.HTTP_400_BAD_REQUEST)

    
        serializer = OTPverificationSerializer(data=request.data)
        session_id = request.session.session_key

        if serializer.is_valid():
            otp = serializer.data["otp"]
            email = serializer.data["email"]
            user = User.objects.get(email=email)
            current_time = timezone.now()

        
            if (current_time - user.otp_timestamp).total_seconds() <= 60:
                if user.otp == otp:
                    print("haii",user.otp,otp) 
                    user.is_active = True
                    user.otp = ""
                    user.save()
                    return Response({"message": "User successfully registered"}, status=status.HTTP_200_OK)
                else:
                    user.resend_count += 1
                    user.save()
                    if user.resend_count < 3:
                        otp = user.generate_new_otp()
                        user.otp = otp
                        user.otp_timestamp = current_time
                        user.save()
                        send_otp_email(email, otp)
                        return Response({"error": "Incorrect OTP. New OTP sent. Please check your email"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"error": "You've reached the resend limit for OTP. Please register again."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Your OTP has expired, and you've reached the resend limit."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        print("here the request",request)
        print("Headers:", request.headers)
        print("Data:", request.data)
        
        response = super().post(request, *args, **kwargs)
        
        return response
class UserLoginView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print("goood")
            user = serializer.validated_data["user"]
            print(user)
            refresh = RefreshToken.for_user(user)
            user_data = {
                "id": user.id,
                "username": user.username,
            
            }
    
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": user_data,
            })
    
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)
class Forgotpassword(APIView):
    def post(self,request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(): 
            email = serializer.validated_data['email'] 

            try:
                user = User.objects.get(email=email)
                otp = user.generate_new_otp() 
                user.otp = otp
                user.save()
                  
                send_otp_email(email, otp)
                return Response({"message": "New OTP sent. Please check your email"})
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Forgototpverification(APIView):
    def post(self,request):
        serializer=ForgotOTPverificationSerializer(data=request.data)
        print("yes")
        if serializer.is_valid():
            email = serializer.validated_data['email'] 
            user=User.objects.get(email=email)
            otp=serializer.validated_data['otp']
            print("hai",email)
            print(user.otp)
            print(otp)
            if user.otp==otp:
                print("true")
                return Response({"message":"Your Otp verified"})
                
            else:
                return Response({"message":"Your otp is incorrect "})
        else:
            return Response(serializer.errors, status=400)
        
class Confirmpassword(APIView):
    def put(self, request):
        email = request.data.get('email')
        new_password = request.data.get('newPassword')
        confirm_password = request.data.get('confirmPassword')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if new_password != confirm_password:
            return Response({"message": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        
class UpdateUserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.save()
        return Response("User data updated successfully", status=status.HTTP_200_OK)
