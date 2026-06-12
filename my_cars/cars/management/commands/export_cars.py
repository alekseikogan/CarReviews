from pathlib import Path

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Экспорт данных cars в fixtures/cars.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            default='fixtures/cars.json',
            help='Путь к файлу fixture относительно my_cars/',
        )

    def handle(self, *args, **options):
        output = Path(options['output'])
        if not output.is_absolute():
            output = Path(__file__).resolve().parents[3] / output
        output.parent.mkdir(parents=True, exist_ok=True)

        call_command(
            'dumpdata',
            'cars.body',
            'cars.mark',
            'cars.car',
            indent=2,
            natural_foreign=True,
            natural_primary=True,
            output=str(output),
        )
        self.stdout.write(self.style.SUCCESS(f'Экспортировано в {output}'))
