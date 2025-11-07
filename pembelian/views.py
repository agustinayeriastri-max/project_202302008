from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.forms import formset_factory
from django.db.models import Sum
from django.template.loader import get_template
from django.utils.timezone import now
from django import forms
from xhtml2pdf import pisa

from .models import (
    Pembelian, Barang, Supplier, TransaksiPembelian,
    DetailPembelian, KategoriSepatu
)

from .forms import (
    TransaksiPembelianForm, DetailPembelianForm, BarangForm
)

# ------------------ HELPER ------------------ #
def get_kategori_list():
    return KategoriSepatu.objects.all()

# ------------------ HALAMAN AWAL ------------------ #
def welcome_page(request):
    kategori_list = get_kategori_list()
    return render(request, 'penjualan/welcome.html', {'kategori_list': kategori_list})

# ------------------ DASHBOARD ------------------ #
def dashboard(request):
    kategori_list = get_kategori_list()
    context = {
        'total_barang': Barang.objects.count(),
        'total_supplier': Supplier.objects.count(),
        'total_transaksi': TransaksiPembelian.objects.count(),
        'total_pembelian': Pembelian.objects.count(),
        'barang_menipis': Barang.objects.filter(stok__lt=10),
        'kategori_list': kategori_list,
    }
    return render(request, 'penjualan/dashboard.html', context)

# ------------------ TRANSAKSI MULTI BARANG ------------------ #
def tambah_transaksi(request):
    kategori_list = get_kategori_list()
    DetailFormSet = formset_factory(DetailPembelianForm, extra=2, can_delete=True)

    if request.method == 'POST':
        form_transaksi = TransaksiPembelianForm(request.POST)
        formset = DetailFormSet(request.POST)
        if form_transaksi.is_valid() and formset.is_valid():
            transaksi = form_transaksi.save()
            total_harga = 0
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    detail = form.save(commit=False)
                    detail.transaksi = transaksi
                    detail.save()
                    detail.barang.stok += detail.jumlah
                    detail.barang.save()
                    total_harga += detail.jumlah * detail.harga_beli
            transaksi.total_harga = total_harga
            transaksi.save()
            return redirect('list_transaksi')
    else:
        form_transaksi = TransaksiPembelianForm()
        formset = DetailFormSet()

    return render(request, 'penjualan/form_transaksi.html', {
        'form_transaksi': form_transaksi,
        'formset': formset,
        'kategori_list': kategori_list,
    })

def list_transaksi(request):
    kategori_list = get_kategori_list()
    transaksi_list = TransaksiPembelian.objects.all().order_by('-id')
    return render(request, 'penjualan/list_transaksi.html', {
        'transaksi_list': transaksi_list,
        'kategori_list': kategori_list
    })

def detail_transaksi(request, id):
    kategori_list = get_kategori_list()
    transaksi = get_object_or_404(TransaksiPembelian, pk=id)
    detail_list = DetailPembelian.objects.filter(transaksi=transaksi)
    return render(request, 'penjualan/detail_transaksi.html', {
        'transaksi': transaksi,
        'detail_list': detail_list,
        'kategori_list': kategori_list
    })

def hapus_transaksi(request, id):
    transaksi = get_object_or_404(TransaksiPembelian, pk=id)
    for detail in transaksi.details.all():
        detail.barang.stok -= detail.jumlah
        detail.barang.save()
    transaksi.delete()
    return redirect('list_transaksi')

def hapus_detail(request, id):
    detail = get_object_or_404(DetailPembelian, pk=id)
    transaksi_id = detail.transaksi.id
    detail.barang.stok -= detail.jumlah
    detail.barang.save()
    detail.delete()
    return redirect('detail_transaksi', id=transaksi_id)

