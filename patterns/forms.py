from django.forms import ModelForm, TextInput
from patterns.models import DesignPattern

class NewPatternName(ModelForm):
	class Meta:
		model = DesignPattern 
		fields = ['name']
		widgets = { 'name': TextInput(attrs={'placeholder': 'Enter a pretentious soundign name for the pattern'})
		}
