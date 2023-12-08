from django.urls import path 
from .views import RideCreateView,RideFilterView,Bookride,SelectedRide,UserRideDetails,UserDetail,Accept,Reject,PaymentReview,create_razorpay_order,TransactionAPIView,get_ride_details,cancel_ride,wallet,save_notification
urlpatterns = [
    path('publishride',  RideCreateView.as_view()),
    path('rideavailable',RideFilterView.as_view()),
    path('selectedride/<int:ride_id>/', SelectedRide.as_view()),
    path('ridebook',Bookride.as_view()),
    path('ridedetails',UserRideDetails.as_view()),
     path('user/<int:userid>/', UserDetail.as_view()),
    
    path('accept/<int:rideid>/', Accept.as_view(), name='accept-ride'),
    path('reject/<int:rideid>/', Reject.as_view(), name='reject-ride'),
    path('paymentreview/<int:rideid>',PaymentReview.as_view()),
    path('paymentgateway',create_razorpay_order),
    path('verifygateway',TransactionAPIView.as_view()),
    path('requestridedetail/<int:rideId>',get_ride_details),
    path('cancel_ride/<int:ride_id>/', cancel_ride),
    path('wallet',wallet),
    path('notfiy',save_notification)
    
    
    
]
