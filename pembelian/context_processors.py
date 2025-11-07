# pembelian/context_processors.py
from .models import KategoriSepatu

def kategori_list(request):
    return {'kategori_list': KategoriSepatu.objects.all()}
