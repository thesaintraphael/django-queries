from app.models import Author, BloodBank, Order, Person, Pet
from django.contrib import admin


admin.site.register(Person)
admin.site.register(BloodBank)
admin.site.register(Pet)
admin.site.register(Order)
admin.site.register(Author)
