from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator

from products.models    import Product
from categories.models  import SecondCategory

class ProductItemView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            result = {
                'id'              : product_id,
                'title'           : product.title,
                'description'     : product.description,
                'first_category'  : product.second_category.first_category.title,
                'second_category' : product.second_category.title,
                'price'           : product.price,
                'stock'           : product.stock,
                'discount'        : product.discount,
                'thumbnail_images': [image.url for image in product.thumbnail_images.all()],
                'detail_images'   : [image.url for image in product.detail_images.all()]
            }

            return JsonResponse({'result': result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_PRODUCT'}, status = 404)

        except SecondCategory.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_SECOND_CATEGORY'}, status = 404)

class ProductListView(View):
    def get(self, request):
        limit              = int(request.GET.get("limit", 10))
        offset             = int(request.GET.get("offset", 1))
        first_category_id  = request.GET.get('first-category', 1)
        second_category_id = request.GET.get('second-category')
        sort               = request.GET.get('sort')
        tea_types          = request.GET.getlist('type')

        if first_category_id:
            queries = Q(second_category__first_category_id = first_category_id)

        elif second_category_id:
            queries = Q(second_category = second_category_id)

        if tea_types:
            queries &= Q(types__name__in = tea_types)
        
        sort_dict = {
            'price-desc' : '-price', 
            'price-asc'  : 'price' 
        }

        ordering = sort_dict.get(sort, '-created_at')

        products = Product.objects.filter(queries).order_by(ordering).distinct()
        
        p = Paginator(products, limit)
        pages_count = p.num_pages

        if offset < 1 or offset > pages_count:
            return JsonResponse({'result': 'INVALID_PAGE'}, status=404)

        total = {
            'total_items' : products.count(),
            'total_pages' : pages_count,
            'current_page': offset,
            'limit'       : limit
        }
        
        page_items = p.page(offset) 
        products = [{
            'id'              : page_item.id,
            'title'           : page_item.title,
            'price'           : page_item.price,
            'stock'           : page_item.stock,
            'thumbnail_images': [image.url for image in page_item.thumbnail_images.all()],
            'types'           : [type.name for type in page_item.types.all()]
        } for page_item in page_items]

        return JsonResponse({'total' : total, 'products': products}, status=200)
        
