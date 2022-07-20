# Generated by Django 4.0.6 on 2022-07-20 08:50

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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=10)),
                ('stock', models.IntegerField()),
                ('discount', models.DecimalField(decimal_places=0, max_digits=3, null=True)),
                ('second_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.secondcategory')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'types',
            },
        ),
        migrations.CreateModel(
            name='ThumbnailImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumbnail_images', to='products.product')),
            ],
            options={
                'db_table': 'thumbnail_images',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='types',
            field=models.ManyToManyField(to='products.type'),
        ),
        migrations.CreateModel(
            name='DetailImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_images', to='products.product')),
            ],
            options={
                'db_table': 'detail_images',
            },
        ),
    ]
