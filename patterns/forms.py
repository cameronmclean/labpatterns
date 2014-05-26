from django.forms import ModelForm, TextInput, HiddenInput, Textarea
from patterns.models import *

# This is the form to add a new pattern name and pattern pictogram to the database - it is inteded as the fist page for adding a new pattern.
class NewPatternName(ModelForm):
	class Meta:
		model = DesignPattern 
		fields = ['name', 'pictogram']
		widgets = { 'name': TextInput(attrs={'placeholder': 'Enter a pretentious sounding name for the pattern'})
		}

class NewProblem(ModelForm):
	class Meta:
		model = Problem 
		fields = ['description']
		labels = { 'description': 'Problem Description',
		}
		widgets = { 'description': Textarea(attrs={'cols':80, 'rows':20}), 'description': Textarea(attrs={'placeholder': 'Enter a pithy description of the problem'}), 
		}

class NewContext(ModelForm):
	class Meta:
		model = Context 
		fields = ['description']
		labels = { 'description': 'Context',
		}
		widgets = {  'description': Textarea(attrs={'cols':80, 'rows':20}), 'description': Textarea(attrs={'placeholder': 'Enter a detailed description of the context in which this problem occurs'})
		}

# the NewForce from is used in form factory (modelformset_factory) in the view to allow muliple instances of forces to be displated and edited on a single page  
class NewForce(ModelForm):
	class Meta:
		model = Force 
		fields = ['name', 'description', 'pictogram']
		labels = { 'name': 'Force', 'description': 'Definition',
		}
		widgets = {  'description': Textarea(attrs={'cols':80, 'rows':20}), 'description': Textarea(attrs={'placeholder': 'Enter a definition for this force term - be as specific as the pattern allows'}),
					'name': TextInput(attrs={'placeholder': 'Enter a term to name this force'})

		}

class NewSolution(ModelForm):
	class Meta:
		model = Solution 
		fields = ['description']
		labels = { 'description': 'Solution Description',
		}
		widgets = {  'description': Textarea(attrs={'cols':80, 'rows':20}), 'description': Textarea(attrs={'placeholder': 'Enter a pithy description of the solution'})
		}

class NewRationale(ModelForm):
	class Meta:
		model = Rationale 
		fields = ['description']
		labels = { 'description': 'Rationale',
		}
		widgets = {  'description': Textarea(attrs={'cols':80, 'rows':20}), 'description': Textarea(attrs={'placeholder': 'Enter a detailed description of the rationale which justifies the solution'})
		}


class NewDiagram(ModelForm):
	class Meta:
		model = Diagram 
		fields = ['title', 'comment', 'diagram']
		labels = {'title': 'Title', 'diagram': 'Diagram', 'comment': 'Comment'}
		widgets = { 'title': TextInput(attrs={'placeholder': 'Enter a title for the diagram'}), 'comment': Textarea(attrs={'placeholder': 'Enter a description for the diagram', 'cols':80, 'rows':20})
		}
