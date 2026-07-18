import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0002_ticketmessage_is_staff_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین پیام')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='chat_conversation',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='کاربر',
                )),
            ],
            options={
                'verbose_name': 'گفتگو',
                'verbose_name_plural': 'گفتگوها',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='متن پیام')),
                ('is_staff_reply', models.BooleanField(default=False, verbose_name='پاسخ پشتیبانی')),
                ('is_read', models.BooleanField(default=False, verbose_name='خوانده‌شده')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')),
                ('conversation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='messages',
                    to='support.conversation',
                    verbose_name='گفتگو',
                )),
                ('sender', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='chat_messages',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='فرستنده',
                )),
            ],
            options={
                'verbose_name': 'پیام گفتگو',
                'verbose_name_plural': 'پیام‌های گفتگو',
                'ordering': ['created_at'],
            },
        ),
    ]
