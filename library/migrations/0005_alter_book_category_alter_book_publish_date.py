# Generated by Django 4.0.3 on 2023-12-22 21:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_book_category_alter_book_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library.category'),
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 22, 22, 30, 2, 119663)),
        ),
    ]
