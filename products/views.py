from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from products.models    import Product
from categories.models  import SecondCategory

class ProductListView(View):
    def get(self, request):
        category_id = request.GET['category']
        if not SecondCategory.objects.filter(id=category_id).exists():
            return JsonResponse({'result': 'INVALID_CATEGORY'}, status=404)

        result = []
        
        products = Product.objects.filter(second_category_id=category_id)
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
    