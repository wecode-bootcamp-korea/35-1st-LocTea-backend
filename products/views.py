from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from products.models    import Product

class ProductListView(View):
    def get(self, request):
        first_category_id  = request.GET.get('first-category', None)
        second_category_id = request.GET.get('second-category', None)
        sort               = request.GET.get('sort', None)
        types              = request.GET.get('type', None)

        filter_queries = Q()
        order_string = ''

        if not request.GET:
            filter_queries &= Q(second_category__first_category_id=1)

        if first_category_id:
            filter_queries &= Q(second_category__first_category_id = first_category_id)
        
        if second_category_id:
            filter_queries &= Q(second_category = second_category_id)

        if types:
            type_queries = Q()
            
            for type in types.split(','):
                type_queries |= Q(types__name=type)

            filter_queries &= type_queries

        if not sort or sort == 'new-arrival':
            order_string = '-created_at'
        
        elif sort == 'price-desc':
            order_string = 'price'
        
        else:
            order_string = '-price'
        
        result = []
        products = Product.objects.filter(filter_queries).order_by(order_string).distinct()
    
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
        
