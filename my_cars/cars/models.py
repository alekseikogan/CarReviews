import datetime

from django.db import models
from pkg_resources import require


class Car(models.Model):

    MARK = [
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('Cirtoen', 'Cirtoen'),
        ('Dodge', 'Dodge'),
        ('Fiat', 'Fiat'),
        ('Ford', 'Ford'),
        ('Jelly', 'Jelly'),
        ('Jaguar', 'Jaguar'),
        ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'),
        ('KIA', 'KIA'),
        ('Lexus', 'Lexus'),
        ('Land Rover', 'Land Rover'),
        ('Mersedes', 'Mersedes'),
        ('Mini', 'Mini'),
        ('Mazda', 'Mazda'),
        ('Mitsubishi', 'Mitsubishi'),
        ('Nissan', 'Nissan'),
        ('Ravon', 'Ravon'),
        ('Renault', 'Renault'),
        ('Smart', 'Smart'),
        ('Skoda', 'Skoda'),
        ('Toyota', 'Toyota'),
        ('Volkswagen', 'Volkswagen'),
        ('Volvo', 'Volvo'),
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
        max_length=100, default='Модель не выбрана')
    complect = models.CharField(max_length=50, blank=True)
    body = models.CharField(
        max_length=50, choices=BODY, default='Кузов не выбран')
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField(default=datetime.date.today().year)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.mark} {self.model}')
