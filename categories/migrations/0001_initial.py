# Generated by Django 4.0.5 on 2022-07-18 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirstCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'first_categories',
            },
        ),
        migrations.CreateModel(
            name='SecondCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('first_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.firstcategory')),
            ],
            options={
                'db_table': 'second_categories',
            },
        ),
    ]
