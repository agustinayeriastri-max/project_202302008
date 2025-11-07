from django import forms
from django.forms import modelformset_factory
from .models import Pembelian, TransaksiPembelian, DetailPembelian, Barang

class PembelianForm(forms.ModelForm):
    class Meta:
        model = Pembelian
        fields = ['supplier', 'barang', 'jumlah', 'harga_beli']

class TransaksiPembelianForm(forms.ModelForm):
    class Meta:
        model = TransaksiPembelian
        fields = ['supplier', 'tanggal']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
        }

class DetailPembelianForm(forms.ModelForm):
    class Meta:
        model = DetailPembelian
        fields = ['barang', 'jumlah', 'harga_beli']

DetailPembelianFormSet = modelformset_factory(
    DetailPembelian,
    form=DetailPembelianForm,
    extra=2,
    can_delete=True
)

class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = ['kategori', 'supplier', 'nama', 'harga', 'stok']
