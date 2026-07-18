from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_conversation_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='telegram_message_id',
            field=models.BigIntegerField(
                blank=True,
                null=True,
                help_text='برای همگام‌سازی داخلی با گروه پشتیبانی تلگرام — دستی پر نکنید.',
                verbose_name='شناسه پیام تلگرام',
            ),
        ),
        migrations.CreateModel(
            name='TelegramBotState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update_id', models.BigIntegerField(default=0, verbose_name='آخرین شناسه پردازش‌شده')),
            ],
            options={
                'verbose_name': 'وضعیت بات تلگرام',
                'verbose_name_plural': 'وضعیت بات تلگرام',
            },
        ),
    ]
