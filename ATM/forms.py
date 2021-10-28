from django import forms
from django.forms import ModelForm
from django.db import models

class Test_Result_Form(ModelForm):
	class Meta:
		model = Test_Result
		fields = '__all__'

class Test_Result_Import_Form(forms.Form):
	log_file = forms.FileField()


