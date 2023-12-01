from django.contrib import admin
from .models import Catalog, ProductCategory, ProductSubcategory, Product, ShoppingCart


admin.site.register(Catalog)
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(Product)
admin.site.register(ShoppingCart)
