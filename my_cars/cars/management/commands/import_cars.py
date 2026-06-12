from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cars.models import Body, Car, Mark


def _cars_missing_photo_files():
    media_cars = Path(settings.MEDIA_ROOT) / 'cars'
    missing = 0
    for car in Car.objects.only('slug'):
        if not (media_cars / f'{car.slug}.jpg').exists():
            missing += 1
    return missing


class Command(BaseCommand):
    help = 'Импорт данных из fixtures/cars.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--input',
            default='fixtures/cars.json',
            help='Путь к fixture относительно my_cars/',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Очистить таблицы и импортировать заново',
        )
        parser.add_argument(
            '--skip-photos',
            action='store_true',
            help='Не привязывать локальные фото после импорта',
        )

    def handle(self, *args, **options):
        input_path = Path(options['input'])
        if not input_path.is_absolute():
            input_path = Path(__file__).resolve().parents[3] / input_path

        if not input_path.exists():
            self.stdout.write(self.style.ERROR(f'Файл не найден: {input_path}'))
            self.stdout.write('Запустите: python manage.py generate_fixture')
            return

        if Car.objects.exists() and not options['force']:
            self.stdout.write(self.style.WARNING(
                'Данные уже есть. Используйте --force для перезагрузки',
            ))
            call_command('download_car_photos', '--link-only')
            missing = _cars_missing_photo_files()
            if missing:
                self.stdout.write(f'Скачивание отсутствующих фото ({missing})...')
                call_command('download_car_photos')
            return

        if options['force']:
            Car.objects.all().delete()
            Mark.objects.all().delete()
            Body.objects.all().delete()
            self.stdout.write(self.style.WARNING('Существующие данные удалены'))

        call_command('loaddata', str(input_path))
        self.stdout.write(self.style.SUCCESS(f'Импортировано из {input_path}'))

        if not options['skip_photos']:
            call_command('download_car_photos', '--link-only')
            missing = _cars_missing_photo_files()
            if missing:
                self.stdout.write(f'Скачивание отсутствующих фото ({missing})...')
                call_command('download_car_photos')
