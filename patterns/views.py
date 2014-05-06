from django.shortcuts import render, redirect
from django.http import HttpResponse
from patterns.forms import NewPatternName


# Create your views here.

def home(request):
	return render(request, 'home.html')

def add_new_pattern_name(request):
	form = NewPatternName()
	if request.method == 'POST':
		form = NewPatternName(request.POST)
		if form.is_valid():
			# model ImageField and modelForms field are causing validation errors. Need to declare the right type.. 
			form.save()
		
		return redirect('/')

	return render(request, 'new_name.html', {'form':form})