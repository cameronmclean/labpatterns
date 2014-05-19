from django.shortcuts import render, redirect
from django.http import HttpResponse
from patterns.forms import *
from django.forms.models import modelformset_factory
from patterns.models import *
from django.views.decorators.cache import cache_control
from patterns import thesaurus3


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

	
			
			return redirect('/newforce/')
		
		#else:
		#	print formP.errors
		#	print formC.errors
	else:
		formP = NewProblem()
		formC = NewContext()
	return render(request, 'new_probtext.html', {'formP':formP, 'formC':formC})


#@cache_control(no_cache=True, must_revalidate=True) - no longer needed - solved via template <body onunload="">
def add_new_force(request):
	ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False)
	data = {
		'form-TOTAL_FORMS': '1',
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	if request.method == 'POST' :

		if 'forces_added' in request.session:
			ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False, extra=0)
			data['form-TOTAL_FORMS'] = Force.objects.filter(parent_pattern=request.session['new_pattern_key']).count()
			initialForms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
			print data['form-TOTAL_FORMS']
			print initialForms
			formset = ForceFormSet(request.POST, request.FILES, data, queryset=initialForms)
		

		else:
			formset = ForceFormSet(request.POST, request.FILES, data, queryset=Force.objects.none())
		
		if formset.is_valid():
			for form in formset.forms:
				newInstance = form.save(commit=False)
				newInstance.parent_pattern = DesignPattern.objects.get(id=request.session['new_pattern_key'])
		#		print dir(newInstance)
		#		print newInstance.description
		#		print newInstance.parent_pattern_id
				newInstance.save()	
								
			request.session['forces_added'] = True

			return redirect('/newsolutionale/')
	else: 
		if 'forces_added' in request.session:
			ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False, extra=0) # dont display extra forms if user hits back button
			data['form-TOTAL_FORMS'] = Force.objects.filter(parent_pattern=request.session['new_pattern_key']).count()
			initialForms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
			print data['form-TOTAL_FORMS']
			print initialForms
			formset = ForceFormSet(queryset=initialForms)
		
		else:
			formset = ForceFormSet(queryset=Force.objects.none())

	return render(request, 'new_force.html', {'formset': formset})




def add_new_solution(request):
	if request.method == 'POST':
		#check to see if we have filled out this form already in this session
		if 'new_solution_id' in request.session:
			formS = NewSolution(request.POST, instance=Solution.objects.get(id=request.session['new_solution_id'])) 
		else:
			formS = NewSolution(request.POST)

		if 'new_rationale_id' in request.session:
			formR = NewRationale(request.POST, instance=Rationale.objects.get(id=request.session['new_ratioanle_id']))
		else:
			formR = NewRationale(request.POST)


		if formS.is_valid() and formR.is_valid():
			# save form to object
			newSolutionInstance = formS.save(commit=False)
			newRationaleInstance = formR.save(commit=False)
			# give the object the last created pattern ID key
			newSolutionInstance.parent_pattern = DesignPattern.objects.get(id = request.session['new_pattern_key'])
			newRationaleInstance.parent_pattern = DesignPattern.objects.get(id = request.session['new_pattern_key'])


			# save the objects into the db
			newSolutionInstance.save()
			newRationaleInstance.save()


			#put the just added info into a session variable 
			request.session['new_solution_id'] = newSolutionInstance.id
			request.session['new_rationale_id'] = newRationaleInstance.id
		
			
			return redirect('/related/')

	else:
		formS = NewSolution()
		formR = NewRationale()


	return render(request, 'new_solutionale.html', {'formS':formS, 'formR':formR})


def see_related_terms(request):

	#chcek to see if we have loaded words already

	if not 'wordlist' in request.session:
		# get all the force objects for the current pattern
		terms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
		#terms = Force.objects.filter(parent_pattern=32)
		#creat a dict to store a list of terms for each pattern force
		related_force_terms = {}
		tempWordlist = []
		for name in terms:
			tempWordlist = thesaurus3.get_all(name.name) # parses the force name by space delim and returns the aggregate of all the related words
			related_force_terms[name.name] = tempWordlist # store the force name and list of related terms in the dict

			#save the related terms in the db
			for aword in tempWordlist:
				wordToSave = RelatedWord(force=Force.objects.get(name=name.name), word=aword)
				wordToSave.save()

			request.session['wordlist'] = True # this doesnt need to get set every time through the for loop, but can be anywhre inside the first if..
		

	#print related_force_terms.keys()
	#print thesaurus3.get_all('test')
	#print type(wordlist)

	#create a list to store the selected words
	listToKeep = []
	if request.method == "POST":

		listToKeep = request.POST.getlist('checks')
		for item in listToKeep:
			print item
		
		#load all the words again based on t
		wordsToDelete = RelatedWord.objects.filter(force=(Force.objects.filter(parent_pattern=request.session['new_pattern_key'])))
		#loop through all the related words in this session, if its not on the list - delete it.
		
		for thing in wordsToDelete:
			if thing.word not in listToKeep:
				thing.delete()
	

		
		# flush the session dictonary so adding another pattern in during the same browser session wont overwrite the one we just added...
		# this should come after the last form entry page.
		#	request.session.flush()			
		del request.session['new_pattern_key']
		del request.session['new_pattern_name']
		del request.session['new_pattern_image']
		del request.session['new_problem_id']
		del request.session['new_context_id']
		#	del request.session['new_force_id']
		del request.session['forces_added']
		del request.session['new_solution_id']
		del request.session['new_rationale_id']
	
		del request.session['wordlist']
		
		return redirect('/')


	return render(request, 'see_related.html', {'related_force_terms':related_force_terms})

