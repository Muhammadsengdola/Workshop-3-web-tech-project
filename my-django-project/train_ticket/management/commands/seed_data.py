from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from train_ticket.models import *
from datetime import date,time
class Command(BaseCommand):
 def handle(self,*a,**k):
  admin,_=User.objects.get_or_create(username='admin',defaults={'email':'admin@example.com','first_name':'System Admin','is_staff':True,'is_superuser':True}); admin.set_password('admin123'); admin.is_staff=admin.is_superuser=True; admin.save(); Profile.objects.update_or_create(user=admin,defaults={'role':'admin','phone':'0800000000'})
  user,_=User.objects.get_or_create(username='student',defaults={'email':'student@example.com','first_name':'Student'}); user.set_password('student123'); user.save(); Profile.objects.update_or_create(user=user,defaults={'role':'user','phone':'0812345678'})
  ss=[Station.objects.get_or_create(name=n,province=n)[0] for n in ['ยะลา','ปัตตานี','นราธิวาส']]; ts=[Train.objects.get_or_create(train_number=n,type=t)[0] for n,t in [('YLP-101','รถธรรมดา'),('PTN-202','รถด่วน'),('NWT-303','รถนอน')]]; [TrainClass.objects.get_or_create(name=n,price=p) for n,p in [('ธรรมดา',120),('แอร์',180),('นอน',250)]]
  rows=[(0,0,1,date(2026,9,24),time(8),time(9,30)),(1,1,2,date(2026,9,24),time(10),time(11,10)),(2,2,0,date(2026,9,24),time(13),time(14,45)),(0,0,2,date(2026,9,25),time(8),time(10)),(1,2,1,date(2026,9,25),time(11),time(12,20)),(2,1,0,date(2026,9,25),time(14),time(15,40))]
  for ti,oi,di,dt,dep,arr in rows:
   s,_=Schedule.objects.get_or_create(train=ts[ti],origin=ss[oi],destination=ss[di],travel_date=dt,defaults={'departure_time':dep,'arrival_time':arr})
   for x in 'ABCD':
    for n in range(1,6): Seat.objects.get_or_create(schedule=s,number=f'{x}{n}')
  self.stdout.write(self.style.SUCCESS('Seed complete: admin/admin123 and student/student123'))
