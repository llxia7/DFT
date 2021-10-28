from django.template.response import TemplateResponse
from STReport.models import *
from ATM.models import *


def dashboard(request):
    latest_STReport_list = ST_log.objects.filter().order_by('-save_date')[:5]
    latest_ATM_list = Test_Log.objects.filter().order_by('-save_date')[:5]
    data = {
        'latest_STReport_list': latest_STReport_list,
        'latest_ATM_list': latest_ATM_list,

        #		'cate_form': cate_form,
    }

    response = TemplateResponse(request, 'DashBoard.html', data, )
    return response
