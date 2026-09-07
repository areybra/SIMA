from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard_router, name='dashboard-router'),
    path('pelatih/', views.pelatih_dashboard, name='dashboard-pelatih'),
    path('saya/', views.atlet_dashboard, name='dashboard-atlet'),
    path('jurnalis/', views.jurnalis_dashboard, name='dashboard-jurnalis'),
    # Atlet CRUD
    path('pelatih/atlet/', views.atlet_list, name='atlet-list'),
    path('pelatih/atlet/tambah/', views.atlet_create, name='atlet-create'),
    path('pelatih/atlet/<int:pk>/ubah/', views.atlet_update, name='atlet-update'),
    path('pelatih/atlet/<int:pk>/hapus/', views.atlet_delete, name='atlet-delete'),
    # Penilaian
    path('pelatih/kesiapan/', views.penilaian_list, name='penilaian-list'),
    path('pelatih/kesiapan/tambah/', views.penilaian_create, name='penilaian-create'),
    path('pelatih/kesiapan/<int:pk>/ubah/', views.penilaian_update, name='penilaian-update'),
    path('pelatih/kesiapan/<int:pk>/hapus/', views.penilaian_delete, name='penilaian-delete'),
    # Prestasi (pelatih + jurnalis)
    path('pelatih/prestasi/', views.prestasi_list, name='prestasi-list'),
    path('pelatih/prestasi/tambah/', views.prestasi_create, name='prestasi-create'),
    path('pelatih/prestasi/<int:pk>/ubah/', views.prestasi_update, name='prestasi-update'),
    path('pelatih/prestasi/<int:pk>/hapus/', views.prestasi_delete, name='prestasi-delete'),
    # Berita jurnalis
    path('jurnalis/berita/', views.berita_jurnalis_list, name='berita-jurnalis-list'),
    path('jurnalis/berita/tambah/', views.berita_jurnalis_create, name='berita-jurnalis-create'),
    path('jurnalis/berita/<int:pk>/ubah/', views.berita_jurnalis_update, name='berita-jurnalis-update'),
    path('jurnalis/berita/<int:pk>/hapus/', views.berita_jurnalis_delete, name='berita-jurnalis-delete'),
    # Dokumen (admin/pelatih)
    path('pelatih/dokumen/', views.dokumen_list, name='dokumen-list'),
    path('pelatih/dokumen/tambah/', views.dokumen_create, name='dokumen-create'),
    path('pelatih/dokumen/<int:pk>/hapus/', views.dokumen_delete, name='dokumen-delete'),
    # Dokumen saya (atlet)
    path('saya/dokumen/', views.dokumen_saya_list, name='dokumen-saya-list'),
    path('saya/dokumen/tambah/', views.dokumen_saya_create, name='dokumen-saya-create'),
    path('saya/dokumen/<int:pk>/hapus/', views.dokumen_saya_delete, name='dokumen-saya-delete'),
    # Jadwal & Event
    path('pelatih/jadwal/', views.jadwal_list, name='jadwal-list'),
    path('pelatih/jadwal/tambah/', views.jadwal_create, name='jadwal-create'),
    path('pelatih/jadwal/<int:pk>/ubah/', views.jadwal_update, name='jadwal-update'),
    path('pelatih/jadwal/<int:pk>/hapus/', views.jadwal_delete, name='jadwal-delete'),
    path('pelatih/event/tambah/', views.event_create, name='event-create'),
    path('pelatih/event/<int:pk>/ubah/', views.event_update, name='event-update'),
    path('pelatih/event/<int:pk>/hapus/', views.event_delete, name='event-delete'),
    # Master
    path('pelatih/cabor/', views.cabor_list, name='cabor-list'),
    path('pelatih/cabor/<int:pk>/hapus/', views.cabor_delete, name='cabor-delete'),
    path('pelatih/profil-perguruan/', views.profil_perguruan, name='profil-perguruan'),
]
