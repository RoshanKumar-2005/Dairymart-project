from django.contrib import admin
from .models import product,Customer,Cart,ShippingAddress,OrderPlaced,Wishlist

# Register your models here.
admin.site.register(product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','discounted_price','category','product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'subtotal']

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'city', 'zip_code', 'phone')
    search_fields = ('user__username', 'full_name', 'city')
    list_filter = ('city',)
    ordering = ('id',)


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'status', 'ordered_date')
    list_filter = ('status', 'ordered_date')
    search_fields = ('user__username', 'product__title', 'status')
    ordering = ('-ordered_date',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('user__username', 'product__title')
