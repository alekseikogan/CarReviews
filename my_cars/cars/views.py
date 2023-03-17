from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import Car

menu = ['О сайте', 'Добавить машину', 'Обратная связь', 'Войти']


def index(request):
    cars = Car.objects.all()
    return render(
        request, 'cars/index.html', {
            'menu': menu,
            'title': 'Главная страница',
            'cars': cars
            }
        )


def about(request):
    return render(
        request, 'about/author.html', {
            'title': 'Об авторе',
            'menu': menu}
        )


def categories(request, cat_id):
    print(request.GET)
    return HttpResponse(f'<h1>Название категории <p>{cat_id}</p><h>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('Нет нихуя!')
