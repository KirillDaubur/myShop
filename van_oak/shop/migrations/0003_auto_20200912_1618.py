# Generated by Django 3.1.1 on 2020-09-12 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_compound_particular_matches'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to='Products/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Input price', max_digits=7),
        ),
        migrations.CreateModel(
            name='ProductTypeProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Input product type name', max_length=20)),
                ('product_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.producttype')),
            ],
        ),
        migrations.CreateModel(
            name='ProductStack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_in_stock', models.PositiveSmallIntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField()),
                ('product_type_property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.producttypeproperty')),
            ],
        ),
    ]
