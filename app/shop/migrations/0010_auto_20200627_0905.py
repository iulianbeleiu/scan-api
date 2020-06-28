# Generated by Django 3.0.7 on 2020-06-27 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20200627_0829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='address',
        ),
        migrations.AddField(
            model_name='shop',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shop.Address'),
            preserve_default=False,
        ),
    ]
