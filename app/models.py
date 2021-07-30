from app.managers import PersonManager

from django.utils import timezone
from django.db import models


class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nickname = models.CharField(default='nick', max_length=50)
    job = models.CharField(default='DEV', max_length=50)
    birth_date = models.DateField()
    birth_date_year = models.PositiveIntegerField(default=2000)
    tean = models.BooleanField(default=False)
    postal_code = models.CharField(max_length=10, default='AB')
    last_donated = models.DateTimeField(default=timezone.now)
    joined_on = models.DateField(default=timezone.now)

    objects = PersonManager.as_manager()

    def save(self, *args, **kwargs):
        self.birth_date_year = int(str(self.birth_date)[:4])

        if self.birth_date_year > 2003:
            self.tean = True

        super(Person, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return self.first_name + " " +self.last_name

    def __str__(self) -> str:
        return self.full_name



class BloodBank(models.Model):
    
    bloodbag_set = models.IntegerField()
    goal = models.IntegerField()


class Pet(models.Model):

    name = models.CharField(default="Kessy", max_length=50)
    pet_type = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name + " " + self.pet_type


class Order(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Person, related_name='orders', on_delete=models.CASCADE)
    total = models.PositiveIntegerField()


class Author(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
    goes_by = models.CharField(max_length=50, null=True, blank=True)



class Blog(models.Model):

    body = models.TextField()
    modified = models.DateField(auto_now=True)


class Comment(models.Model):

    body = models.TextField()
    modified = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
