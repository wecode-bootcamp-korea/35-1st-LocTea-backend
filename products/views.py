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
        tea_types          = request.GET.get('type')
        limit              = int(request.GET.get('limit', 10))
        offset             = int(request.GET.get('offset', 1))

        queries = Q()

        if not request.GET:
            queries &= Q(second_category__first_category_id=1)

        if first_category_id:
            queries &= Q(second_category__first_category_id = first_category_id)
        
        if second_category_id:
            queries &= Q(second_category = second_category_id)

        if tea_types:
            tea_type_queries = Q()
            
            for tea_type in tea_types.split(','):
                tea_type_queries |= Q(types__name=tea_type)

            queries &= tea_type_queries

        ordering = '-created_at'

        if sort == 'price-desc':
            ordering = '-price'
        
        elif sort == 'price-asc':
            ordering = 'price'
        
        result = []
        products = Product.objects.filter(queries).order_by(ordering).distinct()
        
        p = Paginator(products, limit)
        pages_count = p.num_pages

        if offset < 1 or offset > pages_count:
            return JsonResponse({'result': 'INVALID_PAGE'}, status=404)

        result.append({
            'total_items' : products.count(),
            'total_pages' : pages_count,
            'current_page': offset,
            'limit'       : limit
            })

        page_items = p.page(offset) 
        for page_item in page_items:
            result.append({
                'id'              : page_item.id,
                'title'           : page_item.title,
                'price'           : int(page_item.price),
                'stock'           : page_item.stock,
                'thumbnail_images': [image.url for image in page_item.thumbnail_images.all()],
                'types'           : [type.name for type in page_item.types.all()]
            })

        return JsonResponse({'result': result}, status=200)
        
