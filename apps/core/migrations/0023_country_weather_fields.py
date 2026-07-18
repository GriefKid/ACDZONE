from django.db import migrations, models


SEASON_LABELS = {
    'weather_spring': 'آب‌وهوا در بهار',
    'weather_summer': 'آب‌وهوا در تابستان',
    'weather_autumn': 'آب‌وهوا در پاییز',
    'weather_winter': 'آب‌وهوا در زمستان',
}


def _ops():
    ops = []
    for field_name, label in SEASON_LABELS.items():
        ops.append(migrations.AddField(
            model_name='country',
            name=field_name,
            field=models.TextField(blank=True, verbose_name=label),
        ))
        ops.append(migrations.AddField(
            model_name='country',
            name=f'{field_name}_fa',
            field=models.TextField(blank=True, null=True, verbose_name=label),
        ))
        ops.append(migrations.AddField(
            model_name='country',
            name=f'{field_name}_en',
            field=models.TextField(blank=True, null=True, verbose_name=label),
        ))
    return ops


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_routes_remaining_countries'),
    ]

    operations = _ops()
