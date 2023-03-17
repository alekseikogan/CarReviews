from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect

def index(request):
    return HttpResponse('Главная страница приложения "Мои машины"')

def categories(request, cat_id):
    print(request.GET)
    return HttpResponse(f'<h1>Название категории <p>{cat_id}</p><h>')

def archive(request, year):
    if int(year) > 2023:
        return redirect('home', permanent=1)
    return HttpResponse(f'<h1>Архив по {year} году<h>')

def pageNotFound(request, exception):
    return HttpResponseNotFound('Нет нихуя!')
