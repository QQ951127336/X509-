# Generated by Django 2.0.5 on 2018-06-18 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CertificateWeb', '0005_applyforrevok'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revoke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialNumber', models.CharField(max_length=400)),
            ],
        ),
    ]
