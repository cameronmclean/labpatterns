from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
	return render(request, 'home.html')

def add_new_pattern(request):
	return render(request, 'new.html')