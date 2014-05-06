from django.shortcuts import render
from django.http import HttpResponse
from patterns.forms import NewPatternName


# Create your views here.

def home(request):
	return render(request, 'home.html')

def add_new_pattern_name(request):
	if request.method == 'POST':
		form = NewPatternName(request.POST)
		print form
		#form.save()
		#if form.is_valid():
		#	new_name = form['name']
		#name = request.POST['name']
		#print name
	return render(request, 'new_name.html', {'form':form})