# Generated by Django 4.1.1 on 2022-11-26 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0004_mealrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagName', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='tags',
            field=models.ManyToManyField(blank=True, to='meals.tag'),
        ),
    ]
