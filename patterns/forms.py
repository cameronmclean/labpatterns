from django.forms import ModelForm, TextInput, HiddenInput
from patterns.models import *

# This is the form to add a new pattern name and pattern pictogram to the database - it is inteded as the fist page for adding a new pattern.
class NewPatternName(ModelForm):
	class Meta:
		model = DesignPattern 
		fields = ['name', 'pictogram']
		widgets = { 'name': TextInput(attrs={'placeholder': 'Enter a pretentious soundign name for the pattern'})
		}

class NewProblem(ModelForm):
	class Meta:
		model = Problem 
		fields = ['description']
		widgets = { 'description': TextInput(attrs={'placeholder': 'Enter a pithy description of the problem'})
		}

class NewContext(ModelForm):
	class Meta:
		model = Context 
		fields = ['description']
		widgets = { 'description': TextInput(attrs={'placeholder': 'Enter a detailed description of the context in which this problem occurs'})
		}