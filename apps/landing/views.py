from django.db.models import Avg, Count, ExpressionWrapper, F, FloatField, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.atlets.models import AtletProfile, Cabor, PerguruanProfil, Prestasi
from apps.jadwal.models import AgendaEvent, JadwalLatihan
from apps.kesiapan.models import PenilaianKesiapan
from .forms import ContactMessageForm
from .models import Berita


def landing(request):
    # Graceful fallback jika DB belum migrate / misconfigured (hindari 500 di Vercel)
    try:
        profil = PerguruanProfil.objects.first()
        total_atlet = AtletProfile.objects.filter(status_aktif=True).count()
        total_cabor = Cabor.objects.filter(aktif=True).count()
        total_prestasi = Prestasi.objects.count()
        jadwal_minggu_ini = JadwalLatihan.objects.filter(aktif=True).count()

        rata_expr = ExpressionWrapper((F('fisik') + F('teknik') + F('mental')) / 3.0, output_field=FloatField())
        top_atlet = (
            PenilaianKesiapan.objects.values('atlet__nama_lengkap', 'atlet__cabor__nama')
            .annotate(rata=Avg(rata_expr))
            .order_by('-rata')[:5]
        )
        top_prestasi = Prestasi.objects.select_related('atlet').order_by('-tahun')[:5]
        agenda = AgendaEvent.objects.order_by('tanggal_mulai')[:4]
        jadwal = JadwalLatihan.objects.filter(aktif=True).select_related('cabor')[:6]
        berita_featured = Berita.objects.filter(is_published=True).order_by('-created_at')[:4]
        from apps.kesiapan.models import PenilaianKesiapan as PK
        cedera_count = PK.objects.filter(ada_cedera=True).values('atlet').distinct().count()
    except Exception as e:
        # Log ke console Vercel agar debug, tapi jangan 500
        import logging

        logging.getLogger(__name__).warning(f"DB error di landing (fallback stats kosong): {e}")
        profil = None
        total_atlet = total_cabor = total_prestasi = jadwal_minggu_ini = cedera_count = 0
        top_atlet = []
        top_prestasi = []
        agenda = []
        jadwal = []
        berita_featured = []

    context = {
        'profil': profil,
        'total_atlet': total_atlet,
        'total_cabor': total_cabor,
        'total_prestasi': total_prestasi,
        'jadwal_minggu_ini': jadwal_minggu_ini,
        'top_atlet': top_atlet,
        'top_prestasi': top_prestasi,
        'agenda': agenda,
        'jadwal': jadwal,
        'today': timezone.now(),
        'berita_featured': berita_featured,
        'cedera_count': cedera_count,
    }
    return render(request, 'landing/home.html', context)


def tentang(request):
    profil = PerguruanProfil.objects.first()
    cabor_list = Cabor.objects.filter(aktif=True).order_by('nama')
    jadwal = JadwalLatihan.objects.filter(aktif=True).select_related('cabor').order_by('hari')[:6]
    return render(request, 'landing/tentang.html', {
        'profil': profil,
        'cabor_list': cabor_list,
        'jadwal': jadwal,
        'total_atlet': AtletProfile.objects.filter(status_aktif=True).count(),
        'total_cabor': cabor_list.count(),
    })


def berita_list(request):
    q = request.GET.get('q', '').strip()
    kategori = request.GET.get('kategori', '').strip()
    qs = Berita.objects.filter(is_published=True)
    if kategori:
        qs = qs.filter(kategori=kategori)
    if q:
        qs = qs.filter(Q(judul__icontains=q) | Q(ringkasan__icontains=q))
    return render(request, 'landing/berita_list.html', {
        'berita': qs.order_by('-created_at'),
        'q': q,
        'kategori': kategori,
        'kategori_choices': Berita.Kategori.choices,
    })


def berita_detail(request, slug):
    b = get_object_or_404(Berita, slug=slug, is_published=True)
    # increment views (atomik) — hitung setiap buka halaman
    Berita.objects.filter(pk=b.pk).update(views=F('views') + 1)
    b.refresh_from_db(fields=['views'])
    # berita terkait (kategori sama)
    terkait = Berita.objects.filter(is_published=True, kategori=b.kategori).exclude(pk=b.pk).order_by('-views', '-created_at')[:3]
    return render(request, 'landing/berita_detail.html', {'berita': b, 'terkait': terkait})


def prestasi_public(request):
    q = request.GET.get('q', '').strip()
    cabor_id = request.GET.get('cabor', '').strip()
    tingkat = request.GET.get('tingkat', '').strip()
    qs = Prestasi.objects.select_related('atlet', 'atlet__cabor').order_by('-tahun', '-id')
    if cabor_id:
        qs = qs.filter(atlet__cabor_id=cabor_id)
    if tingkat:
        qs = qs.filter(tingkat=tingkat)
    if q:
        qs = qs.filter(Q(nama_kejuaraan__icontains=q) | Q(atlet__nama_lengkap__icontains=q))
    total = qs.count()
    emas_count = qs.filter(Q(hasil__icontains='emas') | Q(hasil__icontains='juara 1')).count()
    tahun_terbaru = qs.values_list('tahun', flat=True).first()
    return render(request, 'landing/prestasi.html', {
        'prestasi': qs[:60],
        'cabor_list': Cabor.objects.filter(aktif=True).order_by('nama'),
        'q': q, 'cabor_id': cabor_id, 'tingkat': tingkat,
        'total': total, 'emas_count': emas_count, 'tahun_terbaru': tahun_terbaru,
    })


def kontak(request):
    profil = PerguruanProfil.objects.first()
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'landing/kontak.html', {'profil': profil, 'form': ContactMessageForm(), 'sent': True})
    else:
        form = ContactMessageForm()
    return render(request, 'landing/kontak.html', {'profil': profil, 'form': form})
