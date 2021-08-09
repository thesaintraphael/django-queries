from django.db.models.aggregates import Max
from django.db.models.fields import FloatField
from django.db.models import Avg, Count, Q, F
from django.http import JsonResponse
from agg.models import Book, Publisher


BOOKS = Book.objects.all()


def average_price(request):


    avg_price = BOOKS.aggregate(Avg('price'))
    print(avg_price)

    # format {'price__avg': Decimal('25.4950000')}
    # price is set to Decimal, dat is why average also is Decimal
    # returns None (not zero!) if there is no any price


    max_price = BOOKS.aggregate(Max('price'))
    print(max_price)
    # format same as previous


    return JsonResponse('ok', safe=False)


def max_and_avg(request):

    price_dif = Book.objects.aggregate(
        price_diff=Max('price', output_field=FloatField()) - Avg('price', output_field=FloatField())
    )

    print(price_dif)

    # difference between Max and average

    return JsonResponse('ok', safe=False)


def count_things(request):

    # Each publisher, each with a count of books as a "num_books" attribute

    pubs = Publisher.objects.annotate(
        num_books=Count('book')
    )
    print(pubs)

    # Each publisher, with a separate count of books with a rating above and below 5
    above_5 = Count('book', filter=Q(book__rating__gt=5))
    below_5 = Count('book', filter=Q(book__rating__lte=5))
    pubs = Publisher.objects.annotate(below_5=below_5).annotate(above_5=above_5)
    
    for pub in pubs:
        print(pub.above_5, pub.below_5)

    # The top 5 publishers, in order by number of books
    pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
    print(pubs)
    

    return JsonResponse('ok', safe=False)
    

def ann_and_agg(request):

    # Trying annotate and aggregate togheter
    
    max_double_price = Book.objects.annotate(double_price=F('price')*2).aggregate(Max('double_price'))
    print(max_double_price)

    # works as same as with normal fields of a model

    return JsonResponse('ok', safe=False)
