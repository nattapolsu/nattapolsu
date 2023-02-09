# Generated by Django 4.1.3 on 2023-01-05 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=10)),
                ('course_name', models.CharField(max_length=255)),
                ('course_days', models.CharField(max_length=10)),
                ('course_fee', models.CharField(max_length=50)),
                ('course_date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
