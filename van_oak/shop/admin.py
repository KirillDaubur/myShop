from django.contrib import admin

from .models import ProductType, Blank, BlankTrafaret, Compound, \
	Product, ProductTypeProperty, ProductProperty, \
	ParameterizedProduct, Order, ProductInOrder

admin.site.register(ProductType)
admin.site.register(Blank)
admin.site.register(BlankTrafaret)
admin.site.register(Compound)
admin.site.register(Product)
admin.site.register(ProductTypeProperty)
admin.site.register(ProductProperty)
admin.site.register(ParameterizedProduct)
admin.site.register(Order)
admin.site.register(ProductInOrder)

