from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_expand_country_descriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='capital',
            field=models.CharField(blank=True, max_length=100, verbose_name='پایتخت'),
        ),
        migrations.AddField(
            model_name='country',
            name='capital_fa',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='پایتخت'),
        ),
        migrations.AddField(
            model_name='country',
            name='capital_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='پایتخت'),
        ),
        migrations.AddField(
            model_name='country',
            name='official_language',
            field=models.CharField(blank=True, max_length=150, verbose_name='زبان رسمی'),
        ),
        migrations.AddField(
            model_name='country',
            name='official_language_fa',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='زبان رسمی'),
        ),
        migrations.AddField(
            model_name='country',
            name='official_language_en',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='زبان رسمی'),
        ),
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.CharField(blank=True, max_length=100, verbose_name='واحد پول'),
        ),
        migrations.AddField(
            model_name='country',
            name='currency_fa',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='واحد پول'),
        ),
        migrations.AddField(
            model_name='country',
            name='currency_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='واحد پول'),
        ),
        migrations.AddField(
            model_name='country',
            name='calling_code',
            field=models.CharField(blank=True, help_text='مثلاً +98', max_length=10, verbose_name='کد تلفن بین‌الملل'),
        ),
        migrations.AddField(
            model_name='country',
            name='best_time_to_visit',
            field=models.CharField(
                blank=True, help_text='مثلاً «بهار و پاییز» یا «اکتبر تا مارس»',
                max_length=150, verbose_name='بهترین فصل سفر',
            ),
        ),
        migrations.AddField(
            model_name='country',
            name='best_time_to_visit_fa',
            field=models.CharField(
                blank=True, help_text='مثلاً «بهار و پاییز» یا «اکتبر تا مارس»',
                max_length=150, null=True, verbose_name='بهترین فصل سفر',
            ),
        ),
        migrations.AddField(
            model_name='country',
            name='best_time_to_visit_en',
            field=models.CharField(
                blank=True, help_text='مثلاً «بهار و پاییز» یا «اکتبر تا مارس»',
                max_length=150, null=True, verbose_name='بهترین فصل سفر',
            ),
        ),
    ]
