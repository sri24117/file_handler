from django.db import models
import os


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

    def get_file_extension(self):
        filename, extension = os.path.splitext(self.file.name)
        return extension
