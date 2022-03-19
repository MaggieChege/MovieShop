# Generated by Django 4.0.3 on 2022-03-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_rename_day_rented_rentoutmovies_number_of_days_rented'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricing',
            name='movie_type',
            field=models.CharField(choices=[('Regular', 'Regular'), ('Children', 'Children'), ('New_Release', 'New_Release')], max_length=50, unique=True),
        ),
    ]
