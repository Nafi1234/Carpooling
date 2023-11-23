from rest_framework import serializers
from .models  import Ride,ReuquestRide,TimeData,RideChat,Payment
from user.models import User



class TimeDataSerializer(serializers.ModelSerializer):
    formatted_time = serializers.SerializerMethodField()

    def get_formatted_time(self, obj):
        return f"{obj.hours}:{obj.minutes} {obj.period}"

    class Meta:
        model = TimeData
        fields = ['formatted_time']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'phone_number']  # Include other fields as needed

class RideSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    ride_time = TimeDataSerializer()

    class Meta:
        model = Ride
        fields = ['id', 'user_name', 'source', 'first_name', 'phone_number', 'destination', 'source_latitude', 'source_longitude', 'destination_latitude', 'destination_longitude', 'passengers', 'date', 'ride_time', 'fare', 'vehicle_name', 'registration_number', 'landmark']

class RequestRideSerializer(serializers.ModelSerializer):
    ride_details = RideSerializer(source='ride', read_only=True)
    request_user_details = UserSerializer(source='request_user', read_only=True)

    class Meta:
        model = ReuquestRide
        fields = ['id', 'request_user', 'request_user_details', 'ride', 'ride_details', 'passenger_count', 'request_status','payment_status']
        
class RideChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideChat
        fields = ['id', 'content', 'timestamp', 'sender_user', 'ride']
class UserdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= '__all__'
class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class ReuquestRideSerializer(serializers.ModelSerializer):
    ride = RideSerializer()

    class Meta:
        model = ReuquestRide
        fields = '__all__'
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'