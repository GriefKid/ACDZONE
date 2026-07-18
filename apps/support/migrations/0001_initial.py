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
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, verbose_name='موضوع')),
                ('status', models.CharField(
                    choices=[('open', 'باز'), ('answered', 'پاسخ داده شده'), ('closed', 'بسته شده')],
                    default='open', max_length=10, verbose_name='وضعیت',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tickets',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='کاربر',
                )),
            ],
            options={
                'verbose_name': 'تیکت',
                'verbose_name_plural': 'تیکت‌ها',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='TicketMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='متن پیام')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')),
                ('sender', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ticket_messages',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='فرستنده',
                )),
                ('ticket', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='messages',
                    to='support.ticket',
                    verbose_name='تیکت',
                )),
            ],
            options={
                'verbose_name': 'پیام تیکت',
                'verbose_name_plural': 'پیام‌های تیکت',
                'ordering': ['created_at'],
            },
        ),
    ]
