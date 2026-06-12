from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_car_photo_url_alter_car_photo_alter_car_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='photo',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='cars/',
                verbose_name='Фото',
            ),
        ),
    ]
