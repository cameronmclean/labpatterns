from django.forms import ModelForm, TextInput
#from django import forms
from patterns.models import DesignPattern

class NewPatternName(ModelForm):
	class Meta:
		model = DesignPattern 
		fields = ['name', 'pictogram']
		widgets = { 'name': TextInput(attrs={'placeholder': 'Enter a pretentious soundign name for the pattern'})
		}
	#name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter a pretentious sounding name'}))
	#description = forms.CharField()
	#pictogram = forms.ImageField(widget=forms.FileInput)