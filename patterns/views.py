from django.shortcuts import render, redirect
from django.http import HttpResponse
from patterns.forms import *
from django.forms.models import modelformset_factory
from patterns.models import *
from django.views.decorators.cache import cache_control
from patterns import thesaurus3, class_lookup
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

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
		# check to see if we have added a pattern in this session (i.e user has clicked back on browser 
		# - if so, load that pattern to update rather than create a new one)
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
		#check to see if we have filled out this form already in this session - if so, populate the from with that instance
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
		
	
	else:
		formP = NewProblem()
		formC = NewContext()
	return render(request, 'new_probtext.html', {'formP':formP, 'formC':formC})


#@cache_control(no_cache=True, must_revalidate=True)
## - decorator no longer needed - trying to force page reload on browser back solved via template <body onunload="">
def add_new_force(request):
	ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False)
	data = {
		'form-TOTAL_FORMS': '1',
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	if request.method == 'POST' :

		# check to see if we have added forces already - if so get all the current forces and use them as the initial queryset
		# we also need to set data 'form-INITIAL_FORMS' value to the number of forces/forms in the queryset
		if 'forces_added' in request.session:
			ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False, extra=0)
			data['form-TOTAL_FORMS'] = Force.objects.filter(parent_pattern=request.session['new_pattern_key']).count()
			initialForms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
			# print data['form-TOTAL_FORMS']
			# print initialForms
			formset = ForceFormSet(request.POST, request.FILES, data, queryset=initialForms)
		
		# is we havent added forces yet - start with one blank form.	
		else:
			formset = ForceFormSet(request.POST, request.FILES, data, queryset=Force.objects.none())
		
		# validate forms and then save upon POST.
		if formset.is_valid():
			# for each form 
			for form in formset.forms:
				newInstance = form.save(commit=False)
				# add foreign key from session variable
				newInstance.parent_pattern = DesignPattern.objects.get(id=request.session['new_pattern_key'])
				# save each force to db
				newInstance.save()	
			# after saving all forces, set session variable to flag we have added forces								
			request.session['forces_added'] = True

	
			return redirect('/newsolutionale/')
	
	# if we are not POSTing - i.e we GETing - check to see if it forst time or browser back/reload
	else: 
		if 'forces_added' in request.session:
			# if yes - populate the session forces 
			ForceFormSet = modelformset_factory(Force, form=NewForce, can_delete=False, extra=0) # extra=0 causes dont display extra forms
																								 # if user hits back button - if there is a blank form,
																								 # user must enter a Null force or populate another one 
																								 #- they may not want to do this.
			data['form-TOTAL_FORMS'] = Force.objects.filter(parent_pattern=request.session['new_pattern_key']).count()
			initialForms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
			formset = ForceFormSet(queryset=initialForms)
		
		# otherwise this is the first time to add forces - load empty form 
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
			formR = NewRationale(request.POST, instance=Rationale.objects.get(id=request.session['new_rationale_id']))
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
		
			# redirect to select related terms NOTE - we havnt addded references yet...
			return redirect('/related/')

	else:
		formS = NewSolution()
		formR = NewRationale()


	return render(request, 'new_solutionale.html', {'formS':formS, 'formR':formR})


