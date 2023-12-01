# Generated by Django 4.2.7 on 2023-12-01 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='products',
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='shop.product', verbose_name='Продукты'),
        ),
    ]