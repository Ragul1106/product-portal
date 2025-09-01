from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product

def product_list(request):
    search_query = request.GET.get("q", "")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    availability = request.GET.get("availability", "")

    products = Product.objects.all().order_by("name")

    # 🔍 Search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

    # 💰 Price filter
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # ✅ Availability filter
    if availability:
        if availability == "available":
            products = products.filter(is_available=True)
        elif availability == "unavailable":
            products = products.filter(is_available=False)

    # 📊 Pagination
    paginator = Paginator(products, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "min_price": min_price or "",
        "max_price": max_price or "",
        "availability": availability,
        "total_results": products.count(),
    }
    return render(request, "products/product_list.html", context)
