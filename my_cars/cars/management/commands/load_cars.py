from django.core.management.base import BaseCommand
from django.utils.text import slugify

from cars.cars_data import BODY_TYPES, CARS, _desc
from cars.photo_urls import photo_url
from cars.models import Body, Car, Mark


class Command(BaseCommand):
    help = 'Загружает начальные данные об автомобилях в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Пересоздать данные (удалить существующие записи)',
        )
        parser.add_argument(
            '--update-photos',
            action='store_true',
            help='Обновить URL фотографий у существующих записей',
        )

    def handle(self, *args, **options):
        if options['update_photos']:
            updated = 0
            for idx, car in enumerate(
                Car.objects.select_related('mark').order_by('id'),
                start=1,
            ):
                car.photo_url = photo_url(
                    car.id, car.mark.name, car.model, car.year, car.complect,
                )
                car.save(update_fields=['photo_url'])
                updated += 1
            self.stdout.write(self.style.SUCCESS(f'Обновлено фото: {updated}'))
            if not options['force']:
                return

        if options['force']:
            Car.objects.all().delete()
            Mark.objects.all().delete()
            Body.objects.all().delete()
            self.stdout.write(self.style.WARNING('Существующие данные удалены'))

        if Car.objects.exists() and not options['force']:
            self.stdout.write(self.style.WARNING('Данные уже загружены. Используйте --force для перезагрузки'))
            return

        bodies = {}
        for slug, name in BODY_TYPES.items():
            body, _ = Body.objects.get_or_create(slug=slug, defaults={'name': name})
            bodies[slug] = body

        marks = {}
        created_count = 0

        for idx, (mark_name, model, complect, body_slug, year, note) in enumerate(CARS, start=1):
            if mark_name not in marks:
                mark_slug = slugify(mark_name) or f'mark-{idx}'
                mark, _ = Mark.objects.get_or_create(
                    slug=mark_slug,
                    defaults={'name': mark_name},
                )
                marks[mark_name] = mark

            base_slug = slugify(f'{mark_name}-{model}-{complect}') or f'car-{idx}'
            slug = base_slug
            counter = 1
            while Car.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            description = _desc(mark_name, model, complect, body_slug, year, note, index=idx)
            Car.objects.create(
                mark=marks[mark_name],
                slug=slug,
                model=model,
                complect=complect,
                body=bodies[body_slug],
                description=description,
                year=year,
                photo_url=photo_url(idx, mark_name, model, year, complect),
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Загружено {created_count} автомобилей, '
            f'{len(marks)} марок, {len(bodies)} типов кузова',
        ))
