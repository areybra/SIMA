import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, Count, ExpressionWrapper, F, FloatField, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.decorators import admin_pelatih_required, jurnalis_required, role_required
from apps.accounts.decorators import admin_pelatih_jurnalis_required
from apps.atlets.forms import AtletProfileForm, CaborForm, DokumenAtletForm, PerguruanProfilForm, PrestasiForm
from apps.atlets.models import AtletProfile, Cabor, DokumenAtlet, PerguruanProfil, Prestasi
from apps.jadwal.forms import AgendaEventForm, JadwalLatihanForm
from apps.jadwal.models import AgendaEvent, JadwalLatihan
from apps.kesiapan.forms import PenilaianKesiapanForm
from apps.kesiapan.models import PenilaianKesiapan
from apps.landing.forms import BeritaForm
from apps.landing.models import Berita


@login_required
def dashboard_router(request):
    user = request.user
    role = getattr(user, 'role', '')
    if user.is_superuser or role == 'admin':
        return redirect('dashboard-pelatih')
    if role == 'pelatih':
        return redirect('dashboard-pelatih')
    if role == 'jurnalis':
        return redirect('dashboard-jurnalis')
    return redirect('dashboard-atlet')


@admin_pelatih_required
def pelatih_dashboard(request):
    rata_expr = ExpressionWrapper((F('fisik') + F('teknik') + F('mental')) / 3.0, output_field=FloatField())
    total_atlet = AtletProfile.objects.filter(status_aktif=True).count()
    total_pelatih = __import__('apps.accounts.models', fromlist=['CustomUser']).CustomUser.objects.filter(role='pelatih').count()
    total_prestasi = Prestasi.objects.count()
    cedera_aktif = PenilaianKesiapan.objects.filter(ada_cedera=True).values('atlet').distinct().count()

    tren = (
        PenilaianKesiapan.objects.values('tanggal')
        .annotate(rata=Avg(rata_expr))
        .order_by('tanggal')[:30]
    )
    tren_labels = [t['tanggal'].strftime('%d/%m') for t in tren]
    tren_data = [round(t['rata'] or 0, 1) for t in tren]

    hadir = PenilaianKesiapan.objects.values('kehadiran').annotate(jml=Count('id'))
    hadir_map = {h['kehadiran']: h['jml'] for h in hadir}

    top = (
        PenilaianKesiapan.objects.values('atlet__nama_lengkap')
        .annotate(rata=Avg(rata_expr))
        .order_by('-rata')[:5]
    )
    cedera_list = PenilaianKesiapan.objects.filter(ada_cedera=True).select_related('atlet').order_by('-tanggal')[:5]
    terbaru = PenilaianKesiapan.objects.select_related('atlet').order_by('-tanggal')[:8]
    agenda = AgendaEvent.objects.order_by('tanggal_mulai')[:5]

    context = {
        'total_atlet': total_atlet,
        'total_pelatih': total_pelatih,
        'total_prestasi': total_prestasi,
        'cedera_aktif': cedera_aktif,
        'tren_labels': json.dumps(tren_labels, cls=DjangoJSONEncoder),
        'tren_data': json.dumps(tren_data, cls=DjangoJSONEncoder),
        'hadir_map': hadir_map,
        'top': top,
        'cedera_list': cedera_list,
        'terbaru': terbaru,
        'agenda': agenda,
    }
    return render(request, 'dashboard/pelatih.html', context)


@role_required('atlet')
def atlet_dashboard(request):
    profil = getattr(request.user, 'atlet_profile', None)
    if profil is None:
        return render(request, 'dashboard/atlet_noprofile.html')
    penilaian = profil.penilaian.order_by('tanggal')[:30]
    labels = [p.tanggal.strftime('%d/%m') for p in penilaian]
    fisik = [p.fisik for p in penilaian]
    teknik = [p.teknik for p in penilaian]
    mental = [p.mental for p in penilaian]
    vo2 = [float(p.vo2max) if p.vo2max else None for p in penilaian]
    terakhir = profil.penilaian.order_by('-tanggal').first()
    prestasi = profil.prestasi.order_by('-tahun')
    dokumen = profil.dokumen.order_by('-created_at')[:12]
    jadwal = JadwalLatihan.objects.filter(aktif=True).select_related('cabor')
    agenda = AgendaEvent.objects.order_by('tanggal_mulai')[:5]
    context = {
        'profil': profil,
        'terakhir': terakhir,
        'prestasi': prestasi,
        'dokumen': dokumen,
        'jadwal': jadwal,
        'agenda': agenda,
        'labels': json.dumps(labels, cls=DjangoJSONEncoder),
        'fisik': json.dumps(fisik),
        'teknik': json.dumps(teknik),
        'mental': json.dumps(mental),
        'vo2': json.dumps(vo2),
        'penilaian': profil.penilaian.order_by('-tanggal')[:10],
    }
    return render(request, 'dashboard/atlet.html', context)


