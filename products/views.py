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
    # 형식 /products/first_category/second_category
    # 예시 127.0.0.1:8000/products/tea-products/greentea/
    # http -v GET 127.0.0.1:8000/products/tea-products/greentea
    def get(self, request, **kwargs):
        
        return JsonResponse({'result': 1}, status=200)