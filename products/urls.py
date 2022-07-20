from django.urls    import path 

from products.views import ProductItemView, ProductListView

urlpatterns = [
    path('/<int:first_category_id>/<int:second_category_id>/<int:product_id>', ProductItemView.as_view()),
    path('/<int:first_category_id>/<int:second_category_id>', ProductListView.as_view())
]