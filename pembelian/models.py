from django.db import models

# === Kategori Sepatu ===
class KategoriSepatu(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

# === Supplier ===
class Supplier(models.Model):
    nama = models.CharField(max_length=100)
    kontak = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

# === Barang (Sepatu) ===
class Barang(models.Model):
    kategori = models.ForeignKey(KategoriSepatu, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nama

# === Pembelian Barang (langsung ke stok) ===
class Pembelian(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    harga_beli = models.DecimalField(max_digits=10, decimal_places=2)
    tanggal = models.DateTimeField(auto_now_add=True)

    @property
    def total_harga(self):
        return self.jumlah * self.harga_beli

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.barang.stok += self.jumlah
        self.barang.save()

    def __str__(self):
        return f"Pembelian {self.barang.nama} ({self.jumlah})"

# === Transaksi Pembelian (untuk banyak detail) ===
class TransaksiPembelian(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    tanggal = models.DateField()
    total_harga = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Transaksi {self.id} - {self.supplier.nama}"

# === Detail dari Transaksi Pembelian ===
class DetailPembelian(models.Model):
    transaksi = models.ForeignKey(TransaksiPembelian, related_name='details', on_delete=models.CASCADE)
    barang = models.ForeignKey(Barang, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    harga_beli = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_harga(self):
        return self.jumlah * self.harga_beli

    def __str__(self):
        return f"{self.barang.nama} x{self.jumlah}"
