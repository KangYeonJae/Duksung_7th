# Generated by Django 2.2.1 on 2019-05-17 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tip',
            name='photo',
            field=models.ImageField(blank=True, upload_to='tip/%y/%m/%d'),
        ),
    ]
