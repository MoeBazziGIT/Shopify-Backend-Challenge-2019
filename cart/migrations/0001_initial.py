# Generated by Django 2.1.2 on 2019-01-16 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(blank=True, default=False, null=True)),
                ('total', models.FloatField(blank=True, default=0.0)),
                ('products', models.ManyToManyField(blank=True, default=None, related_name='cart_products', to='products.CartProduct')),
            ],
        ),
    ]