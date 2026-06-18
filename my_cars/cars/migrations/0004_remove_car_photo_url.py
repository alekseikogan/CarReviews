from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_alter_car_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='photo_url',
        ),
    ]
