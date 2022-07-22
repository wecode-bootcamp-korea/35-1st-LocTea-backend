from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from products.models    import Product

class ProductListView(View):
    def get(self, request):
        first_category_id  = request.GET.get('first-category')
        second_category_id = request.GET.get('second-category')
        sort               = request.GET.get('sort')
        types              = request.GET.get('type')

        queries = Q()
        ordering = ''

        if not request.GET:
            queries &= Q(second_category__first_category_id=1)
            ordering = '-created_at'

        if first_category_id:
            queries &= Q(second_category__first_category_id = first_category_id)
        
        if second_category_id:
            queries &= Q(second_category = second_category_id)

        if types:
            type_queries = Q()
            
            for type in types.split(','):
                type_queries |= Q(types__name=type)

            queries &= type_queries

        if not sort or sort == 'new-arrival':
            ordering = '-created_at'
        
        elif sort == 'price-desc':
            ordering = 'price'
        
        else:
            ordering = '-price'
        
        result = []
        products = Product.objects.filter(queries).order_by(ordering).distinct()
    
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
        
