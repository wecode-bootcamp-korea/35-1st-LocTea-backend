from django.http  import JsonResponse
from django.views import View 

from categories.models       import FirstCategory

class CategoryView(View): 
    # http -v GET 127.0.0.1:8000/categories
    def get(self, request):
        try:
            first_categories = FirstCategory.objects.all()
            result = {}

            for first_category in first_categories:
                second_categories = first_category.second_categories.all()
                result[first_category.title] = [second_category.title for second_category in second_categories]
        
            return JsonResponse({'result' : result}, status=200)

        except:
            return JsonResponse({'result' : 'INVALID_REQUEST'}, status=404)
