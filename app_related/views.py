from django.db.models.query import Prefetch
from django.shortcuts import render

from app_related.models import Customer, LineItem, Order, Product


def select_related(request):

    orders = Order.objects.select_related('customer').all()

    for order in orders:
        temp = order.customer
        # foreign key relation

    # Select Realated reduces count of queries in foreign key relationships
    return render(request, 'home.html')


def prefetch_related(request):

    orders = Order.objects.prefetch_related('products').all()

    for order in orders:
        a = [product.name for product in order.products.all()]
        # many to many relation

    # Fetch related reduces count of queries in ManytoMany relatons
    return render(request, 'home.html')


def prefetch_filter(request):

    qs = Order.objects.prefetch_related('products').all()

    orders = []
    for order in qs:

        products =  [product.name for product in order.products.filter(price__range=(10, 25))]
        orders.append({'id': order.id, 'name': order.name, 'products': products})


    # In this case count of querysets is increased,
    #  because filter makes Django to change primary query
    # and it can not JOIN right results for use

    """
        To solve that we can use prefetch and filter together as in the newxt view below 
    """

    return render(request, 'home.html')


def filter_prefect(request):

    qs = Order.objects.prefetch_related(
        Prefetch('products', queryset=Product.objects.filter(price__range=(10, 25)))
    )

    orders = []
    for order in qs:

        products =  [product.name for product in order.products.all()]
        orders.append({'id': order.id, 'name': order.name, 'products': products})
    

    # I this case amount of queries should be reduce to 2.

    return render(request, 'home.html')
