from rest_framework import generics
from .models import Ride,TimeData,ReuquestRide
from user.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import RideSerializer,RequestRideSerializer,UserdetailSerializer,ReuquestRideSerializer,TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from datetime import datetime
import json
from django.db.models import  Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
import razorpay
from .main import RazorpayClient
from datetime import date

rz_client = RazorpayClient()
class RideCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.data)
        data = request.data
        user = request.user  

        vehicle_name = data.get('Vechiclename')
        print(vehicle_name)
        registration_number = data.get('Registrationno')
        date_str = data.get('date')
        date = datetime.fromisoformat(date_str).date()
        pickup_location = data.get('pickupLocation')
        dropoff_location = data.get('dropoffLocation')
        price = data.get('Fare')
        time = data.get('time')
        print("Here geting the time",time)
        passenger = data.get('passenger')

        hours_minutes = time.get("minutes")
        hours = time.get("hours")

        period = "pm"
        print("getting minutes",hours_minutes)
        print("gettin_hours",hours)

        time_data, _ = TimeData.objects.get_or_create(
            hours=hours,
            minutes=hours_minutes,
            period=period
        )
        print("here geting pickup",pickup_location)
        source = pickup_location.get('name')
        source_latitude = pickup_location['coordinates']['latitude']
        source_longitude = pickup_location['coordinates']['longitude']    
        destination = dropoff_location.get('name')
        destination_latitude = dropoff_location['coordinates']['latitude']
        destination_longitude = dropoff_location['coordinates']['longitude']

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
            print(source)
            print(destination)

            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                print(date)
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
          
            else:
                print("empty")
            if not destinations:
                return Response({"error": "No rides available matching your criteria"})

    
            serializer = RideSerializer(destinations, many=True, context={'request': request})
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            
            print(f"Error in RideFilterView: {str(e)}")
            return Response({"error": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST)
class SelectedRide(APIView):
    def get(self, request, ride_id):
        print("here",ride_id)
        try:
            print(ride_id)
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
        print(user_id)

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
        print(user_id)
        published_rides = Ride.objects.filter(user=user_id,date__gte=current_date)
        print("here givig the published",published_rides)
        published_rides_serializer = RideSerializer(published_rides, many=True)

    
        requested_rides_matching_published = ReuquestRide.objects.filter(ride__in=published_rides)
        print("here giving the request_rides_matching_published",requested_rides_matching_published)
        requested_rides_matching_published_serializer = RequestRideSerializer(requested_rides_matching_published, many=True)
        requested_rides_for_user = ReuquestRide.objects.filter(request_user=user_id,date__gte=current_date)
        print("here giving the request",requested_rides_for_user)
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
        print(userid)
        try:
            
            user_instance = User.objects.get(id=userid)
            print("arya",user_instance)
            
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserdetailSerializer(user_instance)
        print(serializer)
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
        print(rideid)
        accept = ReuquestRide.objects.get(id=rideid)
        if accept.request_status != 'Approved':
            accept.request_status = 'Approved'
            accept.save() 
            return Response({"message": "Successfully approved"})
        else:
            return Response({"message": "Request is already approved"})
class PaymentReview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, rideid):
        print("here",rideid)
        try:
            
            payment_request = ReuquestRide.objects.get(id=rideid)
        except ReuquestRide.DoesNotExist:
            return Response({"error": "Payment request not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReuquestRideSerializer(payment_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
def create_razorpay_order(request):
    print(request.data)
    request_id=request.data.get("id")
    print(request_id)

    ride_request = get_object_or_404(ReuquestRide, pk=request_id)
    print(ride_request)
    ride = get_object_or_404(Ride, id=ride_request.ride_id)

    client = razorpay.Client(auth=('rzp_test_TpsHVKhrkZuIUJ', 'OJzAGp6Vqx8yu2qgeHhz4y3o'))

    order_amount = int(ride.fare )
    order_currency = 'INR'

    order_params = { 
        'amount': order_amount,
        'currency': order_currency,
        'payment_capture': '1',
    }

    razorpay_order = client.order.create(order_params)
    order_id = razorpay_order['id']
    print("razopay",razorpay_order)

    return Response({'order_id': order_id, 'order_amount': order_amount})


class TransactionAPIView(APIView):
    
    def post(self, request):
        transaction_serializer = TransactionSerializer(data=request.data)
        if transaction_serializer.is_valid():
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