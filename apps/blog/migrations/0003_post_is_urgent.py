from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_options_alter_post_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_urgent',
            field=models.BooleanField(
                default=False,
                help_text=(
                    'برای ACDNews و ACDNotes هر دو. پست فوری همیشه اول لیست می‌آید '
                    '(بدون توجه به تاریخ انتشار) و با قاب/برچسب قرمز مشخص می‌شود.'
                ),
                verbose_name='خبر فوری',
            ),
        ),
    ]