def add_supporting(request):
	#
	# In this view we should add a diagram, references, and create links to related patterns..
	#

	# On browser back - use modelforms to handle updates...???

	RelationFormSet = modelformset_factory(PatternRelation, form=SetPatternRelation, can_delete=False)
	data = {
		'form-TOTAL_FORMS': '1',
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}



	if request.method == 'POST':
		#and we have been to this page before
		if 'new_diagram_id' in request.session:
			#fetch the previous diagram input
			formD = NewDiagram(request.POST, request.FILES, instance=Diagram.objects.get(id = request.session['new_diagram_id'])) 
			#fetch the previous pattern relation input
			RelationFormSet = modelformset_factory(PatternRelation, form=SetPatternRelation, can_delete=False, extra=0) # extra=0 causes dont display extra forms
																								 # if user hits back button - if there is a blank form,
																								 # user must enter a Null force or populate another one 
																								 #- they may not want to do this.
			data['form-TOTAL_FORMS'] = PatternRelation.objects.filter(subject_pattern=request.session['new_pattern_key']).count()
			initialForms = PatternRelation.objects.filter(subject_pattern=request.session['new_pattern_key'])
			formset = RelationFormSet(data, queryset=initialForms)


		# if this is our first POST
		else:
			formD = NewDiagram(request.POST, request.FILES)
			formset = RelationFormSet(request.POST, data, queryset=PatternRelation.objects.none())

		if formD.is_valid() and formset.is_valid():
			newDiagramInstance = formD.save(commit=False)
			newDiagramInstance.parent_pattern = DesignPattern.objects.get(id = request.session['new_pattern_key'])
			newDiagramInstance.save()
			request.session['new_diagram_id'] = newDiagramInstance.id
	
			#save the pattern relationships
			for form in formset.forms:
				newPatternRelation = form.save(commit=False)
				#a hack to allow blank forms
				if not newPatternRelation.linked_pattern:
					print "No more linked patterns to save"
				else:
					# add foreign key from session variable
					newPatternRelation.subject_pattern = DesignPattern.objects.get(id=request.session['new_pattern_key'])
					# save each force to db
					newPatternRelation.save()

			# save zipped metadata file if sent
			if 'archive' in request.FILES:
				workshopMaterials = WorkshopMetadata()
				workshopMaterials.media = request.FILES['archive']	
				workshopMaterials.parent_pattern = DesignPattern.objects.get(id=request.session['new_pattern_key'])
				workshopMaterials.save()

			# see if Bibtexfile attached, if so, parse and store in db
			if 'references' in request.FILES:
				refs = request.FILES['references']
				# parsedRefs is a BibTexParser object
				loadedRefs = BibTexParser(refs.read(), customization=convert_to_unicode)
				# get the list of dicts from the object
				parsedRefs = loadedRefs.get_entry_list()

			#	print type(parsedRefs)
			#	for item in parsedRefs:
			#		print item

				for entry in parsedRefs:
				#	for k, v in entry.items():
				#		print k + " " + v

					refToSave = Reference()
					refToSave.parent_pattern = DesignPattern.objects.get(id=request.session['new_pattern_key'])
					
					print refToSave.parent_pattern.id
					
					try:
						refToSave.kind = entry['type']
						print refToSave.kind
						refToSave.title = entry['title']
						print refToSave.title
						refToSave.authors = entry['author']
						refToSave.publisher = entry['plublisher']
						refToSave.journal = entry['journal']
						refToSave.pages = entry['pages']
						refToSave.year = entry['year']
						refToSave.volume = entry['volume']
						refToSave.number = entry['number']
						refToSave.month = entry['month']
						refToSave.URL = entry['URL']
						refToSave.save()


					except(KeyError):
						continue
					
					try:
						refToSave.full_clean()
						refToSave.is_valid()
						refToSave.save()
					except ValidationError as e:
						print type(e)
						for message in e:
							print message
					
				#	refToSave.save()



		#return redirect('/') 


	#if we are not POSTing
	else:
		#and we have been to this page before
		if 'relations_added' in request.session:
			# if yes - populate the session pattern relations 
			RelationFormSet = modelformset_factory(PatternRelation, form=SetPatternRelation, can_delete=False, extra=0) # extra=0 causes dont display extra forms
																								 # if user hits back button - if there is a blank form,
																								 # user must enter a Null force or populate another one 
																								 #- they may not want to do this.
			data['form-TOTAL_FORMS'] = PatternRelation.objects.filter(subject_pattern=request.session['new_pattern_key']).count()
			initialForms = PatternRelation.objects.filter(subject_pattern=request.session['new_pattern_key'])
			formset = RelationFormSet(data, queryset=initialForms)
		
		# otherwise this is the first time to add forces - load empty forms 
		else:
			formset = RelationFormSet(data, queryset=PatternRelation.objects.none())
			formD = NewDiagram()
		
	

	return render(request, 'add_supporting.html', {'formD':formD, 'formset':formset })

