# Generated by Django 4.1.1 on 2022-11-26 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0005_tag_meal_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='typicalMealTime',
        ),
    ]