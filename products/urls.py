from django.urls    import path 

from products.views import ProductItemView, ProductListView

urlpatterns = [
    path('/<int:product_id>', ProductItemView.as_view()),
    path('/list', ProductListView.as_view())
]