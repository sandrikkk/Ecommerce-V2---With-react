from django.contrib import admin
from product.models import StoreProductsModel, CategoryModel,Review,Order,OrderItem,ShippingAddress
# Register your models here.
class StoreProductsAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category','modified_date','is_avaible')
    prepopulated_fields = {"slug": ("product_name",)}

admin.site.register(StoreProductsModel,StoreProductsAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug')
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)