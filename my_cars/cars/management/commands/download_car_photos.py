from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from cars.models import Car
from cars.photo_urls import photo_url


class Command(BaseCommand):
    help = 'Скачивает фото автомобилей в media/cars/ и привязывает к ImageField'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перекачать все фото заново',
        )
        parser.add_argument(
            '--link-only',
            action='store_true',
            help='Только привязать уже существующие файлы на диске',
        )

    def handle(self, *args, **options):
        media_cars = Path(settings.MEDIA_ROOT) / 'cars'
        media_cars.mkdir(parents=True, exist_ok=True)

        downloaded = 0
        linked = 0
        skipped = 0
        failed = 0

        for car in Car.objects.select_related('mark').order_by('id'):
            local_name = f'{car.slug}.jpg'
            local_path = media_cars / local_name
            relative_path = f'cars/{local_name}'

            if options['link_only']:
                if local_path.exists() and (not car.photo or options['force']):
                    car.photo = relative_path
                    car.save(update_fields=['photo'])
                    linked += 1
                else:
                    skipped += 1
                continue

            if car.photo and local_path.exists() and not options['force']:
                if car.photo.name != relative_path:
                    car.photo = relative_path
                    car.save(update_fields=['photo'])
                skipped += 1
                continue

            url = car.photo_url or photo_url(
                car.id, car.mark.name, car.model, car.year, car.complect,
            )

            try:
                response = requests.get(url, timeout=45, headers={
                    'User-Agent': 'DriveLog/1.0 (car catalog seed)',
                })
                response.raise_for_status()
                content = response.content
                if len(content) < 1000:
                    raise ValueError('Слишком маленький файл')

                local_path.write_bytes(content)
                car.photo = relative_path
                if not car.photo_url:
                    car.photo_url = url
                car.save(update_fields=['photo', 'photo_url'])
                downloaded += 1
                self.stdout.write(f'  ✓ {car.mark.name} {car.model}')
            except Exception as exc:
                failed += 1
                self.stdout.write(self.style.WARNING(
                    f'  ✗ {car.slug}: {exc}',
                ))
                if local_path.exists() and not car.photo:
                    car.photo = relative_path
                    car.save(update_fields=['photo'])
                    linked += 1

        self.stdout.write(self.style.SUCCESS(
            f'Готово: скачано {downloaded}, привязано {linked}, '
            f'пропущено {skipped}, ошибок {failed}',
        ))
