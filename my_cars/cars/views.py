from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddCarForm
from .models import Car, Mark

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить машину', 'url_name': 'addcar'},
    {'title': 'Технологии', 'url_name': 'tech'},
    {'title': 'Войти', 'url_name': 'login'},
    ]


# def index(request):
#     cars = Car.objects.order_by('?')[:5]
#     marks = Mark.objects.all()
#     context = {
#             'menu': menu,
#             'title': 'Мои автомобили',
#             'cars': cars,
#             'marks': marks,
#             'mark_selected': 0
#             }
#     return render(request, 'cars/index.html', context)


class CarHome(ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    extra_context = {
        'title_low': '5 случайных автомобилей',
        'title_up': 'Мои автомобили'
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        marks = Mark.objects.all()
        context['menu'] = menu
        context['marks'] = marks
        context['mark_selected'] = 0
        return context

    def get_queryset(self):
        return Car.objects.order_by('?')[:5]


# def show_mark(request, mark_slug):
#     marks = Mark.objects.all()
#     marks_forslug = Mark.objects.filter(slug=mark_slug)
#     cars = Car.objects.filter(mark=marks_forslug[0].id)

#     if len(cars) == 0:
#         raise Http404()

#     current_mark = get_object_or_404(Mark, slug=mark_slug).name
#     context = {
#             'menu': menu,
#             'title': f'Список машин марки {current_mark}',
#             'cars': cars,
#             'marks': marks,
#             'mark_selected': mark_slug,
#             }
#     return render(request, 'cars/index.html', context)


class MarkList(ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        marks = Mark.objects.all()
        current_mark = get_object_or_404(
            Mark, slug=self.kwargs["mark_slug"]).name
        context['title_up'] = f'Автомобили марки {current_mark}'
        context['title_low'] = f'Автомобили марки {current_mark}'
        context['menu'] = menu
        context['marks'] = marks
        context['mark_selected'] = self.kwargs['mark_slug']
        return context

    def get_queryset(self):
        return Car.objects.filter(mark__slug=self.kwargs['mark_slug'])


# def show_car(request, car_slug):
#     car = get_object_or_404(Car, slug=car_slug)
#     marks = Mark.objects.all()
#     context = {
#             'car': car,
#             'menu': menu,
#             'title': car,
#             'marks': marks,
#             'mark_selected': car.mark.slug
#             }
#     return render(request, 'cars/car.html', context)


class ShowCar(DetailView):
    model = Car
    template_name = 'cars/car.html'
    slug_url_kwarg = 'car_slug'
    context_object_name = 'car'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        current_car = get_object_or_404(Car, slug=self.kwargs['car_slug'])
        context['title_up'] = f'{str(current_car.mark)} {str(current_car.model)}'
        context['title_low'] = f'{str(current_car.mark)} {str(current_car.model)}'
        context['menu'] = menu
        context['marks'] = Mark.objects.all()
        context['mark_selected'] = current_car.mark.slug
        return context


# def addcar(request):
#     if request.method == 'POST':
#         form = AddCarForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddCarForm()
#     context = {
#             'title': 'Добавление автомобиля',
#             'menu': menu,
#             'form': form}
#     return render(request, 'cars/addcar.html', context)


class AddCar(CreateView):
    form_class = AddCarForm
    template_name = 'cars/addcar.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        context['title_up'] = 'Добавление автомобиля'
        context['title_low'] = 'На чем катался?'
        context['menu'] = menu
        context['marks'] = Mark.objects.all()
        return context


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
