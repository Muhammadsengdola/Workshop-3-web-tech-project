from django.contrib import admin
from .models import *
admin.site.register([Profile,Station,Train,TrainClass,Schedule,Seat,Booking,ContactMessage,Visitor])
