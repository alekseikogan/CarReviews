from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AddCarForm, LoginUserForm, RegisterUserForm
from .models import Car, Mark

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить машину', 'url_name': 'addcar'},
    {'title': 'Технологии', 'url_name': 'tech'},
]


class CarHome(ListView):
    paginate_by = 4
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    extra_context = {
        'title_low': 'Список авто, на которых я катался',
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
        return Car.objects.all()


class MarkList(ListView):
    model = Car
    template_name = 'cars/index.html'
    context_object_name = 'cars'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        current_mark = get_object_or_404(
            Mark, slug=self.kwargs['mark']).name
        context['title_up'] = f'Автомобили марки {current_mark}'
        context['title_low'] = f'Автомобили марки {current_mark}'
        context['menu'] = menu
        context['marks'] = Mark.objects.all()
        context['mark_selected'] = self.kwargs['mark']
        return context

    def get_queryset(self):
        return Car.objects.filter(mark__slug=self.kwargs['mark'])


class ShowCar(DetailView):
    model = Car
    template_name = 'cars/car.html'
    slug_url_kwarg = 'car'
    context_object_name = 'car'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        current_car = get_object_or_404(Car, slug=self.kwargs['car'])
        context['title_up'] = f'{str(current_car.mark)} {str(current_car.model)}'
        context['title_low'] = f'{str(current_car.mark)} {str(current_car.model)}'
        context['menu'] = menu
        context['marks'] = Mark.objects.all()
        context['mark_selected'] = current_car.mark.slug
        return context


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
    marks = Mark.objects.all() 
    context = {
        'title': 'Об авторе',
        'menu': menu,
        'marks': marks
    }
    return render(request, 'about/author.html', context)


def tech(request):
    marks = Mark.objects.all()
    context = {
        'title': 'Об авторе',
        'menu': menu,
        'marks': marks
    }
    return render(request, 'about/tech.html', context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Упс! Такой страницы не существует!</h1>')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'cars/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        context['title_up'] = 'Регистрация'
        context['title_low'] = 'Давайте знакомиться'
        marks = Mark.objects.all()
        context['menu'] = menu
        context['marks'] = marks
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'cars/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        '''Создание динамического контекста'''
        context = super().get_context_data(**kwargs)
        context['title_up'] = 'Вход'
        context['title_low'] = 'Авторизация'
        marks = Mark.objects.all()
        context['menu'] = menu
        context['marks'] = marks
        return context

    def get_success_url(self):
        return reverse_lazy('home')
