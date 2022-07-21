from django.urls    import path 

from products.views import ProductItemView

urlpatterns = [
    path('/<int:product_id>', ProductItemView.as_view())
]