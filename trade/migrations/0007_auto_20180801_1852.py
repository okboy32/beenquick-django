# Generated by Django 2.0.5 on 2018-08-01 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_auto_20180801_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='freight',
            field=models.FloatField(default=0.0, verbose_name='运费'),
        ),
        migrations.AlterField(
            model_name='ordergoods',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Products', verbose_name='商品'),
        ),
    ]