def see_related_terms(request):


	#create a list to store the selected words
	listToKeep = []
	
	if request.method == "POST":

		listToKeep = request.POST.getlist('checks')
		#for item in listToKeep:
		#	print item
		
		#load all the words again based on the session variables
		wordsToDelete = RelatedWord.objects.filter(force=(Force.objects.filter(parent_pattern=request.session['new_pattern_key'])))
		#loop through all the related words in this session, if its not on the list - delete it.
		
		for thing in wordsToDelete:			
			if thing.word not in listToKeep:
				print "removing related word " + thing.word
				thing.delete()
	
		
		return redirect('/match/')

	else:

		# check to see if we have loaded words already, if so, delete all the current related words in the db, and start again with a clean slate
		# this way is a dodgy hack to prevent duplicate entries being stored in the db if the user hits back/forward multiple times
		if 'wordlist' in request.session:
		# get list of all the realted word objects for this session, then delete them - we then go and get them all again
			allWordsToDelete = RelatedWord.objects.filter(force=(Force.objects.filter(parent_pattern=request.session['new_pattern_key'])))
			for item in allWordsToDelete:
				print "Deleting them all! " + item.word
				item.delete()

		# get all the force objects for the current pattern
		terms = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])
		#terms = Force.objects.filter(parent_pattern=32)
		#creat a dict to store a list of terms for each pattern force
		related_force_terms = {}
		tempWordlist = []
		for name in terms:
			tempWordlist = thesaurus3.get_all(name.name) # we give thesaurus3 the name of the force object 
														 # thesaurus3 returns a dict of of all the related words, including the original name
			related_force_terms[name.name] = tempWordlist # store the force name and list of related terms in the dict 
														# NOTE this is passed to the template and we loop through it.

			#save the related terms in the db
			for aword in tempWordlist:
				print aword + " returned to views.py"
				wordToSave = RelatedWord(force=Force.objects.get(name=name.name), word=aword)
				wordToSave.save()

				request.session['wordlist'] = True # this doesnt need to get set every time through the second for loop, but can be anywhre inside the first if..
		

		return render(request, 'see_related.html', {'related_force_terms':related_force_terms})

