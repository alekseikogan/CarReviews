from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from pytest import mark

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


def show_car(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    marks = Mark.objects.all()
    context = {
            'car': car,
            'menu': menu,
            'title': car,
            'marks': marks,
            'mark_selected': car.mark.slug
            }
    return render(request, 'cars/car.html', context)


def show_mark(request, mark_slug):
    marks = Mark.objects.all()
    marks_forslug = Mark.objects.filter(slug=mark_slug)
    cars = Car.objects.filter(mark=marks_forslug[0].id)

    if len(cars) == 0:
        raise Http404()

    current_mark = get_object_or_404(Mark, slug=mark_slug).name
    context = {
            'menu': menu,
            'title': f'Список машин марки {current_mark}',
            'cars': cars,
            'marks': marks,
            'mark_selected': mark_slug,
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
