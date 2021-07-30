from app.models import Author, Blog, BloodBank,  Experiment, Comment, Order, Person, Pet
from django.contrib import admin


admin.site.register(Person)
admin.site.register(BloodBank)
admin.site.register(Pet)
admin.site.register(Order)
admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Experiment)