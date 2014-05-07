from django.forms import ModelForm, TextInput
from patterns.models import DesignPattern

class NewPatternName(ModelForm):
	class Meta:
		model = DesignPattern 
		fields = ['name', 'pictogram']
		# need to add pictogram to form - but modelForm and model have a field mismatch that needs to be declared or else validation errors ensue.
		widgets = { 'name': TextInput(attrs={'placeholder': 'Enter a pretentious soundign name for the pattern'})
		}
