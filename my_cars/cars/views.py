from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from .models import Car, Mark

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить машину', 'url_name': 'addcar'},
    {'title': 'Технологии', 'url_name': 'tech'},
    {'title': 'Войти', 'url_name': 'login'},
    ]


def index(request):
    cars = Car.objects.all()
    marks = Mark.objects.all()
    context = {
            'menu': menu,
            'title': 'Мои автомобили',
            'cars': cars,
            'marks': marks,
            'mark_selected': 0
            }
    return render(request, 'cars/index.html', context)


def show_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    context = {
            'menu': menu,
            'title': str(car),
            'car': car,
            'mark_selected': car_id
            }
    return render(request, 'cars/car.html', context)


def show_mark(request, mark_id):
    cars = Car.objects.filter(mark_id=mark_id)
    marks = Mark.objects.all()

    if len(cars) == 0:
        raise Http404()

    current_mark = Mark.objects.get(pk=mark_id).name
    context = {
            'menu': menu,
            'title': f'Список машин {current_mark}',
            'cars': cars,
            'marks': marks,
            'mark_selected': mark_id,
            }
    return render(request, 'cars/index.html', context)


def addcar(request):
    return HttpResponse('<h1>Добавление автомобиля</h1>')


def about(request):
    context = {
            'title': 'Об авторе',
            'menu': menu}
    return render(request, 'about/author.html', context)


def tech(request):
    context = {
            'menu': menu}
    return render(request, 'about/tech.html', context)


def login(request):
    return render('<h1>Авторизация</h1>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('Нет нихуя!')
