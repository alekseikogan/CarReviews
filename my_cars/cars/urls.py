from django.urls import path

from cars.views import categories, index, about

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('cats/<int:cat_id>/', categories),
]
