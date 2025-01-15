from django.db import models


class Membre(models.Model):
    name = models.fields.CharField(max_length=150)
    first_name = models.fields.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)