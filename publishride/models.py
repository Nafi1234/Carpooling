from django.db import models
from user.models import User

from django.utils import timezone

class TimeData(models.Model):
    hours = models.CharField(max_length=5)
    minutes = models.CharField(max_length=5)
    period = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.hours}:{self.minutes} {self.period}"

class Ride(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    source_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    source_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    passengers = models.PositiveIntegerField()
    date = models.DateField() 
    ride_time = models.ForeignKey(TimeData, on_delete=models.CASCADE)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=20)
    

    def __str__(self):
        return f"Ride from {self.source} to {self.destination}"
class ReuquestRide(models.Model):
    request_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reuested_rides')
    ride  = models.ForeignKey(Ride, on_delete=models.CASCADE,related_name='ride_requests')
    passenger_count=models.IntegerField(max_length=5)
    REQUEST_STATUS_CHOICES =(
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ) 
    request_status = models.CharField(max_length=10,choices=REQUEST_STATUS_CHOICES)
    payment_status = models.CharField(
        max_length=10,
        choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')],
        default='unpaid'
    )
    def __str__(self):
        return f"Request for ride from {self.ride.source} to {self.ride.destination}" 
class Payment(models.Model):
    ride_request = models.OneToOneField('ReuquestRide', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.BooleanField(default=False)  # Change to BooleanField
    payment_id = models.CharField( verbose_name="Payment ID")
    order_id = models.CharField( verbose_name="Order ID")
    signature = models.CharField( verbose_name="Signature", blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self):
        return f"Payment #{self.id} for RideRequest #{self.ride_request.id}"
class RideChat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ride_chats')

    def __str__(self):
        return f'{self.sender.username} - {self.content}'