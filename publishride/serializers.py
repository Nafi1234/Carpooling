from rest_framework import serializers
from .models  import Ride,ReuquestRide,TimeData,RideChat,Payment,Wallet,Notification
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
        fields = ['username', 'email', 'first_name', 'phone_number']  

class RideSerializer(serializers.ModelSerializer):
    
    
    user_details = UserSerializer(source="user",read_only=True)
    time_detail = TimeDataSerializer(source="ride_time",read_only=True)
    class Meta:
        model = Ride
        fields=('id','user','user_details','source','destination','passengers','date','fare','ride_time','time_detail')
    
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
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wallet
        fields = "__all__"
class UserdetailSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    class Meta:
        model = User
        fields= '__all__'


class ReuquestRideSerializer(serializers.ModelSerializer):
    ride = RideSerializer()

    class Meta:
        model = ReuquestRide
        fields = '__all__'
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'content']