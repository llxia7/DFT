from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from ATM.models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from functools import reduce
import re
import time


class TestLog(ListView):
	model = Test_Log

class ActionMap(ListView):
	model = Action_Map



### Show test log list, see the log detail, delete logs, create tables.
def log_list(request):
	select_pk_list = list(filter(lambda x : request.POST.dict()[x]=='on' , request.POST.dict() ))
	select_name_list = list(map(lambda x : Test_Log.objects.get(pk=x).log_name , select_pk_list))
	object_list = Test_Log.objects.all()

	### Show 2d applicaton map.
	if (request.POST.get('action')=='2dmap'):

		response = TemplateResponse(request,'atm/app_map.html', data, )
		return response

	### When push the delete button, go to confirm page.
	elif (request.POST.get('action')=='delete'):
		request.session['d_pk']=select_pk_list
		data = {
			'select_list':select_name_list,
		}
		response = TemplateResponse(request,'atm/confirm_delete.html', data, )
		return response

	### After confirm the delete objects, delete them.
	elif (request.POST.get('action')=='confirm_delete'):
		d_pk_list = request.session['d_pk']
		for pk in d_pk_list:
			Test_Log.objects.filter(id=pk).delete()

	data={
		'object_list':object_list,
	}

	response = TemplateResponse(request,'atm/test_log_list.html',data, )
	return response



def log_details(request,pk):
	test_log = Test_Log.objects.all().get(pk=pk)
	results = Result_Detail.objects.all().filter(log_name=pk)

	data = {
		'test_log':test_log,
		'results':results,
	}
	response = TemplateResponse(request,'atm/log_detail.html',data, )
	return response



# Create your views here.
def import_log(request):

	if (request.POST.get('action')=='import'):

		iform = Test_Result_Import_Form(request.POST, request.FILES)

		if iform.is_valid():
			iform.save()

		else:
			form_err = iform.errors


	else:
		iform = Test_Result_Import_Form()


def create_map(request):
	display_list=""

	if (request.POST.get('action')=='app_map'):

		### get datas from database
		im_list = ''

		### transfer data to display_list
		display_list=""

	data = {
		'display_list':display_list,
	}

	response = TemplateResponse(request,'atm/create_map.html',data, )
	return response
#def log_detail(request,pk):
#
#	try_list = []
#	try_dict = {}
#	try_obj	= ''
#
#	test_log = Test_Log.objects.get(pk=pk)
#	result_display_list = []
#
#	### get device list
##	device_list = []
##	all_device_obj = Device.objects.all()
##	for do in all_device_obj:
##		device_list.append(do.name)
#	device_list = list(map(lambda x : x.name , Device.objects.all()))
#
#	### make instrument model -> action tree data structure
#	im_ac_dict = {}
#	sf_list = []
#	all_action_map_obj = Action_Map.objects.all()
#	im_old = ''
#	im_new = ''
#	ac_list = []
#	for amo in all_action_map_obj:
##		print(amo)
#		im_new = amo.instrument_model
#		ac_new = amo.action
#		if im_new == im_old:
#			ac_list.append(ac_new)
#		elif im_old :
#			ac_list = list(set(ac_list))
#			im_ac_dict[im_old]=ac_list
#			ac_list=[]
#			ac_list.append(ac_new)
#		else:
#			ac_list=[]
#			ac_list.append(ac_new)
#		im_old = im_new
#	ac_list = list(set(ac_list))
#	im_ac_dict[im_old]=ac_list
#
#
#
#
#	### get all related detail objects accoding to log name
#	all_detail_obj = Log_Detail.objects.all().filter(log_name=test_log.pk)
#
#
#	### make result list to display, it is a list of list.
#	### each list contain 4 data
#	### [Data, Action, Device, Result]
#	### [Head, Text, RoS, CoS ]
#	### [Tag, html tag, '', '']
#	### template file will print different content accoding to these data.
#	result_display_li_li = []
#	result_list = []
#	for im in im_ac_dict.keys():
#		ac_count = len(im_ac_dict[im])
#		ac_list = im_ac_dict[im]
#		result_list = ['Tag','tr','','']
#		result_display_li_li.append(result_list)
#		result_list = ['Head', im, ac_count, '1']
#		result_display_li_li.append(result_list)
#		for ac in ac_list:
#			sf_list=[]
#			if (ac_list.index(ac)>=1):
#				result_list = ['Tag','tr','','']
#				result_display_li_li.append(result_list)
#			result_list = ['Head', ac, '1', '1']
#			result_display_li_li.append(result_list)
#
#			sf_list = list(map(lambda x : x.sub_flow, all_action_map_obj.filter(action=ac)))
#			for d in device_list:
#				dpk = Device.objects.get(name=d).pk
#				result='N'
#				ampk_list = list(map(lambda x : Action_Map.objects.get(sub_flow=x).pk, sf_list))
#				ampk_list = list(filter(lambda x : all_detail_obj.filter(device=dpk, sub_flow=x) , ampk_list))
#				pf_list = list(map(lambda x : all_detail_obj.get(device=dpk, sub_flow=x).result , ampk_list))
#				if pf_list:
#					result = reduce(lambda x,y : x if x=='F' else y, pf_list)
#
#
#
##			### find sf_list for current ac
##			for obj in all_action_map_obj:
##				if obj.action == ac:
##					sf_list.append(obj.sub_flow)
##
#				### Combine all the sub_flow result in the sub_
##				for sf in sf_list:
##					#ampk = Action_Map.objects.get(sub_flow=sf).pk
##					ampk_f = lambda x: Action_Map.objects.get(sub_flow=x).pk
##					ampk = ampk_f(sf)
##					try:
##						detail_obj = all_detail_obj.get(device=dpk, sub_flow=ampk)
##						if result !='F':
##							result = detail_obj.result
##					except:
##						pass
#				result_list = ['Data', ac, d, result]
#				result_display_li_li.append(result_list)
#
#			result_list = ['Tag', 'etr', '', '']
#			result_display_li_li.append(result_list)
#
#
#
#
#	data={
#		'try_list':ac_list,
#		'try_dict':im_ac_dict,
#		'test_log':test_log,
#	#	'result_list':result_list,
#		'try_obj':all_action_map_obj,
#		'display_list':result_display_li_li,
#		'device_list':device_list,
#	}
#
#	response = TemplateResponse(request,'atm/log_detail.html',data, )
#	return response
