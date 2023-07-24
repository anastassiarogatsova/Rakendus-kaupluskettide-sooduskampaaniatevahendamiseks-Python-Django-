from django.db import models

# Create your models here.

class Campaign(models.Model):
    kmp_url = models.TextField(null=True)
    kmp_bg_image=models.TextField(null=True)
    kmp_desc=models.TextField(null=True)
    

