from django.http        import JsonResponse
from django.views       import View

from products.models    import Product

class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter(second_category_id=request.GET['category'])
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
    