from django.db.models import Q, F, DateTimeField, ExpressionWrapper, Count
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from app.models import BloodBank, Person

from datetime import date, timedelta


# How does Count works


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



def nested_q(request):

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


def f_object(request):

    # no need to have a can_donate_field on DB
    # F makes us able to compute something

    people = Person.objects.annotate(
        can_donate_on=ExpressionWrapper(
            F("last_donated") + timedelta(days=56),
            output_field = DateTimeField()
            ) 
    ).filter(can_donate_on__lt=timezone.now())

    # Expression Wrapper is used to set common output_field fo 2 different


    return render(request, 'can_donate.html', {'people': people})


def f_different_fields(request):

    bank = BloodBank.objects.annotate(
        existent_amount=Count('bloodbag_set'),
        remaining=F('goal') - F('existent_amount')
    ).values_list("goal", "existent_amount", "remaining")

    print(bank)
    return JsonResponse("OK", safe=False)


def q_f_together(request):

    people = Person.objects.filter(
        Q(first_name=F('last_name'))
        & ~Q(job__icontains='DEV')
    )
    # First name equals to last name and job not include DEV

    people2 = Person.objects.filter(
        first_name=F('last_name')
    )  # this works too :D

    print(people2)

    return render(request, "job.html", {"people":people})

