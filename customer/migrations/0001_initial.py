# Generated by Django 4.0.3 on 2023-05-03 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=180)),
                ('last_name', models.CharField(max_length=180)),
                ('surname', models.CharField(blank=True, max_length=180, null=True)),
                ('national', models.CharField(blank=True, max_length=180, null=True)),
                ('address', models.CharField(blank=True, max_length=180, null=True)),
                ('place_work', models.CharField(blank=True, max_length=180, null=True)),
                ('telephone_number', models.CharField(blank=True, max_length=180, null=True)),
                ('profession', models.CharField(blank=True, max_length=180, null=True)),
                ('iin', models.CharField(max_length=13, unique=True)),
                ('signature', models.FileField(blank=True, null=True, upload_to='signatures/')),
            ],
        ),
    ]
