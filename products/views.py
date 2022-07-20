from django.http        import JsonResponse
from django.views       import View

from products.models    import Product, ThumbnailImage, DetailImage
from categories.models  import FirstCategory, SecondCategory

class ProductItemView(View):
    # 형식 /products/first_category_name/second_category_name/product_id
    # 예시 127.0.0.1:8000/products/tea-products/greentea/2
    # http -v GET 127.0.0.1:8000/products/tea-products/greentea/2
    def get(self, request, **kwargs):
        try:
            product_id = kwargs['product_id']
            product = Product.objects.get(id=product_id)

            result = {
                'title'           : product.title,
                'description'     : product.description,
                'first_category'  : kwargs['first_category'],
                'second_category' : kwargs['second_category'],
                'price'           : product.price,
                'stock'           : product.stock,
                'discount'        : product.discount,
                'thumbnail_images': [image.url for image in product.thumbnail_images.all()],
                'detail_images'   : [image.url for image in product.detail_images.all()]
            }

            return JsonResponse({'result': result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_PRODUCT'}, status = 401)

        except SecondCategory.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_SECOND_CATEGORY'}, status = 401)

class ProductListView(View):
    # 티 제품 / 녹차 말차 카테고리 get
    # http -v GET 127.0.0.1:8000/products/1/2
    def get(self, request, **kwargs):
        products = Product.objects.filter(second_category_id=kwargs['second_category_id'])
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