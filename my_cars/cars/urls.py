from cars.views import AddCar, CarHome, MarkList, ShowCar, about, tech
from django.urls import path, include
from my_cars import settings
from .views import LoginUser, RegisterUser, logout_user
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', CarHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addcar/', AddCar.as_view(), name='addcar'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('tech/', tech, name='tech'),
    path('cars/<slug:car>/', ShowCar.as_view(), name='show_car'),
    path('mark/<slug:mark>/', MarkList.as_view(), name='show_mark'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')),]