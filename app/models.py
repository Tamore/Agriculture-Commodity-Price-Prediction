from django.db import models

# Create your models here.
from django.db import models
    
class Datas(models.Model):
    district = models.CharField(max_length=50)
    market = models.CharField(max_length=50)
    commodity = models.CharField(max_length=50)
    variety = models.CharField(max_length=50)  
    grade = models.CharField(max_length=50, blank=True)  #Grade can be empty for
    date = models.CharField(max_length=50)