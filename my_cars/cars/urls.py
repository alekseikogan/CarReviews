from cars.views import AddCar, CarHome, MarkList, ShowCar, about, tech
from django.urls import path

from .views import LoginUser, RegisterUser

urlpatterns = [
    path('', CarHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addcar/', AddCar.as_view(), name='addcar'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('tech/', tech, name='tech'),
    path('cars/<slug:car>/', ShowCar.as_view(), name='show_car'),
    path('mark/<slug:mark>/', MarkList.as_view(), name='show_mark'),
]
