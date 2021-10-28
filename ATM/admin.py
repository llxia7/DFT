from django.contrib import admin
from ATM.models import *
from django.db import models

class Action_Map_Admin(admin.ModelAdmin):
	list_display = ('sub_flow','action','instrument_model','device')
	list_filter = ('sub_flow','action','instrument_model','device')
admin.site.register(Action_Map, Action_Map_Admin)

class Test_Log_Admin(admin.ModelAdmin):
	list_display = ('log_name','test_date','device','stage')
	list_filter = ('log_name','test_date','device','stage')

admin.site.register(Test_Log, Test_Log_Admin)

class Result_Detail_Admin(admin.ModelAdmin):
	list_display = ('log_name','sub_flow','result')
	list_filter = ('log_name','sub_flow','result')

admin.site.register(Result_Detail, Result_Detail_Admin)

class Device_Admin(admin.ModelAdmin):
	list_display = ('name',)
	list_filter = ('name',)

admin.site.register(Device, Device_Admin)
