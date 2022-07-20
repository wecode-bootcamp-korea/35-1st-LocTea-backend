from django.urls    import path 

from products.views import ProductItemView, ProductListView

urlpatterns = [
    path('/<str:first_category>/<str:second_category>/<int:product_id>', ProductItemView.as_view()),
    path('/<str:first_category>/<str:second_category>', ProductListView.as_view())
]