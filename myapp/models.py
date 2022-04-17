from django.db import models


class Document(models.Model):
    docfile = models.FileField(upload_to='uploads/%Y/%m/%d')
class Results(models.Model):
    docfile = models.FileField(upload_to='results/%Y/%m/%d')
