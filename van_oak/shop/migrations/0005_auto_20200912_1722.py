# Generated by Django 3.1.1 on 2020-09-12 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200912_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='productproperty',
            name='product_stack',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shop.productstack'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='compounds',
            field=models.ManyToManyField(blank=True, to='shop.Compound'),
        ),
        migrations.AlterField(
            model_name='productstack',
            name='product',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
            preserve_default=False,
        ),
    ]