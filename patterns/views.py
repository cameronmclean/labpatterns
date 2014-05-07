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
		# if form is valid save it to a new object, and store the object contents in session dictonary
		if form.is_valid():
			newPatternInstance = form.save()
			request.session['new_pattern_key'] = newPatternInstance.id
			request.session['new_pattern_name'] = newPatternInstance.name
			request.session['new_pattern_image'] = str(newPatternInstance.pictogram)

			return redirect('/newprobtext/')
		else:
			print form.errors
	else:
		form = NewPatternName()
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
			# save form to object
			newProblemInstance = formP.save(commit=False)
			newContextInstance = formC.save(commit=False)
			# give the object the last created pattern ID key
			newProblemInstance.parent_pattern = DesignPattern.objects.get(id = request.session['new_pattern_key'])
			newContextInstance.parent_pattern = DesignPattern.objects.get(id = request.session['new_pattern_key'])
			# save the objects into the db
			newProblemInstance.save()
			newContextInstance.save()	
			
			return redirect('/')
		else:
			print formP.errors
			print formC.errors
	else:
		formP = NewProblem()
		formC = NewContext()
	return render(request, 'new_probtext.html', {'formP':formP, 'formC':formC})
