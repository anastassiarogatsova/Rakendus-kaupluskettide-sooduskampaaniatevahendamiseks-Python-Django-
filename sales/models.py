from django.db import models

class Sale(models.Model):
    category = models.TextField()
    store = models.CharField(max_length=100)
    headline = models.CharField(max_length=100)
    image = models.TextField()
    discount = models.TextField(null=True)
    new_price=models.TextField(null=True)
    old_price=models.TextField(null=True)
    


    def __str__(self):
        return self.headline



