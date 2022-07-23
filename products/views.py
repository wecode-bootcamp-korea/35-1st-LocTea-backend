from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator

from products.models    import Product

class ProductListView(View):
    def get(self, request):
        first_category_id  = request.GET.get('first-category')
        second_category_id = request.GET.get('second-category')
        sort               = request.GET.get('sort')
        types              = request.GET.get('type')
        limit              = request.GET.get('limit', 10)
        offset             = request.GET.get('offset', 1)

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
        
        products = Product.objects.filter(queries).order_by(ordering).distinct()
        
        p = Paginator(products, limit)
        page_items = p.page(offset) # Emptypage인 경우 handling하기
        result = []
        
        for page_item in page_items:
            result.append({
                'id'              : page_item.id,
                'title'           : page_item.title,
                'price'           : page_item.price,
                'stock'           : page_item.stock,
                'thumbnail_images': [image.url for image in page_item.thumbnail_images.all()],
                'types'           : [type.name for type in page_item.types.all()]
            })

        return JsonResponse({'result': result}, status=200)
        
