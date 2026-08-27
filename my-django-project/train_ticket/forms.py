from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage
class RegisterForm(forms.ModelForm):
 password=forms.CharField(widget=forms.PasswordInput,min_length=6); password2=forms.CharField(widget=forms.PasswordInput,label='Confirm password'); phone=forms.CharField(max_length=20)
 class Meta: model=User; fields=['username','email','first_name']
 def clean(self):
  d=super().clean()
  if d.get('password')!=d.get('password2'): raise forms.ValidationError('Passwords do not match.')
  if User.objects.filter(email=d.get('email')).exists(): raise forms.ValidationError('Email is already registered.')
  return d
class ContactForm(forms.ModelForm):
 class Meta: model=ContactMessage; fields=['name','email','subject','message']
