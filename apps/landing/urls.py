from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('tentang/', views.tentang, name='tentang'),
    path('berita/', views.berita_list, name='berita-list'),
    path('berita/<slug:slug>/', views.berita_detail, name='berita-detail'),
    path('prestasi/', views.prestasi_public, name='prestasi-public'),
    path('kontak/', views.kontak, name='kontak'),
]
