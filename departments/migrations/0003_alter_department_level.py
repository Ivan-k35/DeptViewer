# Generated by Django 4.2.16 on 2024-11-06 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_alter_department_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]