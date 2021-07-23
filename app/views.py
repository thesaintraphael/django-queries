from django.db.models import Q
from django.shortcuts import render

from app.models import Person

from datetime import date


def exact_or_not():

    # returns only Rafa
    exact = Person.objects.filter(first_name__exact='Rafa')
    print("Exact:", exact)

    # Return also objects such as RAFA, rafa and so on.
    iexact = Person.objects.filter(first_name__iexact='Rafa')
    print("Iexact:", iexact)
    
    #    same happens with contains and icontains




def q_and_or(request):

    date_ = date(2008, 1, 1 )

    # or
    people = Person.objects.filter(Q(birth_date__gt=date_) | Q(tean=True))

    # and
    people = Person.objects.filter(Q(birth_date__lt=date_) & Q(tean=True))
  
    return render(request, 'main.html', {'people': people})



def q2(request):

    # all_people = Person.objects.filter(postal_code='BB')
    all_people = Person.objects.all()

    # nested Q query
    people = Person.objects.filter(
        
        # range, obvopusly
        Q(
            Q(birth_date__year__range=(1990, 1992))
            | Q(birth_date__year__range=(1995, 2002))
        )

        # and with postal code BB
        & Q(postal_code="BB")

        # and not that which starts with C
        & ~Q(first_name__startswith='C')

        | ~Q(
            postal_code='BB'
        )
            # TODO check it out
    )

    return render(request, "nested.html", {"all_people": all_people, "people": people})



def search(request):

    params = ['name']
    value = 'Cris'

    user_filter = Q()
    # creating Q object

    if "name" in params:
        
        # adding filters to Q objects
        user_filter.add(
            Q(
                Q(first_name__icontains=value)
                | Q(last_name__icontains=value)
            ),
            Q.OR # could be AND depends on a filter
        )

    if 'postal_code' in params:

        user_filter.add(
            Q(postal_code=value), Q.OR
        )
    
    people = Person.objects.filter(user_filter)

    return render(request, 'search.html', {"people":people})


