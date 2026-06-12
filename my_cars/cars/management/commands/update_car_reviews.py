from django.core.management.base import BaseCommand
from django.utils.text import slugify

from cars.cars_data import CARS, _desc
from cars.models import Car


class Command(BaseCommand):
    help = 'Обновляет описания автомобилей из car_reviews.py (без пересоздания БД)'

    def handle(self, *args, **options):
        existing_slugs = set()
        updated = 0
        missing = []

        for idx, (mark_name, model, complect, body_slug, year, note) in enumerate(CARS, start=1):
            base_slug = slugify(f'{mark_name}-{model}-{complect}') or f'car-{idx}'
            car_slug = base_slug
            counter = 1
            while car_slug in existing_slugs:
                car_slug = f'{base_slug}-{counter}'
                counter += 1
            existing_slugs.add(car_slug)

            description = _desc(mark_name, model, complect, body_slug, year, note, index=idx)
            try:
                car = Car.objects.get(slug=car_slug)
            except Car.DoesNotExist:
                missing.append(car_slug)
                continue

            if car.description != description:
                car.description = description
                car.save(update_fields=['description'])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f'Обновлено описаний: {updated}'))
        if missing:
            self.stdout.write(self.style.WARNING(
                f'Не найдено в БД ({len(missing)}): {", ".join(missing[:5])}...',
            ))
