from django.shortcuts import render, redirect
from django.http import HttpResponse
from patterns.forms import *
from patterns.models import *


# Create your views here.


# The home page 
def home(request):
	#once we are at home page reset session vaiables for adding a new pattern
	
	request.session.flush()
	return render(request, 'home.html')


# The first page to add a new pattern - after successful form submision it should redirect to adding problem and context
def add_new_pattern_name(request):
#	form = NewPatternName()
	if request.method == 'POST':
		# check to see if we have added a pattern in this session (i.e user has clicked back on browser - if so, load that pattern to update rather than create a new one)
		# note we clear the session dictonary after the final form submission. 
		if 'new_pattern_key' in request.session:
			form = NewPatternName(request.POST, request.FILES, instance=DesignPattern.objects.get(id=request.session['new_pattern_key']))
		else: 
			form = NewPatternName(request.POST, request.FILES)
		# if form is valid save it to a new object, and store the object contents in session dictonary
		if form.is_valid():
			newPatternInstance = form.save()
			request.session['new_pattern_key'] = newPatternInstance.id
			request.session['new_pattern_name'] = newPatternInstance.name
			request.session['new_pattern_image'] = str(newPatternInstance.pictogram)

			return redirect('/newprobtext/')

		  # print form.errors
	else:
		form = NewPatternName()
	return render(request, 'new_name.html', {'form':form})


# the next page to add problem and context to a new pattern
# the template will display the recently added name and picture from the previous page... 
def add_new_prob_and_context(request):
#	formP = NewProblem()
#	formC = NewContext()
	if request.method == 'POST':
		#check to see if we have filled out this form already in this session
		if 'new_problem_id' in request.session:
			formP = NewProblem(request.POST, instance=Problem.objects.get(id=request.session['new_problem_id'])) 
		else:
			formP = NewProblem(request.POST)

		if 'new_context_id' in request.session:
			formC = NewContext(request.POST, instance=Context.objects.get(id=request.session['new_context_id']))
		else:
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
			#put the just added info into a session variable 
			request.session['new_problem_id'] = newProblemInstance.id
			request.session['new_context_id'] = newContextInstance.id

			# flush the session dictonary so adding another pattern in during the same browser session wont overwrite the one we just added...
			# this should come after the last form entry page.
		#	request.session.flush()
			del request.session['new_pattern_key']
			del request.session['new_pattern_name']
			del request.session['new_pattern_image']
			del request.session['new_problem_id']
			del request.session['new_context_id']
			
			return redirect('/')
		
		#else:
		#	print formP.errors
		#	print formC.errors
	else:
		formP = NewProblem()
		formC = NewContext()
	return render(request, 'new_probtext.html', {'formP':formP, 'formC':formC})
