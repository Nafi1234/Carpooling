from rest_framework import generics
from .models import Ride,TimeData,ReuquestRide,Wallet
from user.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import RideSerializer,RequestRideSerializer,UserdetailSerializer,ReuquestRideSerializer,TransactionSerializer,WalletSerializer,NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime
import json
from django.db.models import  Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
import razorpay
from rest_framework.decorators import permission_classes
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from .main import RazorpayClient
from datetime import date

rz_client = RazorpayClient()
class RideCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
    
        data = request.data
        user = request.user  

        vehicle_name = data.get('Vechiclename')
        
        registration_number = data.get('Registrationno')
        date_str = data.get('date')
        date = datetime.fromisoformat(date_str).date()
        pickup_location = data.get('pickupLocation')
        dropoff_location = data.get('dropoffLocation')
        price = data.get('Fare')
        time = data.get('time')
    
        passenger = data.get('passenger')

        hours_minutes = time.get("minutes")
        hours = time.get("hours")

        period = "pm"


        time_data, _ = TimeData.objects.get_or_create(
            hours=hours,
            minutes=hours_minutes,
            period=period
        )
        
        source = pickup_location.get('name')
        source_latitude = pickup_location['coordinates']['latitude']
        source_longitude = pickup_location['coordinates']['longitude']    
        destination = dropoff_location.get('name')
        destination_latitude = dropoff_location['coordinates']['latitude']
        destination_longitude = dropoff_location['coordinates']['longitude']
        existing_ride = Ride.objects.filter(
            user=user,
            date=date
        ).first()

        if existing_ride:
            return Response({"message": "You have already published a ride for this date.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        ride = Ride(
            user=user,  
            vehicle_name=vehicle_name,
            registration_number=registration_number,
            date=date,
            source=source,
            source_latitude=source_latitude,
            source_longitude=source_longitude,
            destination=destination,
            destination_latitude=destination_latitude,
            destination_longitude=destination_longitude,
            fare=price,
            ride_time=time_data,
            passengers=passenger
        )
        ride.save()

        return Response({"message": "Ride published successfully.", "success": True}, status=status.HTTP_201_CREATED)

class RideFilterView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)

            source = data.get("leavingFrom")
            destination = data.get("goingto")
            date_str = data.get('date')
            passengers = int(data.get('passengers'))
        

            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
    
            except ValueError:
                return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        
            
            destinations = Ride.objects.filter(
                passengers__gte=passengers,
                date=date,
                source=source,
                destination=destination
            )
    
            if destinations.exists():
                for destination in destinations:
                    print(destination)

        
            if not destinations:
                return Response({"error": "No rides available matching your criteria"})

    
            serializer = RideSerializer(destinations, many=True, context={'request': request})
        
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            
    
            return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)
class SelectedRide(APIView):
    def get(self, request, ride_id):
    
        try:
        
            ride = get_object_or_404(Ride, id=ride_id)
            
        
            serializer = RideSerializer(ride)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Ride.DoesNotExist:
            return Response({"message": "Ride not found for the specified ID."}, status=status.HTTP_404_NOT_FOUND)
class Bookride(APIView):
    permission_classes = [IsAuthenticated]
    def post (self,request):
        ride_id = request.data.get('rideId')
        passenger_count=request.data.get('count')
        user_id = request.user.id
    

        request_ride = ReuquestRide.objects.create(
            request_user_id=user_id,
            ride_id=ride_id,
            request_status='pending',
            passenger_count=passenger_count
        )




        return Response({'message': 'Ride request created successfully'}, status=status.HTTP_201_CREATED)
class UserRideDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        current_date = date.today()

        published_rides = Ride.objects.filter(user=user_id,date__gte=current_date)
    
        published_rides_serializer = RideSerializer(published_rides, many=True)
        requested_rides_matching_published = ReuquestRide.objects.filter(ride__in=published_rides)
    
        requested_rides_matching_published_serializer = RequestRideSerializer(requested_rides_matching_published, many=True)
        requested_rides_for_user = ReuquestRide.objects.filter(request_user=user_id,request_date__gte=current_date)
        requested_rides_for_user_serializer = RequestRideSerializer(requested_rides_for_user, many=True)

        response_data = {}

        if published_rides.exists():
            response_data['published_rides'] = published_rides_serializer.data

        if requested_rides_matching_published.exists():
            response_data['requested_rides_matching_published'] = requested_rides_matching_published_serializer.data

        if requested_rides_for_user.exists():
            response_data['requested_rides_for_user'] = requested_rides_for_user_serializer.data

        if published_rides.exists() or requested_rides_matching_published.exists() or requested_rides_for_user.exists():
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No rides available.'}, status=status.HTTP_404_NOT_FOUND)
class UserDetail(APIView):

    def get(self, request, userid):
        
        try:
            
            user_instance = User.objects.get(id=userid)
            
            
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserdetailSerializer(user_instance)
    
        return Response(serializer.data)
