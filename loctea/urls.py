from django.urls import path, include

urlpatterns = [
    path('categories', include('categories.urls')),
    path('products', include('products.urls')),
]
