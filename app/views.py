from django.db.models import Q

from app.models import Person

from datetime import date, datetime


def exact_or_not():

    # returns only Rafa
    exact = Person.objects.filter(first_name__exact='Rafa')
    print("Exact:", exact)

    # Return also objects such as RAFA, rafa and so on.
    iexact = Person.objects.filter(first_name__iexact='Rafa')
    print("Iexact:", iexact)
    
    #    same happens with contains and icontains




def q_objects():

    date_ = date(2008, 1, 1 )

    person = Person.objects.filter(Q(birth_date__lt=date_) | Q(tean=True))
    print(person)