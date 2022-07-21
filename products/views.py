from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from products.models    import Product
from categories.models  import SecondCategory

class ProductListView(View):
    '''
    1. 쿼리 파라미터가 없는 경우 : /products/list
        1) '티 제품(1차 카테고리, id 1)' 카테고리에 속한 상품 전체를 보여줌
        2) 24개만 보여줌, 신상품순으로 보여줌, 전체 타입 보여줌
    2. 1차 카테고리를 선택한 경우 : /products/list?first-category=1
        1) 해당 카테고리에 속한 상품 전체를 보여줌
        2) 24개만 보여줌, 신상품순으로 보여줌, 전체 타입 보여줌(티 제품을 선택한 경우)
    3. 2차 카테고리를 선택한 경우 : /products/list?second-category=1
        1) 해당 카테고리에 속한 상품 전체를 보여줌
        2) 24개만 보여줌, 신상품순으로 보여줌, 전체 타입 보여줌(티 제품을 선택한 경우)
    4. 1차 필터를 선택한 경우 : /products/list?first-category=1&sort=new-arrival
        1)  

    '''
    def get(self, request):
        category_id = request.GET['second-category']
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
    
