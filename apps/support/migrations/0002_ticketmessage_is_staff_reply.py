from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketmessage',
            name='is_staff_reply',
            field=models.BooleanField(default=False, verbose_name='پاسخ پشتیبانی'),
        ),
    ]
