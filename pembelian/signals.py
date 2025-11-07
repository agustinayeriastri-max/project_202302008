from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import DetailPembelian

@receiver(pre_save, sender=DetailPembelian)
def update_stok_on_edit(sender, instance, **kwargs):
    if instance.pk:
        old = DetailPembelian.objects.get(pk=instance.pk)
        if old.barang != instance.barang:
            old.barang.stok += old.jumlah
            old.barang.save()

            if instance.barang.stok < instance.jumlah:
                raise ValidationError("Stok tidak cukup.")
            instance.barang.stok -= instance.jumlah
            instance.barang.save()
        else:
            selisih = instance.jumlah - old.jumlah
            if instance.barang.stok < selisih:
                raise ValidationError("Stok tidak cukup.")
            instance.barang.stok -= selisih
            instance.barang.save()

@receiver(post_delete, sender=DetailPembelian)
def restore_stok_on_delete(sender, instance, **kwargs):
    instance.barang.stok += instance.jumlah
    instance.barang.save()
