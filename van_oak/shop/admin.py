from django.contrib import admin

from .models import ProductType, Blank, BlankTrafaret, Compound

admin.site.register(ProductType)
admin.site.register(Blank)
admin.site.register(BlankTrafaret)
admin.site.register(Compound)

