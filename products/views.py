from django.http        import JsonResponse
from django.views       import View

from products.models    import Product, ThumbnailImage, DetailImage
from categories.models  import FirstCategory, SecondCategory

class ProductItemView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            second_category = SecondCategory.objects.get(id=product.second_category.id)

            result = {
                'title'           : product.title,
                'description'     : product.description,
                'first_category'  : second_category.first_category.title,
                'second_category' : second_category.title,
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