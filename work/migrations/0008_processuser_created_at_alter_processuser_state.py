# Generated by Django 5.1.6 on 2025-02-25 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0007_remove_process_marketing_remove_process_state_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processuser',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='processuser',
            name='state',
            field=models.IntegerField(choices=[(0, '접수완료'), (1, '계약완료'), (2, '서류작성'), (3, '심사진행'), (4, '처리완료'), (5, '상담종료')], default=1),
        ),
    ]
