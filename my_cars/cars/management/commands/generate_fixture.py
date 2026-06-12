import json
from datetime import datetime, timezone
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from cars.cars_data import BODY_TYPES, CARS, _desc
from cars.photo_urls import photo_url


class Command(BaseCommand):
    help = 'Генерирует fixtures/cars.json из cars_data.py'

    def handle(self, *args, **options):
        fixture_path = Path(__file__).resolve().parents[3] / 'fixtures' / 'cars.json'
        fixture_path.parent.mkdir(parents=True, exist_ok=True)

        items = []
        body_pk = {}
        mark_pk = {}
        created = datetime(2024, 1, 1, tzinfo=timezone.utc).isoformat()

        for idx, (slug, name) in enumerate(BODY_TYPES.items(), start=1):
            body_pk[slug] = idx
            items.append({
                'model': 'cars.body',
                'pk': idx,
                'fields': {'name': name, 'slug': slug},
            })

        car_pk = 0
        for idx, (mark_name, model, complect, body_slug, year, note) in enumerate(CARS, start=1):
            if mark_name not in mark_pk:
                mark_slug = slugify(mark_name) or f'mark-{len(mark_pk) + 1}'
                mark_pk[mark_name] = len(mark_pk) + 1
                items.append({
                    'model': 'cars.mark',
                    'pk': mark_pk[mark_name],
                    'fields': {'name': mark_name, 'slug': mark_slug},
                })

            base_slug = slugify(f'{mark_name}-{model}-{complect}') or f'car-{idx}'
            car_slug = base_slug
            counter = 1
            existing_slugs = {
                i['fields']['slug']
                for i in items
                if i['model'] == 'cars.car'
            }
            while car_slug in existing_slugs:
                car_slug = f'{base_slug}-{counter}'
                counter += 1

            car_pk += 1
            description = _desc(mark_name, model, complect, body_slug, year, note, index=idx)
            remote_url = photo_url(idx, mark_name, model, year, complect)

            items.append({
                'model': 'cars.car',
                'pk': car_pk,
                'fields': {
                    'mark': mark_pk[mark_name],
                    'body': body_pk[body_slug],
                    'slug': car_slug,
                    'model': model,
                    'complect': complect,
                    'description': description,
                    'year': year,
                    'photo': f'cars/{car_slug}.jpg',
                    'photo_url': remote_url,
                    'time_create': created,
                },
            })

        with fixture_path.open('w', encoding='utf-8') as fh:
            json.dump(items, fh, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f'Создан {fixture_path}: {len(body_pk)} кузовов, '
            f'{len(mark_pk)} марок, {car_pk} автомобилей',
        ))
