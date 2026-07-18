import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255, verbose_name='پیام')),
                ('link', models.CharField(blank=True, max_length=255, verbose_name='لینک')),
                ('is_read', models.BooleanField(default=False, verbose_name='خوانده‌شده')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notifications',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='کاربر',
                )),
            ],
            options={
                'verbose_name': 'اعلان',
                'verbose_name_plural': 'اعلان‌ها',
                'ordering': ['-created_at'],
            },
        ),
    ]
