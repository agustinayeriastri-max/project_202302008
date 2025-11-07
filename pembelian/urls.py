from django.urls import path
from . import views

urlpatterns = [
    # Halaman Awal dan Dashboard
    path('', views.welcome_page, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Transaksi Multi-Barang
    path('transaksi/', views.list_transaksi, name='list_transaksi'),
    path('transaksi/tambah/', views.tambah_transaksi, name='tambah_transaksi'),
    path('transaksi/detail/<int:id>/', views.detail_transaksi, name='detail_transaksi'),
    path('transaksi/hapus/<int:id>/', views.hapus_transaksi, name='hapus_transaksi'),

    # Form Pembelian
    path('pembelian/form/', views.form_pembelian, name='form_pembelian'),

    # Detail Transaksi
    path('detail/edit/<int:id>/', views.edit_detail, name='edit_detail'),
    path('detail/hapus/<int:id>/', views.hapus_detail, name='hapus_detail'),

    # Laporan Pembelian
    path('laporan/', views.laporan_pembelian, name='laporan_pembelian'),
    path('laporan/cetak/', views.cetak_pdf, name='cetak_pdf'),

    # Stok Barang
    path('stok/', views.daftar_stok_barang, name='stok_barang'),

    # Kategori
    path('kategori/', views.kategori_list, name='kategori_list'),
    path('kategori/hapus/<int:id>/', views.hapus_kategori, name='hapus_kategori'),
    path('kategori/edit/<int:id>/', views.edit_kategori, name='edit_kategori'),

    # Barang berdasarkan Kategori
    path('kategori/<int:kategori_id>/barang/', views.barang_per_kategori, name='barang_per_kategori'),

    # AJAX
    path('ajax/get-harga-barang/', views.get_harga_barang, name='get_harga_barang'),
    path('ajax/get-barang-by-supplier/', views.get_barang_by_supplier, name='get_barang_by_supplier'),
]
