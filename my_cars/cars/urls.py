from django.urls import path, re_path

from cars.views import categories, index, archive

urlpatterns = [
    path('', index, name='home'),
    path('cats/<int:cat_id>/', categories),
    re_path(r'^archive/(?P<year>[0-9]{4})', archive),
]
