from django import forms

class RegistrationForm(forms.Form):
	role = forms.ChoiceField(choices=(('dps', 'DPS'), ('healer', "Healer"), ('tank', 'Tank')),
									 widget=forms.RadioSelect)
	standby = forms.BooleanField(False)