# ------------------ EDIT DETAIL ------------------ #
def edit_detail(request, id):
    detail = get_object_or_404(DetailPembelian, id=id)
    kategori_list = get_kategori_list()
    if request.method == 'POST':
        form = DetailPembelianForm(request.POST, instance=detail)
        if form.is_valid():
            detail.barang.stok -= detail.jumlah
            detail.barang.save()

            updated_detail = form.save(commit=False)
            updated_detail.save()

            updated_detail.barang.stok += updated_detail.jumlah
            updated_detail.barang.save()

            return redirect('detail_transaksi', id=detail.transaksi.id)
    else:
        form = DetailPembelianForm(instance=detail)

    return render(request, 'penjualan/edit_detail.html', {
        'form': form,
        'kategori_list': kategori_list,
        'detail': detail,
    })

# ------------------ FORM PEMBELIAN ------------------ #
def form_pembelian(request):
    kategori_list = get_kategori_list()
    return render(request, 'penjualan/form_pembelian.html', {
        'kategori_list': kategori_list
    })

# ------------------ LAPORAN ------------------ #
def laporan_pembelian(request):
    kategori_list = get_kategori_list()
    detail_list = DetailPembelian.objects.select_related('transaksi', 'barang', 'transaksi__supplier').all()

    for detail in detail_list:
        detail.subtotal = detail.jumlah * detail.harga_beli

    total = sum(detail.subtotal for detail in detail_list)

    return render(request, 'penjualan/laporan_pembelian.html', {
        'detail_list': detail_list,
        'total': total,
        'kategori_list': kategori_list
    })

def cetak_pdf(request):
    detail_list = DetailPembelian.objects.select_related('transaksi', 'barang', 'transaksi__supplier').all()

    for detail in detail_list:
        detail.subtotal = detail.jumlah * detail.harga_beli

    total = sum(detail.subtotal for detail in detail_list)

    template = get_template('penjualan/laporan_pdf.html')
    html = template.render({
        'detail_list': detail_list,
        'total': total,
        'now': now(),
    })
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response)
    return response

# ------------------ STOK BARANG ------------------ #
def daftar_stok_barang(request):
    kategori_list = get_kategori_list()
    barang_list = Barang.objects.all()
    return render(request, 'penjualan/stok_barang.html', {
        'barang_list': barang_list,
        'kategori_list': kategori_list
    })

# ------------------ AJAX ------------------ #
def get_harga_barang(request):
    barang_id = request.GET.get('barang_id')
    try:
        barang = Barang.objects.get(pk=barang_id)
        return JsonResponse({'harga': float(barang.harga)})
    except Barang.DoesNotExist:
        return JsonResponse({'harga': 0})

def get_barang_by_supplier(request):
    supplier_id = request.GET.get('supplier_id')
    barangs = Barang.objects.filter(supplier_id=supplier_id).values('id', 'nama')
    return JsonResponse(list(barangs), safe=False)

# ------------------ BARANG PER KATEGORI ------------------ #
def barang_per_kategori(request, kategori_id):
    kategori = get_object_or_404(KategoriSepatu, id=kategori_id)
    barang_list = Barang.objects.filter(kategori=kategori)
    kategori_list = get_kategori_list()
    return render(request, 'penjualan/barang_per_kategori.html', {
        'kategori': kategori,
        'barang_list': barang_list,
        'kategori_list': kategori_list
    })

# ------------------ KATEGORI ------------------ #
def kategori_list(request):
    kategori_list = get_kategori_list()
    return render(request, 'penjualan/kategori_list.html', {
        'kategori_list': kategori_list
    })

def hapus_kategori(request, id):
    kategori = get_object_or_404(KategoriSepatu, id=id)
    kategori.delete()
    return redirect('kategori_list')

class KategoriForm(forms.ModelForm):
    class Meta:
        model = KategoriSepatu
        fields = ['nama']
        labels = {'nama': 'Nama Kategori'}

def edit_kategori(request, id):
    kategori = get_object_or_404(KategoriSepatu, id=id)
    kategori_list = get_kategori_list()
    if request.method == 'POST':
        form = KategoriForm(request.POST, instance=kategori)
        if form.is_valid():
            form.save()
            return redirect('kategori_list')
    else:
        form = KategoriForm(instance=kategori)
    return render(request, 'penjualan/edit_kategori.html', {
        'form': form,
        'kategori_list': kategori_list
    })