def ontology_lookup(request):

	listToKeep = []
	selectedValue = {}
	if request.method == 'POST':
		
		# get the checked items - returns the id of the ontology match object 
		listToKeep = request.POST.getlist('checks')

		# get the select values (of the checked the items) 
		for item in listToKeep:
			selectedValue[item] = request.POST[item]
		
		#for item in listToKeep:
		#	print item
		#	print type(item)
		#	for k, v in selectedValue.items():
		#		print k + " " + v

		
		# set the relationship choice for the selected items
		for k, v in selectedValue.iteritems():
			w = RelatedOntologyTerm.objects.get(id=k)
			w.relationship = v
			w.save()

		
		# load all the ontology matches again
		allOntologyMatches = RelatedOntologyTerm.objects.filter(force=(Force.objects.filter(parent_pattern=request.session['new_pattern_key'])))
		# loop through all the ontology matches in this session, if its not on the listToKeep - delete it.
		for thing in allOntologyMatches:
			if str(thing.id) not in listToKeep:
		#		print "deleting " + str(thing.id)
				thing.delete()
				
		
		return redirect('/supporting/')

	else:
		# clear all previous potential matches and re-fetch on page reload
 		if 'already_matched' in request.session:
 			allThingsToDelete = RelatedOntologyTerm.objects.filter(force=(Force.objects.filter(parent_pattern=request.session['new_pattern_key'])))
			for entry in allThingsToDelete:
				entry.delete()
		
		# Get list of all the current forces from the db
		currentForces = Force.objects.filter(parent_pattern=request.session['new_pattern_key'])

		search_terms = {}
		#terms = []
		# for each force, get the name, sore in a list, then append to the list the related words (if any)
		# then query the NCBO API, and return a dict which contains the force, and a list of ontology matches....
		for item in currentForces:
			terms = [] # reset the terms list?
			#store the foce name
			terms.append(item.name)
		
			# get the related terms and append to the list
			wordObjects = RelatedWord.objects.filter(force_id=item.id)
			for thing in wordObjects:
				terms.append(thing.word)

			# store in a dict forces [key] and terms [list of values] to be passed to the lookup
			search_terms[item.name] = terms

		#	for k, v in search_terms.items():   #
		#		#print k 						#  This prints a list of search terms to the console for debugging
		#		for item in v:					# 
		#			print item 					#
	
		# lookup returns a dict of dict to be stored in matches. dict[force name] {[term]{ncbo JSON}} 
			matches = class_lookup.lookup(search_terms)

		#print type(matches) # matches is a dict {}
		#k = matches.keys() # keys are unicode force names
		#print k

		#saved_option = {} #create empty dict to store the saved options - later this will be a model instance

		for match, data in matches.iteritems(): #for each key (match) in the matches dict{} , there is another dict{} (data) as the value
			#d = data.keys()  # the data keys are 'links' 'pageCount' 'collection' 'prevPage' 'nextPage'
			force_we_are_working_on = match
			# we are interested in the 'collection' key = the value of which is a list of dicts! yikes!
			# i.e data['collection'] in this for loop contains a list of dicts{} !
	
			# for each force term (match) fetch the list of dicts we are interested in
			newlist = data['collection']

			# we now want to access the dicts in this list
			for thing in newlist:
			#	print type(thing)
			#	k = thing.keys()
			#	print k

			# the dict keys in our newlist (a copy of data['collection']) vary by item - but include 'definition', 'synonym', 'links', 'semanticType', 'obsolete', 'prefLabel' '@context' '@id' '@type' 'cui'
	
			# the values for each of the keys differs too - with more nested dicts, list, etc...  looping over them as below gives the following mapping...
			#	for key, datas in thing.iteritems():
			#		print type(datas)

			#the above gives....
			# 'definition'    <type 'list'>  
			# 'synonym'       <type 'list'>
			# 'links'	      <type 'dict'>
			# 'semanticType'  <type 'list'>  
			# 'obselete'      <type 'bool'>
			# 'prefLabel'     <type 'unicode'>
			# '@context'      <type 'dict'>
			# '@id'           <type 'unicode'>
			# '@type'         <type 'unicode'>
			# 'cui'           <type 'list'>
				
			# we want to grab prefLabel, synonym, defintion, id, type, and from within links - the value of ['ontology']
			# then store all of these in a db table, indexed by force.
			# later the user can cull the ones they dont want.
			
			#only save instances for which definitions exist 
			
				saved_option = RelatedOntologyTerm()

				if 'definition' in thing:

					saved_option.definition = str(thing['definition']).strip('u[]')  # we need to convert this to a string
					saved_option.prefLabel = thing['prefLabel']
					if 'synonym' in thing:
						saved_option.synonyms = thing['synonym']  # watch the s here!
					saved_option.term = thing['@id']
					#saved_option['type'] = thing['@type']
				
					for a, b in thing.iteritems():
						if a == 'links' and 'ontology' in b:
							parsedURL = b['ontology'].split('/')  #the ontology name (URL) returned from the API needs to converted to the 
							name = parsedURL[-1]				  # human clickable link - we parse the URL and grab the last '/'sep element
																  # whcih is the ontology name - eg NCIT from http://data.bioportal/NCIT
							saved_option.ontology = "http://bioportal.bioontology.org/ontologies/" + name 
				
					saved_option.force = Force.objects.get(name=force_we_are_working_on)  # not sure if this variable is accessible

					saved_option.save()

					request.session['already_matched'] = True

				# should now be a list saved to the db. - a list of all possible cadidate matches 
				# we need to present these to the template and have the user cull/select only the relevant ones

		# collect and pass the saved but unfiltered matches to the template 	
	
		ontology_match = {}
		for item in currentForces:
			ontology_match[item.name] = RelatedOntologyTerm.objects.filter(force=Force.objects.filter(name=item.name))
			# ontology_match is now a dict with keys = force name, values = model instances
			# we loop over these in the template and diplay them for slection and relationship setting...
	
		choices = RelatedOntologyTerm.CHOICES
	
	

		# flush the session dictonary so adding another pattern in during the same browser session wont overwrite the one we just added...
		# this should come after the last form entry page.
		#	request.session.flush()			
		#del request.session['new_pattern_key']
		#del request.session['new_pattern_name']
		#del request.session['new_pattern_image']
		#del request.session['new_problem_id']
		#del request.session['new_context_id']
		#	del request.session['new_force_id']
		#del request.session['forces_added']
		#del request.session['new_solution_id']
		#del request.session['new_rationale_id']
	
		#del request.session['wordlist']

		return render(request, 'match.html', {'ontology_match':ontology_match, 'choices':choices})


