from itertools import product
from django.http        import JsonResponse
from django.views       import View
from products.models    import Product, ThumbnailImage, DetailImage

class ProductItemView(View):
    # http -v GET 127.0.0.1:8000/products/2
    def get(self, request, **kwargs):
        product_id = kwargs['product_id']
        return JsonResponse({'message': product_id}, status=200)