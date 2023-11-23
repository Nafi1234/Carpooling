from rest_framework import serializers
from .models import  User
from django.utils import timezone
import re
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    confirm_password= serializers.CharField(write_only=True)
    class Meta:
        model= User
        fields=("id","first_name","last_name","email","password","phone_number","confirm_password")
        extra_kwargs ={
            'password':{'write_only':True}
        }
        
    def validate_password(self,value):
        if len(value)<6:
            raise serializers.ValidationError("password must have at least 6 character")
        if not any(char.isupper() for char in value):
             raise serializers.ValidationError("Password must contain at least one Upper Case")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    def validate_first_name(self,value):
        print("here print",value)
        if not value.isalpha():
            raise serializers.ValidationError("First name should only contain character ")
        return value
    def validate_last_name(self,value):
        if not value.isalpha():
            raise serializers.ValidationError("last name should only contain character ")
        return value
    def validate_phone_number(self,value):
        print("phone_number",value)
        if not re.match(r'^\d{10}$', value):
            raise serializers.ValidationError("Phone number must have exactly 10 digits.")
        return value
    def validate_email(self,value):
        if '@' not in value or '.' not in value:
            raise serializers.ValidationError("Invalid email format")  
        return value
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data


        
    def create(self, validated_data):
        print("series",validated_data)
        validated_data.pop('confirm_password', None)
        username = validated_data.get('email')
        user = User.objects.create(
        first_name=validated_data.get('first_name'),
        last_name=validated_data.get('last_name'),
        username=username,
        email=validated_data.get('email'),
    
        phone_number=validated_data.get('phone_number'),
    )  
        user.set_password(validated_data.get('password'))
        user.save()
        return user
        
   
class OTPverificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)
    email=serializers.EmailField()
class ForgotOTPverificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)
    email=serializers.EmailField()
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password=serializers.CharField()
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)
            if user is not None and user.is_active: 
                data["user"] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        return data
    
    
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']
class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
class VerifySerializer(serializers.Serializer):
    otp=serializers.CharField(max_length=4)
    email=serializers.EmailField()
class ConfirmpasswordSerializer(serializers.ModelSerializer):
    confirm_password =serializers.CharField(write_only=True)
    class Meta:
        model =User
        fields = ('email','password','confirm_password')
        extra_kwargs ={
            'password':{'write_only':True}
        }
        def  validate_password(self,value):
            if len(value)<6:
                raise serializers.ValidationError("password must have at least 6 character")
            if not any(char.isupper() for char in value):
                raise serializers.ValidationError("Their should have atleast one Capital")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                raise serializers.ValidationError("Password must contain at least one special character.")
            return value
        def validate(self,data):
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError('Passwod and confirm pass not mathced')
        def create(self ,validated_data):
            email = validated_data.get('email')
            user=User.objects.get(email=email)
        
            password=validated_data.get('password')
            user.set_password(password)
            user.save()
            return user