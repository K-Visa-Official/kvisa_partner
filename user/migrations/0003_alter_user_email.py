# Generated by Django 5.1.6 on 2025-02-16 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_bu_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='이메일'),
        ),
    ]
