from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404,redirect,render
from .forms import RegisterForm,ContactForm
from .models import *

def is_admin(u): return bool(u and u.is_authenticated and getattr(getattr(u,'profile',None),'role',None)=='admin')
def admin_only(view):
 def w(request,*a,**kw):
  if not is_admin(request.user): messages.error(request,'Admin login required.'); return redirect('admin_login')
  return view(request,*a,**kw)
 w.__name__=view.__name__; return w

def home(request):
 Visitor.objects.create(ip_address=request.META.get('REMOTE_ADDR')); return render(request,'train_ticket/home.html',{'visitor_count':Visitor.objects.count(),'cards':[('📝 สมัครสมาชิก','ลงทะเบียนเพื่อจองตั๋วและดูประวัติการจอง','/register/','สมัคร'),('🔑 เข้าสู่ระบบ','ล็อกอินเพื่อทำรายการจอง','/login/','ล็อกอิน'),('⚙️ แอดมิน','แดชบอร์ดจัดการข้อมูล','/admin-login/','เข้าสู่ระบบแอดมิน')]})
def login_view(request):
 if request.method=='POST':
  ident=request.POST.get('username','').strip(); pwd=request.POST.get('password',''); u=authenticate(request,username=ident,password=pwd)
  if not u:
   f=User.objects.filter(email__iexact=ident).first(); u=authenticate(request,username=f.username,password=pwd) if f else None
  if u: login(request,u); return redirect('home')
  messages.error(request,'Username/email or password is incorrect.')
 return render(request,'train_ticket/login.html')
def register(request):
 f=RegisterForm(request.POST or None)
 if request.method=='POST' and f.is_valid():
  u=f.save(commit=False); u.set_password(f.cleaned_data['password']); u.save(); Profile.objects.create(user=u,phone=f.cleaned_data['phone']); messages.success(request,'Registration successful.'); return redirect('login')
 return render(request,'train_ticket/register.html',{'form':f})
def logout_view(request): logout(request); return redirect('home')
def search(request):
 qs=Schedule.objects.select_related('train','origin','destination').all(); o=request.GET.get('origin',''); d=request.GET.get('destination',''); dt=request.GET.get('date','')
 if o: qs=qs.filter(origin_id=o)
 if d: qs=qs.filter(destination_id=d)
 if dt: qs=qs.filter(travel_date=dt)
 return render(request,'train_ticket/search.html',{'schedules':qs,'stations':Station.objects.all(),'classes':TrainClass.objects.all(),'o':o,'d':d,'dt':dt})
@login_required
def seat_selection(request,schedule_id,class_id):
 s=get_object_or_404(Schedule.objects.select_related('train','origin','destination'),pk=schedule_id); c=get_object_or_404(TrainClass,pk=class_id)
 if request.method=='POST':
  with transaction.atomic():
   seat=Seat.objects.select_for_update().filter(pk=request.POST.get('seat_id'),schedule=s).first()
   if not seat or seat.is_booked: messages.error(request,'Seat is already booked.')
   else:
    Booking.objects.create(user=request.user,schedule=s,seat=seat,ticket_class=c,price=c.price,status='Confirmed'); seat.is_booked=True; seat.booked_by=request.user; seat.save(); messages.success(request,'Booking successful.'); return redirect('my_bookings')
 return render(request,'train_ticket/seat_selection.html',{'schedule':s,'ticket_class':c,'seats':s.seats.all()})
@login_required
def my_bookings(request): return render(request,'train_ticket/my_bookings.html',{'bookings':request.user.bookings.select_related('schedule__train','schedule__origin','schedule__destination','seat','ticket_class')})
def contact(request):
 f=ContactForm(request.POST or None)
 if request.method=='POST' and f.is_valid(): f.save(); messages.success(request,'Message sent successfully.'); return redirect('contact')
 return render(request,'train_ticket/contact.html',{'form':f})
def admin_login(request):
 if request.method=='POST':
  u=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
  if is_admin(u): login(request,u); return redirect('dashboard')
  messages.error(request,'Invalid admin credentials.')
 return render(request,'train_ticket/admin_login.html')
@admin_only
def dashboard(request): return render(request,'train_ticket/dashboard.html',{'counts':[('Users',User.objects.count()),('Trains',Train.objects.count()),('Stations',Station.objects.count()),('Schedules',Schedule.objects.count()),('Bookings',Booking.objects.count()),('Messages',ContactMessage.objects.count())]})
@admin_only
def admin_bookings(request):
 if request.GET.get('delete'):
  b=get_object_or_404(Booking,pk=request.GET['delete']); b.seat.is_booked=False; b.seat.booked_by=None; b.seat.save(); b.delete(); return redirect('admin_bookings')
 return render(request,'train_ticket/admin_bookings.html',{'bookings':Booking.objects.select_related('user','schedule__train','schedule__origin','schedule__destination','seat','ticket_class')})
@admin_only
def admin_users(request): return render(request,'train_ticket/admin_users.html',{'users':User.objects.select_related('profile')})
def crud(request,model,template,fields,extra=None):
 obj=get_object_or_404(model,pk=request.GET['edit']) if request.GET.get('edit') else None
 if request.GET.get('delete'): get_object_or_404(model,pk=request.GET['delete']).delete(); return redirect(request.resolver_match.url_name)
 if request.method=='POST':
  obj=get_object_or_404(model,pk=request.POST['id']) if request.POST.get('id') else model()
  for f in fields: setattr(obj,f,request.POST.get(f))
  obj.save(); return redirect(request.resolver_match.url_name)
 ctx={'objects':model.objects.all(),'edit':obj}; ctx.update(extra() if extra else {}); return render(request,template,ctx)
@admin_only
def admin_trains(request): return crud(request,Train,'train_ticket/admin_trains.html',['train_number','type'])
@admin_only
def admin_stations(request): return crud(request,Station,'train_ticket/admin_stations.html',['name','province'])
@admin_only
def admin_classes(request): return crud(request,TrainClass,'train_ticket/admin_classes.html',['name','price'])
@admin_only
def admin_schedules(request): return crud(request,Schedule,'train_ticket/admin_schedules.html',['train_id','origin_id','destination_id','travel_date','departure_time','arrival_time'],lambda:{'trains':Train.objects.all(),'stations':Station.objects.all()})
