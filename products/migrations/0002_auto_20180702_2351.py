# Generated by Django 2.0.5 on 2018-07-02 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='p_cids',
            new_name='children_pid',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='pcid',
            new_name='pid',
        ),
    ]
