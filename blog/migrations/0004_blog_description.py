# Generated by Django 3.2.9 on 2021-11-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='description',
            field=models.TextField(default=''),
        ),
    ]