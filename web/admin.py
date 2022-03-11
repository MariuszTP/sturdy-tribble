from django.contrib import admin
from .models import *
from django.utils.html import format_html





from .models import Category
admin.site.register(Category)
from .models import ImageProduct, Product

from .models import Customer
admin.site.register(Customer)

from .models import Order
admin.site.register(Order)


class ImageProductInline(admin.StackedInline):
    model = ImageProduct

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="100px" />'.format(obj.image.url))
        
    image_tag.short_description = 'Product Image Preview'
    readonly_fields = ['image_tag']

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageProductInline]

    list_display = ['name', 'price', 'category']
    search_fields = ['name']
    list_filter = ['name']

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="100px" />'.format(obj.image.url))

    image_tag.short_description = 'Product Image Preview'
    readonly_fields = ['image_tag']



admin.site.register(Product, ProductAdmin)
admin.site.register(ImageProduct)


