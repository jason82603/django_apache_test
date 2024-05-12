from django.db import models
from django.contrib.auth.models import User

class ProductModel(models.Model):
    pname =  models.CharField(max_length=100, default='')
    pprice = models.IntegerField(default=0)
    pdescription = models.TextField(blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.pname

class UVData(models.Model):
    station_name = models.CharField(max_length=50)
    element_name = models.CharField(max_length=100)
    uv_index = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.station_name} - {self.element_name} ({self.date})"