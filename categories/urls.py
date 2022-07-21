from django.urls      import path 

from categories.views import CategoryView

urlpatterns = [
    path('', CategoryView.as_view()),
]