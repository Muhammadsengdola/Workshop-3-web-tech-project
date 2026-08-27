from django.contrib.auth.models import User
from django.db import models
class Profile(models.Model):
 user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile'); phone=models.CharField(max_length=20,blank=True); role=models.CharField(max_length=10,choices=[('user','User'),('admin','Admin')],default='user')
class Station(models.Model):
 name=models.CharField(max_length=100); province=models.CharField(max_length=100)
 def __str__(self): return self.name
class Train(models.Model):
 train_number=models.CharField(max_length=50); type=models.CharField(max_length=50)
 def __str__(self): return self.train_number
class TrainClass(models.Model):
 name=models.CharField(max_length=50); price=models.DecimalField(max_digits=10,decimal_places=2)
 def __str__(self): return self.name
class Schedule(models.Model):
 train=models.ForeignKey(Train,on_delete=models.CASCADE); origin=models.ForeignKey(Station,on_delete=models.PROTECT,related_name='departures'); destination=models.ForeignKey(Station,on_delete=models.PROTECT,related_name='arrivals'); travel_date=models.DateField(); departure_time=models.TimeField(); arrival_time=models.TimeField()
class Seat(models.Model):
 schedule=models.ForeignKey(Schedule,on_delete=models.CASCADE,related_name='seats'); number=models.CharField(max_length=5); is_booked=models.BooleanField(default=False); booked_by=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='booked_seats')
 class Meta: constraints=[models.UniqueConstraint(fields=['schedule','number'],name='unique_schedule_seat')]
class Booking(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookings'); schedule=models.ForeignKey(Schedule,on_delete=models.CASCADE,related_name='bookings'); seat=models.ForeignKey(Seat,on_delete=models.PROTECT,related_name='bookings'); ticket_class=models.ForeignKey(TrainClass,on_delete=models.PROTECT); price=models.DecimalField(max_digits=10,decimal_places=2); booking_date=models.DateTimeField(auto_now_add=True); status=models.CharField(max_length=20,choices=[('Pending','Pending'),('Confirmed','Confirmed'),('Cancelled','Cancelled')],default='Pending')
class ContactMessage(models.Model):
 name=models.CharField(max_length=100); email=models.EmailField(); subject=models.CharField(max_length=200,blank=True); message=models.TextField(); created_at=models.DateTimeField(auto_now_add=True)
class Visitor(models.Model):
 ip_address=models.GenericIPAddressField(null=True,blank=True); visit_time=models.DateTimeField(auto_now_add=True)
