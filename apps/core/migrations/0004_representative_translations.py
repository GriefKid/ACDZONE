from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_representative'),
    ]

    operations = [
        migrations.AddField(
            model_name='representative',
            name='position_fa',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='عنوان'),
        ),
        migrations.AddField(
            model_name='representative',
            name='position_en',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='عنوان'),
        ),
        migrations.AddField(
            model_name='representative',
            name='bio_fa',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AddField(
            model_name='representative',
            name='bio_en',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
    ]