# ---- Jurnalis dashboard ----
@jurnalis_required
def jurnalis_dashboard(request):
    total_berita = Berita.objects.count()
    total_published = Berita.objects.filter(is_published=True).count()
    total_draft = total_berita - total_published
    total_prestasi = Prestasi.objects.count()
    berita_terbaru = Berita.objects.order_by('-created_at')[:6]
    prestasi_terbaru = Prestasi.objects.select_related('atlet').order_by('-tahun', '-id')[:6]
    return render(request, 'dashboard/jurnalis.html', {
        'total_berita': total_berita,
        'total_published': total_published,
        'total_draft': total_draft,
        'total_prestasi': total_prestasi,
        'berita_terbaru': berita_terbaru,
        'prestasi_terbaru': prestasi_terbaru,
    })


@jurnalis_required
def berita_jurnalis_list(request):
    q = request.GET.get('q', '').strip()
    qs = Berita.objects.order_by('-created_at')
    if q:
        qs = qs.filter(Q(judul__icontains=q) | Q(ringkasan__icontains=q))
    return render(request, 'dashboard/berita_list.html', {'object_list': qs, 'q': q})


@jurnalis_required
def berita_jurnalis_create(request):
    form = BeritaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.penulis = request.user
        obj.save()
        return redirect('berita-jurnalis-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Tambah Berita'})


@jurnalis_required
def berita_jurnalis_update(request, pk):
    obj = get_object_or_404(Berita, pk=pk)
    # jurnalis hanya boleh edit miliknya sendiri kecuali admin
    if not request.user.is_superuser and getattr(request.user, 'role', '') == 'jurnalis' and obj.penulis and obj.penulis != request.user:
        raise PermissionDenied('Anda hanya boleh mengubah berita milik Anda.')
    form = BeritaForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('berita-jurnalis-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': f'Ubah Berita: {obj.judul}'})


@jurnalis_required
def berita_jurnalis_delete(request, pk):
    obj = get_object_or_404(Berita, pk=pk)
    if not request.user.is_superuser and getattr(request.user, 'role', '') == 'jurnalis' and obj.penulis and obj.penulis != request.user:
        raise PermissionDenied('Anda hanya boleh menghapus berita milik Anda.')
    if request.method == 'POST':
        obj.delete()
        return redirect('berita-jurnalis-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


# ---------- generic CRUD helper ----------
def _crud_list_create(request, model, form_class, template, redirect_name, order='-id'):
    qs = model.objects.all().order_by(order) if hasattr(model.objects, 'all') else None
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            if isinstance(obj, PenilaianKesiapan) and not obj.dinilai_oleh:
                obj.dinilai_oleh = request.user
                obj.save()
            return redirect(redirect_name)
    else:
        form = form_class()
    return render(request, template, {'object_list': qs, 'form': form})


@admin_pelatih_required
def atlet_list(request):
    q = request.GET.get('q', '')
    cabor_id = request.GET.get('cabor', '')
    qs = AtletProfile.objects.select_related('cabor', 'user').order_by('nama_lengkap')
    if q:
        qs = qs.filter(nama_lengkap__icontains=q)
    if cabor_id:
        qs = qs.filter(cabor_id=cabor_id)
    return render(request, 'dashboard/atlet_list.html', {
        'object_list': qs, 'q': q, 'cabor_id': cabor_id,
        'cabor_list': Cabor.objects.filter(aktif=True),
    })


@admin_pelatih_required
def atlet_create(request):
    form = AtletProfileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('atlet-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Tambah Atlet'})


@admin_pelatih_required
def atlet_update(request, pk):
    obj = get_object_or_404(AtletProfile, pk=pk)
    form = AtletProfileForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('atlet-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': f'Ubah Atlet: {obj.nama_lengkap}'})


@admin_pelatih_required
def atlet_delete(request, pk):
    obj = get_object_or_404(AtletProfile, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('atlet-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


@admin_pelatih_required
def penilaian_list(request):
    qs = PenilaianKesiapan.objects.select_related('atlet', 'atlet__cabor').order_by('-tanggal')
    atlet_id = request.GET.get('atlet', '')
    if atlet_id:
        qs = qs.filter(atlet_id=atlet_id)
    return render(request, 'dashboard/penilaian_list.html', {
        'object_list': qs[:200],
        'atlet_list': AtletProfile.objects.order_by('nama_lengkap'),
        'atlet_id': atlet_id,
    })


@admin_pelatih_required
def penilaian_create(request):
    form = PenilaianKesiapanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.dinilai_oleh = request.user
        obj.save()
        return redirect('penilaian-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Input Penilaian Kesiapan'})


@admin_pelatih_required
def penilaian_update(request, pk):
    obj = get_object_or_404(PenilaianKesiapan, pk=pk)
    form = PenilaianKesiapanForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('penilaian-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Ubah Penilaian'})


