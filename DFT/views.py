from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

def home(request):
	authentication_form=AuthenticationForm

	if request.user.is_authenticated():
#		update_log = Log.objects.all().order_by('-up_date')
#		manual = SystemManual.objects.all().order_by('name') 
#
#		data = {
#			'update_log':update_log,
#			'manual':manual,
#		}
#
#		response = TemplateResponse(request,'home.html',data,)
		response = TemplateResponse(request,'pages/index.html',)
	else:
		form = authentication_form(request)

		response = TemplateResponse(request,'login.html',{'form':form})

	return response
