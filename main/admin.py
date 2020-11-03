from django.contrib import admin

from .models import *

class ClienteInline(admin.TabularInline):
    model=Cliente


class ColaboradorInline(admin.TabularInline):
    model=Colaborador


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        ClienteInline,
        ColaboradorInline
    ]
    
class ProductoImageInline(admin.TabularInline):
    model=ProductoImage


class ProductoAdmin(admin.ModelAdmin):
    inlines = [
        ProductoImageInline,
    ]

# Register your models here.
admin.site.register(Localizacion)
#admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Colaborador)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Producto, ProductoAdmin)