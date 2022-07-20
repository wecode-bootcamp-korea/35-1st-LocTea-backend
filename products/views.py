from django.http        import JsonResponse
from django.views       import View

from products.models    import Product, ThumbnailImage, DetailImage
from categories.models  import FirstCategory, SecondCategory

class ProductListView(View):
    # http -v GET 127.0.0.1:8000/products/1/2
    def get(self, request, **kwargs):
        products = Product.objects.filter(second_category_id=kwargs['second_category_id'])
        result = []
        for product in products:
            result.append({
                'id'              : product.id,
                'title'           : product.title,
                'price'           : product.price,
                'stock'           : product.stock,
                'thumbnail_images': [image.url for image in product.thumbnail_images.all()],
                'types'           : [type.name for type in product.types.all()]
            })
        return JsonResponse({'result': result}, status=200)