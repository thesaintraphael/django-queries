from django.db.models.aggregates import Sum
from django.db.models.fields import FloatField
from django.db.models import Avg, Max, Min, Count, Q, F
from django.http import JsonResponse
from agg.models import Author, Book, Publisher, Store


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

    return render(request, "home.html")


def max_and_avg(request):
    
    # difference between Max and average
    price_dif = Book.objects.aggregate(
        price_diff=Max('price', output_field=FloatField()) - Avg('price', output_field=FloatField())
    )

    print(price_dif)

    
    price_and_rating = Book.objects.aggregate(Avg('price'), Avg('rating'), Max('price'), Max('rating'), Min('price'), Min('rating'))

    print(price_and_rating)
    # result: {'price__avg': Decimal('25.4950000000000'), 
    # 'rating__avg': 9.25, 'price__max': Decimal('35.9900000000000'), 
    # 'rating__max': 9.5, 'price__min': Decimal('15'), 'rating__min': 9.0}

    return render(request, "home.html")


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
    

    return render(request, "home.html")
    

def ann_and_agg(request):

    # Trying annotate and aggregate togheter
    
    max_double_price = Book.objects.annotate(double_price=F('price')*2).aggregate(Max('double_price'))
    print(max_double_price)

    # works as same as with normal fields of a model

    return render(request, "home.html")


def aggreagate_for_each(request):

    book_authors = Book.objects.annotate(Count('authors'))
    # Book ===> Authors ===> manytomanyfield

    for book_author in book_authors:

        print(book_author.count_of_authors)

    return render(request, "home.html")


def distinct(request):

    books = Book.objects.annotate(Count('authors', distinct=True), 
    Count('store', distinct=True))

    print(books[0].authors__count)
    print(books[0].store__coint)

    # without distict annotate yield wrong results. Distinct only work for Count
    # so we can not aggregate multiple fields in annotate


def join_aggreagate(request):

    prices = Store.objects.aggregate(min_price=Min('books__price'), max_price=Max('books__price'))
    print(prices)
    # return max and min prices of books that are in the Store

    stores = Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))
    print(stores)
    # return queryset of Store with min and max for each store

    for store in stores:
        print(store.min_price, store.max_price)
    

    # Process of joing Store and Book models

    return render(request, "home.html")


def sum_pages(request):

    authors = Author.objects.annotate(
        total_pages=Sum('book__pages')
    ).values_list('name', 'total_pages').order_by('total_pages')

    print(authors)

    return render(request, "home.html")


# Aggreation and other QS clauses

def filter_ag(request):

    books = Book.objects.filter(name__startswith='H').annotate(
        num_authors=Count('authors')
    ).values_list('name', 'num_authors')

    print(books)

    books = Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)
    print(books)

    # If you need two annotations with two separate filters you can use the filter
    #  argument with any aggregate. For example, to generate a list of authors with 
    # a count of highly rated books:

    highly_rated = Count('book', filter=Q(book__rating__gte=7))
    authors = Author.objects.annotate(num_count=Count('book'), 
    highly_rated_books=highly_rated).values_list('name', 'num_count', 'highly_rated_books')

    print(authors)

    return render(request, "home.html")


def aggregate_annotaions(request):

    # 1. Count number of authors for each book
    # 2. Find average for all of them

    num_authors_avg = Book.objects.annotate(
        num_authors=Count('authors')
    ).aggregate(Avg('num_authors'))

    print(num_authors_avg)

    return render(request, "home.html")
