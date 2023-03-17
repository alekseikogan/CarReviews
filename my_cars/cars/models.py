import datetime

from django.db import models
from pkg_resources import require


class Car(models.Model):

    MARK = [
        ('Audi', 'Ауди'),
        ('BMW', 'БМВ'),
        ('Cirtoen', 'Ситроен'),
        ('Dodge', 'Додж'),
        ('Fiat', 'Фиат'),
        ('Ford', 'Форд'),
        ('Jelly', 'Джелли'),
        ('Jaguar', 'Ягуар'),
        ('Honda', 'Хонда'),
        ('Hyundai', 'Хёндэ'),
        ('KIA', 'Киа'),
        ('Lexus', 'Лексус'),
        ('Land Rover', 'Ленд Ровер'),
        ('Mersedes', 'Мерседес'),
        ('Mini', 'Мини'),
        ('Mazda', 'Мазда'),
        ('Mitsubishi', 'Митсубиси'),
        ('Nissan', 'Ниссан'),
        ('Ravon', 'Равон'),
        ('Renault', 'Рено'),
        ('Smart', 'Смарт'),
        ('Skoda', 'Шкода'),
        ('Toyota', 'Тойота'),
        ('Volkswagen', 'Фольксваген'),
        ('Volvo', 'Вольво'),
        ('Lada', 'Лада'),
        ('VAZ', 'ВАЗ'),
        ('UAZ', 'УАЗ'),
    ]

    BODY = [
        ('Hatchback', 'Хэтчбек'),
        ('Sedan', 'Седан'),
        ('SUV', 'Внедорожник'),
        ('CUV', 'Кроссовер'),
        ('Van', 'Фургон'),
        ('Coupe ', 'Купе'),
        ('Estate', 'Универсал'),
        ('Truck', 'Грузовик'),
        ('Pickup', 'Пикап'),
        ('LiftBack', 'Лифтбэк'),
    ]

    mark = models.CharField(
        max_length=50, choices=MARK, default='Марка не выбрана')
    model = models.CharField(
        max_length=100, default='Модель  не выбрана')
    complect = models.CharField(max_length=50, blank=True)
    body = models.CharField(
        max_length=50, choices=BODY, default='Кузов не выбран')
    year = models.IntegerField(default=datetime.date.today().year)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.mark} {self.model}')
