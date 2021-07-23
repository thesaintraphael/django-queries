from django.db import models


class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    birth_date_year = models.PositiveIntegerField(default=2000)
    tean = models.BooleanField(default=False)
    postal_code = models.CharField(max_length=10, default='AB')

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
