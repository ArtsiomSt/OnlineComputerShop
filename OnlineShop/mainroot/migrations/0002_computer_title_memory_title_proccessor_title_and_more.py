# Generated by Django 4.0.6 on 2022-10-14 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainroot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='title',
            field=models.CharField(default='Comp', max_length=30),
        ),
        migrations.AddField(
            model_name='memory',
            name='title',
            field=models.CharField(default='Mem', max_length=30),
        ),
        migrations.AddField(
            model_name='proccessor',
            name='title',
            field=models.CharField(default='Proc', max_length=30),
        ),
        migrations.AddField(
            model_name='videocard',
            name='title',
            field=models.CharField(default='Vid', max_length=30),
        ),
    ]