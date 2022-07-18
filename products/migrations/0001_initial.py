# Generated by Django 4.0.5 on 2022-07-18 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('stock', models.IntegerField()),
                ('second_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.secondcategory')),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]