from django.shortcuts import render, redirect
from django.http import HttpResponse
from patterns.forms import *


# Create your views here.


# The home page 
def home(request):
	return render(request, 'home.html')


# The first page to add a new pattern - after successful form submision it should redirect to adding problem and context
def add_new_pattern_name(request):
	form = NewPatternName()
	if request.method == 'POST':
		form = NewPatternName(request.POST, request.FILES)
		if form.is_valid():
			newPatternInstance = form.save(commit=False)
		
		return redirect('/newprobtext/')

	return render(request, 'new_name.html', {'form':form})


# the next page to add problem and context to a new pattern
# the template will display the just added name and picture... 
def add_new_prob_and_context(request):
	formP = NewProblem()
	formC = NewContext()
	if request.method == 'POST':
		formP = NewProblem(request.POST)
		formC = NewContext(request.POST)
		if formP.is_valid() and formC.is_valid():
			newProblemInstance = formP.save(commit=False)
			newContextInstance = formC.save(commit=False)
			newProblemInstance.parent_pattern = add_new_pattern_name.newPatternInstance.id 
			newContextInstance.partent_pattern = add_new_pattern_name.newPatternInstance.id

			newPatternInstance.save()
			newContextInstance.save()
			newProblemInstance.save()

	
		return redirect('/')
	
	return render(request, 'new_probtext.html', {'formP':formP, 'formC':formC})