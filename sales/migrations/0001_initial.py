# Generated by Django 3.1.2 on 2021-05-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField()),
                ('store', models.CharField(max_length=100)),
                ('headline', models.CharField(max_length=100)),
                ('image', models.TextField()),
                ('discount', models.TextField(null=True)),
                ('new_price', models.TextField(null=True)),
                ('old_price', models.TextField(null=True)),
            ],
        ),
    ]
