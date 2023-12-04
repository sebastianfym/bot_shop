from django.contrib import admin
from .models import (Category, ProductSubcategory, Product, ShoppingCart, FAQ, FAQAnswer, AdditionalAnswer,
                     AdditionalQuestion, Channel)


admin.site.register(Channel)
admin.site.register(Category)
admin.site.register(ProductSubcategory)
admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(FAQ)
admin.site.register(FAQAnswer)
admin.site.register(AdditionalQuestion)
admin.site.register(AdditionalAnswer)

