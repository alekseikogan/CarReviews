from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='photo_url',
            field=models.URLField(blank=True, max_length=500, verbose_name='URL фото'),
        ),
        migrations.AlterField(
            model_name='car',
            name='photo',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='photos/%Y/%m/%d/',
                verbose_name='Фото',
            ),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(default=2020, verbose_name='Год'),
        ),
    ]