@admin_pelatih_required
def penilaian_delete(request, pk):
    obj = get_object_or_404(PenilaianKesiapan, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('penilaian-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


@admin_pelatih_jurnalis_required
def prestasi_list(request):
    qs = Prestasi.objects.select_related('atlet').order_by('-tahun')
    return render(request, 'dashboard/prestasi_list.html', {'object_list': qs})


@admin_pelatih_jurnalis_required
def prestasi_create(request):
    form = PrestasiForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        # jurnalis kembali ke list jurnalis bila bukan pelatih
        if getattr(request.user, 'role', '') == 'jurnalis':
            return redirect('prestasi-list')
        return redirect('prestasi-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Tambah Prestasi'})


@admin_pelatih_jurnalis_required
def prestasi_update(request, pk):
    obj = get_object_or_404(Prestasi, pk=pk)
    form = PrestasiForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('prestasi-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Ubah Prestasi'})


@admin_pelatih_jurnalis_required
def prestasi_delete(request, pk):
    obj = get_object_or_404(Prestasi, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('prestasi-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


@admin_pelatih_required
def jadwal_list(request):
    return render(request, 'dashboard/jadwal_list.html', {
        'jadwal': JadwalLatihan.objects.select_related('cabor').order_by('hari'),
        'agenda': AgendaEvent.objects.order_by('tanggal_mulai'),
    })


@admin_pelatih_required
def jadwal_create(request):
    form = JadwalLatihanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('jadwal-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Tambah Jadwal Latihan'})


@admin_pelatih_required
def jadwal_update(request, pk):
    obj = get_object_or_404(JadwalLatihan, pk=pk)
    form = JadwalLatihanForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('jadwal-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Ubah Jadwal'})


@admin_pelatih_required
def jadwal_delete(request, pk):
    obj = get_object_or_404(JadwalLatihan, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('jadwal-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


@admin_pelatih_required
def event_create(request):
    form = AgendaEventForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('jadwal-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Tambah Agenda/Event'})


@admin_pelatih_required
def event_update(request, pk):
    obj = get_object_or_404(AgendaEvent, pk=pk)
    form = AgendaEventForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('jadwal-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Ubah Agenda/Event'})


@admin_pelatih_required
def event_delete(request, pk):
    obj = get_object_or_404(AgendaEvent, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('jadwal-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


@admin_pelatih_required
def cabor_list(request):
    if request.method == 'POST':
        form = CaborForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cabor-list')
    else:
        form = CaborForm()
    return render(request, 'dashboard/cabor_list.html', {
        'object_list': Cabor.objects.order_by('nama'), 'form': form,
    })


@admin_pelatih_required
def cabor_delete(request, pk):
    obj = get_object_or_404(Cabor, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('cabor-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


@admin_pelatih_required
def profil_perguruan(request):
    obj = PerguruanProfil.objects.first()
    form = PerguruanProfilForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard-pelatih')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Profil Perguruan (Landing Page)'})


# ---- Dokumen Atlet ----
@admin_pelatih_required
def dokumen_list(request):
    q = request.GET.get('q', '').strip()
    atlet_id = request.GET.get('atlet', '').strip()
    qs = DokumenAtlet.objects.select_related('atlet', 'uploaded_by').order_by('-created_at')
    if q:
        qs = qs.filter(Q(label__icontains=q) | Q(atlet__nama_lengkap__icontains=q))
    if atlet_id:
        qs = qs.filter(atlet_id=atlet_id)
    return render(request, 'dashboard/dokumen_list.html', {
        'object_list': qs[:200],
        'atlet_list': AtletProfile.objects.order_by('nama_lengkap'),
        'q': q, 'atlet_id': atlet_id,
        'is_admin_view': True,
    })


@admin_pelatih_required
def dokumen_create(request):
    form = DokumenAtletForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.uploaded_by = request.user
        obj.save()
        return redirect('dokumen-list')
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Tambah Dokumen Atlet'})


@admin_pelatih_required
def dokumen_delete(request, pk):
    obj = get_object_or_404(DokumenAtlet, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('dokumen-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})


@role_required('atlet')
def dokumen_saya_list(request):
    profil = getattr(request.user, 'atlet_profile', None)
    if profil is None:
        return render(request, 'dashboard/atlet_noprofile.html')
    qs = profil.dokumen.select_related('uploaded_by').order_by('-created_at')
    return render(request, 'dashboard/dokumen_list.html', {
        'object_list': qs,
        'is_admin_view': False,
    })


@role_required('atlet')
def dokumen_saya_create(request):
    profil = getattr(request.user, 'atlet_profile', None)
    if profil is None:
        return render(request, 'dashboard/atlet_noprofile.html')
    form = DokumenAtletForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        # paksa atlet = profil sendiri agar tidak bisa spoof
        obj.atlet = profil
        obj.uploaded_by = request.user
        obj.save()
        return redirect('dokumen-saya-list')
    # preset atlet di form
    form.fields['atlet'].initial = profil
    return render(request, 'dashboard/form.html', {'form': form, 'title': 'Upload Dokumen Saya'})


@role_required('atlet')
def dokumen_saya_delete(request, pk):
    profil = getattr(request.user, 'atlet_profile', None)
    obj = get_object_or_404(DokumenAtlet, pk=pk, atlet=profil)
    if request.method == 'POST':
        obj.delete()
        return redirect('dokumen-saya-list')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj})
