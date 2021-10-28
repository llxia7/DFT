from django.db import models
# from django.core.files.storage import FileSystemStorage
from new_api.files import *
# from unittest.test.test_case import log_foo
from DFT.settings import MEDIA_ROOT, MEDIA_URL

# fs = FileSystemStorage(location='files/stest',base_url='/files/stest')
# ofs = OverwriteStorage(location='/files/stest',base_url='/files/stest')
ofs = OverwriteStorage(location=MEDIA_ROOT + 'streport', base_url=MEDIA_URL + 'streport')


class ST_log(models.Model):
    title = models.CharField(max_length=100, unique=True)
    data_log = models.FileField(storage=ofs)
    data_csv = models.FileField(max_length=91, storage=ofs)
    time_csv = models.FileField(max_length=92, storage=ofs, blank=True)
    spike_csv = models.FileField(max_length=93, storage=ofs, blank=True)
    process_names = models.CharField(max_length=200)
    workstation_model = models.CharField(max_length=30, blank=True)
    workstation_name = models.CharField(max_length=30, blank=True)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    save_date = models.DateField(auto_now=True)
    st_tape = models.CharField(max_length=150, blank=True)
    tcct_tape = models.CharField(max_length=150, blank=True)
    device = models.CharField(max_length=50, blank=True)
    remarks_mem = models.TextField(blank=True)
    remarks_tet = models.TextField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


#	def file_path(instance, filename):
#		return os.path.join('some_dir', str(instance.some_identifier), 'filename.ext')

class ST_log_attach(models.Model):
    # log_pk		= models.ForeignKey('ST_log',on_delete=models.CASCADE,to_field='title')
    log_pk = models.ForeignKey('ST_log', on_delete=models.CASCADE)
    attachment = models.FileField(max_length=94, storage=ofs)

    class Meta:
        ordering = ['log_pk']

    def __str__(self):
        return self.log_pk.title
