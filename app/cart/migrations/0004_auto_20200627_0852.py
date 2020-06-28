# Generated by Django 3.0.7 on 2020-06-27 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200627_0829'),
        ('cart', '0003_auto_20200613_1453'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name_plural': 'Cart'},
        ),
        migrations.AddField(
            model_name='cart',
            name='shop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
            preserve_default=False,
        ),
    ]