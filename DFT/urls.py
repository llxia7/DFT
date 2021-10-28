from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from STReport.views import ReportList, ReportDetail
from ATM.views import TestLog, ActionMap
from home import views as home_views
from STReport import views as STReport_views
from ATM import views as ATM_views
from QualityIndex import views as QI_views
from django.views.static import serve
import django.contrib.auth

admin.autodiscover()


def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


urlpatterns = [

    ### Admin
    #	(r'^admin/', include(admin.site.urls)),
    #	(r'^admin/jsi18n', i18n_javascript),
    #	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin', admin.site.urls),

    ### Memory Stress Test Report
    url(r'^$', home_views.dashboard, name='home'),
    url(r'^dashboard', home_views.dashboard, name='home'),
    url(r'^stest/list$', ReportList.as_view()),
    url(r'^stest/report_detail/(?P<pk>\d+)$', ReportDetail.as_view()),
    url(r'^stest/import_log$', STReport_views.import_log),
    url(r'^stest/edit$', STReport_views.edit),
    url(r'^stest/list_reports$', STReport_views.list_reports),
    url(r'^stest/add_anno$', STReport_views.add_anno),
    url(r'^stest/edit_report$', STReport_views.edit_report),

    ### Application Test Map
    url(r'^atm/import_log$', ATM_views.import_log),
    url(r'^atm/test_log$', ATM_views.log_list),
    url(r'^atm/log_detail/(?P<pk>\d+)$', ATM_views.log_details),
    url(r'^atm/action_map$', ActionMap.as_view()),
    url(r'^atm/log_list$', ATM_views.log_list),

    ### Quality Index
    url(r'^qi/data$', QI_views.list_log),

    ### Static
    #	url(r'^statics/$','templates/pages/'),
    #	url(r'^templates/(?P<path>.*)$',include('django.views.static.serve'),{'document_root':settings.MEDIA_ROOT+'templates'}),
    #	url(r'^files/(?P<path>.*)$',include('django.views.static.serve'),{'document_root':'files'}),

    #	url(r'^temp/(?P<path>.*)$',include('django.views.static.serve'),{'document_root':'temp'}),

]

if settings.DEBUG:
    urlpatterns += [
        url(r'^files/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    ]
