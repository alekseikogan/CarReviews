from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from cars.models import Car


class Command(BaseCommand):
    help = 'Привязывает локальные фото из media/cars/ к записям автомобилей'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перепривязать фото даже если поле уже заполнено',
        )

    def handle(self, *args, **options):
        media_cars = Path(settings.MEDIA_ROOT) / 'cars'
        media_cars.mkdir(parents=True, exist_ok=True)

        linked = 0
        skipped = 0
        missing = 0

        for car in Car.objects.select_related('mark').order_by('id'):
            local_name = f'{car.slug}.jpg'
            local_path = media_cars / local_name
            relative_path = f'cars/{local_name}'

            if not local_path.exists():
                missing += 1
                continue

            if car.photo and car.photo.name == relative_path and not options['force']:
                skipped += 1
                continue

            car.photo = relative_path
            car.save(update_fields=['photo'])
            linked += 1

        self.stdout.write(self.style.SUCCESS(
            f'Готово: привязано {linked}, пропущено {skipped}, '
            f'без файла на диске {missing}',
        ))
