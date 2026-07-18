from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='long_description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='long_description_fa',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='long_description_en',
            field=models.TextField(blank=True, null=True),
        ),
    ]
