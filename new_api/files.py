from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):

        # file_dir = os.path.join(settings.BASE_DIR,'/files/stest/')
        # file_path = os.path.join(file_dir,name)
        # file_path = os.path.join(settings.BASE_DIR,'files/stest/',name)
        file_path = self.path(name)
        if self.exists(file_path):
            os.remove(file_path)
        else:
            print("overwrite wrong")
        return name
