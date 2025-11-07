# admin.py
from django.contrib import admin
from .models import Supplier, Barang, Pembelian, TransaksiPembelian, DetailPembelian, KategoriSepatu

class DetailPembelianInline(admin.TabularInline):
    model = DetailPembelian
    extra = 1

class TransaksiPembelianAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'tanggal', 'total_harga')
    inlines = [DetailPembelianInline]

admin.site.register(KategoriSepatu)
admin.site.register(Supplier)
admin.site.register(Barang)
admin.site.register(Pembelian)
admin.site.register(TransaksiPembelian, TransaksiPembelianAdmin)
admin.site.register(DetailPembelian)
