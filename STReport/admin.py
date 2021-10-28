from django.contrib import admin
from STReport.models import *
from django.db import models

class ST_log_Admin(admin.ModelAdmin):
	list_display = ('title','workstation_model','workstation_name','begin_time','end_time','save_date','device')
	list_filter = ('title','workstation_model','workstation_name','begin_time','end_time','save_date','device')

admin.site.register(ST_log, ST_log_Admin)

class ST_log_attach_Admin(admin.ModelAdmin):
	list_dispaly = ('log_pk','attachment')
	list_filter = ('log_pk','attachment')
	
admin.site.register(ST_log_attach, ST_log_attach_Admin)
