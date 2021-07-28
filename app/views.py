from django.db.models import (Q, F, DateTimeField, 
    Value, ExpressionWrapper, Count, FloatField, Sum)
from django.db.models.expressions import Case, When
from django.db.models.fields import BooleanField, IntegerField
from django.db.models.functions import Concat, ExtractYear
from django.db.models.functions.comparison import Cast, Coalesce, NullIf
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from app.models import Author, BloodBank, Order, Person, Pet

from datetime import date, timedelta


def exact_or_not():

    # returns only Rafa
    exact = Person.objects.filter(first_name__exact='Rafa')
    print("Exact:", exact)

    # Return also objects such as RAFA, rafa and so on.
    iexact = Person.objects.filter(first_name__iexact='Rafa')
    print("Iexact:", iexact)
    
    #    same happens with contains and icontains


# ----------------------------- Q objects -------------------------------------


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


# ------------------------------------ F objects ---------------------------


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


# ---------------------------------- DB functions -----------------------------------------------------

def count_types(request):
    
    pet_types = Pet.objects.values('pet_type').annotate(
     Count('pet_type')
 )
    print("Only types:", pet_types)

    pets = Pet.objects.values('pet_type', "name").annotate(
     Count('pet_type'), Count('name')
)      
    # this one not returns expected answer, counts only when both fields are same in different objects
    #  A.pet_type == B.pet_type and A.name == B.name

    print("Name and types:", pets)


    return JsonResponse("ok", safe=False)


def concat(request):

    persons = Person.objects.annotate(
        full_name=Concat("first_name", Value(" "), "last_name")
    ).filter(full_name__icontains="nn p").values_list('full_name')
    # without Value result contains no space between first and last names ---> LukaModric instead of Luka Modric

    print(persons)

    # set custom manager
    persons = Person.objects.annotate_full_name().filter(full_name__icontains='nn p').values_list('full_name')
    print(persons) # same result


    persons = Person.objects.annotate(
        full_name=F('first_name') + " " + F('last_name')
    ).values_list('full_name') # returns only zeros (probably cannot add strings)
    print(persons)

    return JsonResponse('ok', safe=False)


def coalesce(request):

    persons = Person.objects.annotate(
        goes_by=Coalesce(
            NullIf('nickname', Value('')),
            'first_name'
        )
    ).values_list('goes_by')

    # goeby equals to first_name if nickname is empty string

    print(persons)

    return JsonResponse("ok", safe=False)


def conditional_expressions(request):

    orders = Order.objects.annotate(
        discounted_total=Case(
            When(
                customer__joined_on__year__range=(2010, 2018),
                then=ExpressionWrapper(F('total')*0.8, output_field=FloatField()),
            ),

            When(
                customer__joined_on__year__range=(1990, 2008),
                then=ExpressionWrapper(F('total')*0.6, output_field=FloatField())
            ),

            default=ExpressionWrapper(F("total"), output_field=FloatField())
        )
    ).values_list('discounted_total', "customer__last_name")

    print(orders)

    return JsonResponse('ok', safe=False)



def mixed(request):

    # TODO try F("birth_date__year") instead of Extract year

    persons = Person.objects.annotate(
        birth_year_int=Cast(
            ExtractYear("birth_date"),
            output_field=IntegerField(),
        ),
        birth_year_modulus_4=F("birth_year_int") % 4,
        birth_year_modulus_100=F("birth_year_int") % 100,
        birth_year_modulus_400=F("birth_year_int") % 400,
    
    ).annotate(

        born_in_leap_year=Case(
            When(
                Q(
                    Q(birth_year_modulus_4=0)
                    & Q(
                        ~Q(birth_year_modulus_100=0)
                        | Q(birth_year_modulus_400=0)
                    )
                ),
                then=True,
            ),
        default=False,
        ouput_field=BooleanField()
        ),
        
    ).filter(born_in_leap_year=True). values_list("birth_date__year", flat=True).order_by('-id')

    # flat used with only one field. Returns one list, not tuples.

    print(persons)

    return JsonResponse("ok", safe=False)


def cast(request):

    author = Author.objects.annotate(
        age_as_float=Cast('age', output_field=FloatField())
    ).first()

    print(author.age_as_float)

    return JsonResponse("ok", safe=False)


def coalesce2(request):

    Author.objects.create(
        name='Margaret Smith', goes_by='Maggie'
    )

    author = Author.objects.annotate(
        screen_name=Coalesce('alias', 'goes_by', 'name')
    ).last()    

    # returns first none null value from given values

    print(author.screen_name)


def coalesce_prevent(request):

    aggregated = Author.objects.aggregate(
        combined_age=Coalesce(Sum('age'), Value(0)),
        combined_age_default=Sum('age')
    )

    print(aggregated['combined_age'])
    print(aggregated['combined_age_default'])

    return JsonResponse("ok", safe=False)


# def collate(request):

#     # Takes an expresssion and a collation name to query against
#     # works on django 3.2

#     authors = Author.objects.filter(name=Collate(
#         Value('john'), 'nocase'
#     ))
    
#     print(authors)


