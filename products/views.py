from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from products.models    import Product
from categories.models  import SecondCategory

class ProductListView(View):
    def get(self, request):
        first_category_id  = request.GET.get('first-category', None)
        second_category_id = request.GET.get('second-category', None)
        sort               = request.GET.get('sort', None)
        type               = request.GET.get('type', None)

        q = Q()

        '''
        # 쿼리 파라미터가 없는 경우 
        if not request.GET:
            # 1차 카테고리 아이디 1번에 속한 모든 제품을 신상품 순으로 보여줌 
            q = Q(second_category__first_category_id=1).order_by('-created_at')
        '''
        # 1차 카테고리를 선택한 경우
        if first_category_id:
            q &= Q(second_category__first_category_id = first_category_id)
        
        # 2차 카테고리를 선택한 경우
        if second_category_id:
            q &= Q(second_category = second_category_id)

        result = []
        products = Product.objects.filter(q)
    
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
        
