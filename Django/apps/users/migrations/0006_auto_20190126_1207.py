# Generated by Django 2.1.2 on 2019-01-26 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190126_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='image/default.gif', upload_to='image/%Y%m%d', verbose_name='头像'),
        ),
    ]