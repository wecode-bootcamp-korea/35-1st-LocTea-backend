from django.urls import path, include

urlpatterns = [
    path('categories', include('categories.urls')),
    path('products', include('products.urls')),
    path('users', include('users.urls')),
    path('cart', include('cart.urls'))
]