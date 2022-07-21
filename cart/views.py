import json
from json.decoder           import JSONDecodeError

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import MultipleObjectsReturned

from cart.models            import Cart
from users.models           import User
from products.models        import Product

class CartView(View) :
    #데코레이터
    def post(self, request) :
        try :
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            quantity   = data['quantity']


            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'PRODUCT_NOT_EXIST'}, status=400)

            if quantity <= 0:
                return JsonResponse({'message':'QUANTITY_ERROR'}, status=400)
        
            cart, is_created  = Cart.objects.get_or_create(
                user       = user,
                product_id = product_id
            )
            cart.quantity += quantity
            cart.save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except Cart.DoesNotExist :
            return JsonResponse({'message':'INVALID_CART'}, status=400)
        except JSONDecodeError :
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


    def get(self, request):
        user = request.user

        if not Cart.objects.filter(user=user).exists():
            return JsonResponse({'message':'USER_CART_NOT_EXIST'}, status=400)

        carts = Cart.objects.filter(user=user)
        
        result = [{
            'user_id'   : user,
            'cart_id'   : cart.id,
            'product_id': cart.product.id,
            'title'     : cart.product.title,
            'quantity'  : cart.quantity,
            'price'     : cart.product.price,
            'image'     : cart.product.thumbnailimage_set.get().image_url
        } for cart in carts]

        return JsonResponse({"result":result}, status = 200)

    def delete(self, request):
        try:    
            user    = request.user
            cart_id = request.GET.get('id')

            if not Cart.objects.get(id=cart_id, user=user).exist():
                return JsonResponse({'message':'INVAILD_CART_ID'}, status=404)

            cart = Cart.objects.get(id=cart_id, user=user)

            cart.delete()
            return JsonResponse({'message':'DELETED'}, status=200)

        except MultipleObjectsReturned :
            return JsonResponse({'message':'MULTIPLE_OBJECTS_RETURNED'}, status=400)
        except ValueError :
            return JsonResponse({'message':'VAULE_ERROR'}, status=400)

    def patch(self, request) :
        try :
            data     = json.loads(request.body)
            user     = request.user
            cart_id  = request.GET.get('id')
            quantity = data['quantity']

            if not Cart.objects.filter(id=cart_id, user=user).exists():
                return JSONDecodeError({'message':'INVALID_CART_ID'}, status=404)

            if quantity <= 0:
                return JSONDecodeError({'message':'QUANTITY_ERROR'}, status=400)

            cart = Cart.objects.get(id=cart_id, user=user)

            cart.quantity = data['quantity']
            cart.save()
            return JsonResponse({'quantity':cart.quantity}, status=200)

        except MultipleObjectsReturned:
            return JSONDecodeError({'message':'MULTIPLE_OBJECT_RETURNED'}, status=400)
        except ValueError :
            return JSONDecodeError({'message':'VALUE_ERROR'}, status=400)