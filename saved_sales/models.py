from django.db import models

class Saved_sales(models.Model):
    id_sale = models.IntegerField(null=True)
    store = models.CharField(max_length=100)
    headline = models.CharField(max_length=100)
    id_user = models.IntegerField(null=True)


