from django.db import models

# Create your models here.



class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    tean = models.BooleanField(default=True)

    @property
    def full_name(self):
        return self.first_name + " " +self.last_name
