from django.db.models import (Q, F, DateTimeField, 
    Value, ExpressionWrapper, Count, FloatField, Sum)
from django.db.models.expressions import Case, When
from django.db.models.fields import BooleanField, IntegerField
from django.db.models.functions import Concat, ExtractYear
from django.db.models.functions.comparison import Cast, Coalesce, Greatest, NullIf
from django.db.models.functions.datetime import Extract
from django.db.models.functions.text import Lower
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from app.models import Author, Blog, BloodBank, Comment, Experiment, Order, Person, Pet

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
    print(people)

    # and
    people = Person.objects.filter(Q(birth_date__lt=date_) & Q(tean=True))
    print(people)
  
    return JsonResponse('ok', safe=False)


def nested_q(request):

    # all_people = Person.objects.filter(postal_code='BB')
    all_people = Person.objects.all()
    print(all_people)

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

    print(people)

    return JsonResponse('ok', safe=False)



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
    print(people)

    return JsonResponse('ok', safe=False)



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

    print(people)

    return JsonResponse('ok', safe=False)


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
    print(people)

    people2 = Person.objects.filter(
        first_name=F('last_name')
    )  # this works too :D

    print(people2)

    return JsonResponse('ok', safe=False)


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



def greatest(request):

    """Accepts a list of at least two field names or expressions and returns the greatest value.
     Each argument must be of a similar type, so mixing text 
        and numbers will result in a database error."""
    
    blog = Blog.objects.create(body='Greatest is the best')
    comment = Comment.objects.create(body='No Least is better.', blog=blog)

    comments = Comment.objects.annotate(last_updated=Greatest(
        'modified', 'blog__modified'
    ))

    annotated_comment = comments.first()
    print(annotated_comment.id)

    return JsonResponse('ok', safe=False)



# def json_object(request):

    """Takes a list of key-value pairs and 
    returns a JSON object containing those pairs."""

    # Works on django 3.2

    # Author.objects.create(
    #     name='Mac Miller', alias='mc_miller', age=28
    # )

    # author = Author.objects.annotate(json_object=JSONObject(
    #     name=Lower('name'),
    #     alias='alias',
    #     age=F('age') * 2.
    # )).first()

    # print(author.json_object)
    # {'name': 'margaret smith', 'alias': 'msmith', 'age': 50}

    # return JsonResponse('ok', safe=False)



def least(request):

    # from django.db.models.functions import Least

    """Accepts a list of at least two field names or expressions and returns the least value.
     Each argument must be of a similar type, so mixing text and
      numbers will result in a database error."""
    
    pass


def null_if(request):

    # from django.db.models.functions import NullIf

    """Accepts two expressions and returns None 
    if they are equal, otherwise returns expression1."""

    # examle on line 202 with Coalesce



# --------------------------- Date Functions --------------------------

def extract(request):

    experiment = Experiment.objects.annotate(
        start_year=Extract('start_datetime', 'year')                  

    ).first()

    print(experiment.start_year)

    experiment = Experiment.objects.annotate(
        start_year=F('start_datetime__year')
    ).first()

    print(experiment.start_year)
    # prints whole date


    experiments_count = Experiment.objects.filter(
    start_datetime__year=Extract('end_datetime', 'year')).count()
    print(experiments_count)



    """
        lookup_name = year, month, day, week_day, iso_weekd_day and so on

    
    """
    

    return JsonResponse('ok', safe=False)


# --------------------------- Common --------------------------


def values_with_get(request):
    
    author = Author.objects.create(name="Tom", age=19)
    author_id = author.id
    
    # The values and values_list method should be callled by an queryset
    # so that is why we cannot call something like that Author.objects.get(id=2).values("name")
    # objects.get returns object not a queryset
    
    # To call values with get:
    print(Author.objects.values("name").get(id=author_id))
    
    return render(request, "home.html")


def mapping_querry(request):
    
    # Author.objects.create(name="Ben", age=32)
    
    # mapping with loop
    authors = Author.objects.all()
    authors_map = {author.pk: author for author in authors}
    print(authors_map)  # {1: 'Tom', 2: 'Ben'}
    
    
    # without loop
    authors_map = Author.objects.in_bulk()
    print(authors_map) # same result
    
    
    # possible to send id_list of objects inside in_bulk
    print(Author.objects.in_bulk(id_list=[1, 2]))
    
    return render(request, "home.html")
