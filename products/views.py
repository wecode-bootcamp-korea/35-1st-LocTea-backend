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
        limit              = request.GET.get("limit", 10)
        offset             = request.GET.get("offset", 1)
        first_category_id  = request.GET.get('first-category')
        second_category_id = request.GET.get('second-category')
        sort               = request.GET.get('sort')
        tea_types          = request.GET.getlist('type')

        queries  = Q(second_category__first_category_id = 1)

        if first_category_id:
            queries = Q(second_category__first_category_id = first_category_id)

        if second_category_id:
            queries = Q(second_category = second_category_id)

        if tea_types:
            tea_type_queries = Q()
            tea_type_queries |= Q(types__name__in = tea_types)
            queries &= tea_type_queries

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
        
        products = []
        page_items = p.page(offset) 
        for page_item in page_items:
            products.append({
                'id'              : page_item.id,
                'title'           : page_item.title,
                'price'           : page_item.price,
                'stock'           : page_item.stock,
                'thumbnail_images': [image.url for image in page_item.thumbnail_images.all()],
                'types'           : [type.name for type in page_item.types.all()]
            })

        return JsonResponse({'total' : total, 'products': products}, status=200)
            




            

# get이랑 query parameter 사용하기
# 이번 주 인기 제품 & 여름맞이 선물은 하나의 view에서 query parameter로 묶기...?
# 인기 & 여름맞이 = 제품 7개 (사진, 제품이름, 가격 필요) (but, 여름맞이는 아이스티만))

#오늘만 이 가격 = 제품 1개 (사진, 제품이름, 가격, 할인율 필요)
# product 칸에서 할인률 높은 거 하나 뽑아서 보내주기

class SevenProductView(View): 
    def get(self, request): 
        summer = Product.objects.second_category_id(Q(id=5)|Q(id=8)).order_by(모르겠다)[:7]
        week   = Product.objects.all().order_by(모르겠따)[:7]

        result_summer  = {
                'id'              : summer.id,
                'title'           : summer.title,
                'description'     : summer.description,
                'first_category'  : summer.second_category.first_category.title,
                'second_category' : summer.second_category.title,
                'price'           : summer.price,
                'stock'           : summer.stock,
                'discount'        : summer.discount,
                'thumbnail_images': [image.url for image in summer.thumbnail_images.all()],
                'detail_images'   : [image.url for image in summer.detail_images.all()]
            }
        
        result_week     = {
                'id'              : week.id,
                'title'           : week.title,
                'description'     : week.description,
                'first_category'  : week.second_category.first_category.title,
                'second_category' : week.second_category.title,
                'price'           : week.price,
                'stock'           : week.stock,
                'discount'        : week.discount,
                'thumbnail_images': [image.url for image in week.thumbnail_images.all()],
                'detail_images'   : [image.url for image in week.detail_images.all()]
            }

        return JsonResponse({'summer' : result_summer,'week' : result_week}, status = 200)

    # except Product.DoesNotExist:
    #     return JsonResponse({'message' : 'INVALID_PRODUCT'}, status = 404)

    # except SecondCategory.DoesNotExist:
    #     return JsonResponse({'message' : 'INVALID_SECOND_CATEGORY'}, status = 404)

class TodayProductView(View): 
    def get(self, request): 
        today             = Product.objects.all().order_by('-discount')[:1]

        result_today      = {
                'id'              : today.id,
                'title'           : today.title,
                'description'     : today.description,
                'first_category'  : today.second_category.first_category.title,
                'second_category' : today.second_category.title,
                'price'           : today.price,
                'stock'           : today.stock,
                'discount'        : today.discount,
                'thumbnail_images': [image.url for image in today.thumbnail_images.all()],
                'detail_images'   : [image.url for image in today.detail_images.all()]
            }
        return JsonResponse({'today' : result_today}, status = 200)