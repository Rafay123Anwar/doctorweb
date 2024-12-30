# Generated by Django 5.1.3 on 2024-12-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=15, unique=True)),
                ('address', models.TextField()),
                ('specialization', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('profile_picture', models.BinaryField(blank=True, null=True)),
                ('joining_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=15, unique=True)),
                ('address', models.TextField()),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('profile_picture', models.BinaryField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('managed_doctors', models.ManyToManyField(blank=True, related_name='managed_by_staff', to='api.doctor')),
                ('managed_patients', models.ManyToManyField(blank=True, related_name='managed_by_staff', to='api.patient')),
            ],
        ),
    ]