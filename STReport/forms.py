from django import forms
from django.forms import ModelForm
from STReport.models import *
from django.contrib.admin import widgets
# from django.forms.extras.widgets import *
from django.forms.widgets import *
from django.contrib.admin import widgets
from django.db import models


# class ST_log_import_Form(forms.Form):
class ST_log_import_Form(ModelForm):
    class Meta:
        model = ST_log
        fields = '__all__'
    # exclude = ['data_csv']

    # fields = ['title', 'data_log', 'begin_time', 'end_time', 'tape']
    # import_file = forms.FileField()
    # process_names = forms.CharField(max_length=100)
    choose_VSZ = forms.BooleanField(required=False, initial=True)
    choose_RSZ = forms.BooleanField(required=False, initial=True)


class ST_log_Form(ModelForm):
    class Meta:
        model = ST_log
        fields = '__all__'


    # widgets = {
    #            'start_time': forms.DateInput(attrs={'class':'datepicker'}),
    #        }
    # start_date = forms.DateTimeField(widget=widgets.AdminDateWidget())

class ST_log_list_Form(ModelForm):
    class Meta:
        model = ST_log
        fields = '__all__'

    check_box = forms.BooleanField(required=False)


###############################################
##############  Edited by #####################
############## Jiayu Zhu  #####################
##############  Begin    ######################
###############################################
class ST_log_attach_Form(ModelForm):
    class Meta:
        model = ST_log_attach
        fields = '__all__'


###############################################
##############  Edited by #####################
############## Jiayu Zhu  #####################
##############    End    ######################
###############################################

###############################################
##############  Edited by #####################
############## Jiayu Zhu  #####################
##############  Begin    ######################
###############################################
class CSV_chart_Form(forms.Form):
    timecol = forms.FloatField()
    selection = forms.CharField(max_length=200)
    anno_name = forms.CharField(max_length=100)
    anno_text = forms.CharField(max_length=1000)
###############################################
##############  Edited by #####################
############## Jiayu Zhu  #####################
##############    End    ######################
###############################################