class Accept(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,rideid):
        accept=Ride.objects.get(id=rideid)
        accept.request_status='Approved'
        return Response({"message":"successfully approved"})
class Reject(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, rideid):
        reject = ReuquestRide.objects.get(id=rideid)
        reject.request_status = 'Rejected'
        reject.save()
        return Response({"message": "Successfully rejected"})
class Accept(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, rideid):
        accept = ReuquestRide.objects.get(id=rideid)
    
        Ridecount = Ride.objects.get(id=accept.ride_id)
    
        Ridecount.passengers = Ridecount.passengers - accept.passenger_count
        Ridecount.save()
        
        if accept.request_status != 'Approved':
            accept.request_status = 'Approved'
            accept.save() 
            channel_layer = get_channel_layer()
            ride_channel_name = f'ride_{accept.ride_id}'
            async_to_sync(channel_layer.group_send)(
                ride_channel_name,
                {
                    'type': 'ride.approved',
                    'message': 'Driver has accepted the ride!',
                }
            ) 
            return Response({"message": "Successfully approved"})
        else:
            return Response({"message": "Request is already approved"})
class PaymentReview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, rideid):
        try:
            
            payment_request = ReuquestRide.objects.get(id=rideid)
        except ReuquestRide.DoesNotExist:
            return Response({"error": "Payment request not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReuquestRideSerializer(payment_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
def create_razorpay_order(request):

    request_id=request.data.get("id")


    ride_request = get_object_or_404(ReuquestRide, pk=request_id)

    ride = get_object_or_404(Ride, id=ride_request.ride_id)

    client = razorpay.Client(auth=('rzp_test_TpsHVKhrkZuIUJ', 'OJzAGp6Vqx8yu2qgeHhz4y3o'))

    order_amount = int(ride.fare )*100
    order_currency = 'INR'

    order_params = { 
        'amount': order_amount,
        'currency': order_currency,
        'payment_capture': '1',
    }

    razorpay_order = client.order.create(order_params)
    order_id = razorpay_order['id']


    return Response({'order_id': order_id, 'order_amount': order_amount})


class TransactionAPIView(APIView):
    
    def post(self, request):
        
        ridid=request.data.get("ride_request")
    
        transaction_serializer = TransactionSerializer(data=request.data)
        if transaction_serializer.is_valid():
            

            ride=ReuquestRide.objects.get(id=ridid)
            ride.payment_status="Paid"
            ride.save()
            
            rz_client.verify_payment_signature(
                razorpay_payment_id = transaction_serializer.validated_data.get("payment_id"),
                razorpay_order_id = transaction_serializer.validated_data.get("order_id"),
                razorpay_signature = transaction_serializer.validated_data.get("signature")
            )
            transaction_serializer.save()
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction created"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
    
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ride_details(request,rideId):
    try:
    
        Ridedetails=ReuquestRide.objects.get(id=rideId)
        
        serializer=ReuquestRideSerializer(Ridedetails)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except ReuquestRide.DoesNotExist:
        return Response({"detail": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_ride(request, ride_id):
    try:
    
        request_ride = ReuquestRide.objects.get(id=ride_id, request_user=request.user)
    
    
        ride = request_ride.ride  
    
    
        ride.passengers += request_ride.passenger_count  
    
    
    except ReuquestRide.DoesNotExist:

        pass
    if request_ride.payment_status == 'Paid':
        
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += ride.fare
        wallet.save()

      
        wallet.save()
        request_ride.delete()

        return Response({"message": f"Ride cancelled successfully. Your paid amount of {ride.fare} has been credited to your wallet."})
    else:
        ride.delete()
        return Response({"message": "Ride cancelled successfully."})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet(request):
    wallet = Wallet.objects.get(user_id=request.user)
    serializer = WalletSerializer(wallet)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)