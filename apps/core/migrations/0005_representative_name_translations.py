from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_representative_translations'),
    ]

    operations = [
        migrations.AddField(
            model_name='representative',
            name='first_name_fa',
            field=models.CharField(max_length=80, null=True, verbose_name='نام'),
        ),
        migrations.AddField(
            model_name='representative',
            name='first_name_en',
            field=models.CharField(max_length=80, null=True, verbose_name='نام'),
        ),
        migrations.AddField(
            model_name='representative',
            name='last_name_fa',
            field=models.CharField(max_length=100, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AddField(
            model_name='representative',
            name='last_name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='نام خانوادگی'),
        ),
    ]
