# SIMA — Sistem Interaktif Manajemen Atlet

## 1. Informasi Project

**SIMA** adalah aplikasi web fullstack untuk mengolah data para atlet beserta
tingkat kesiapannya hingga jadwal rutin latihan.

- **Pengguna utama 1 — Pelatih:** mengolah data atlet, menginput penilaian
  kesiapan rutin, mencatat prestasi, serta mengatur jadwal & dokumen atlet, agenda/event.
- **Pengguna utama 2 — Atlet/Anggota:** memantau data tentang dirinya sendiri
  (profil, tren kesiapan, prestasi, jadwal) dalam mode **view-only**, plus **upload dokumen sendiri** (KTP/KK/Akta/Ijazah dll dengan label bebas).
- **Pengguna ke-3 — Admin:** membuat akun, mengelola master cabor dan profil
  perguruan melalui Django Jazzmin (akses langsung `/admin/` — tidak ditampilkan sebagai link publik untuk mengurangi permukaan serangan).
- **Pengguna ke-4 — Jurnalis:** dashboard khusus untuk **upload berita & prestasi** (berita untuk landing, prestasi untuk hall-of-fame).
- **Tanpa registrasi publik.** Seluruh akun dibuat oleh admin. Halaman login
  adalah satu-satunya pintu masuk.

## 2. Tujuan

 1. Mendigitalkan biodata atlet (termasuk TB/BB), kategori/kelas, dan status aktif.
 2. Memantau kesiapan atlet secara berkala: fisik, teknik, mental (0–100),
    VO2Max, snapshot BB/TB, kehadiran, status cedera, dan catatan pelatih.
 3. Menyajikan statistik: tren kesiapan, top atlet, distribusi kehadiran,
    daftar cedera, dan prestasi terbaru — di landing page maupun dashboard.
  4. Mengelola jadwal latihan rutin mingguan dan agenda/event (try out,
     kejuaraan, latihan gabungan) — internal dashboard, tidak di-link publik (kontak yang tampil di landing).
  5. Memberi atlet akses transparan dan terbatas hanya pada datanya sendiri, termasuk kelola dokumen pribadi berlabel (KK/KTP/Akta/Ijazah/Surat Kesehatan/Lainnya).
  6. Memberi jurnalis ruang khusus untuk kurasi berita (rich text + kategori + cover + views) & prestasi tanpa akses ke data kesiapan/jadwal sensitif.
  7. Menyediakan halaman Kontak publik sebagai pengganti Jadwal di landing, plus inbox pesan untuk admin.

## 3. Tech Stack

| Lapisan   | Teknologi |
|-----------|-----------|
| Fullstack | Django 5.x + Django Template (tanpa SPA/DRF) |
| UI publik & dashboard | Bootstrap 5 (CDN) + minimalist modern tokens |
| Grafik    | Chart.js 4 (CDN) |
| Desain    | UI Pro Max — Modern minimal non-klasik · Outfit + Plus Jakarta Sans/Space Grotesk · weight 500-800, line-height 1.75, spacing lega · shapes subtle blob/arch/pill |
| Admin theme | django-jazzmin |
| Database dev | SQLite (`db.sqlite3`) |
| Database prod | MySQL/MariaDB via `PyMySQL` (switch lewat `.env`) |
| Config    | `python-dotenv` (`.env` / `.env.example`) |
| Static prod | `whitenoise` |
| Media upload | Pillow (`media/atlet/`, `media/prestasi/`, `media/perguruan/`, `media/dokumen/`, `media/berita/`) |
| Editor     | Quill 1.3.7 (CDN) untuk rich text Berita (heading/bold/italic/list/link/image, HTML disimpan, `|safe` di detail) |
| Zona waktu | Asia/Jakarta, bahasa `id` |
| Keamanan  | `/admin/` tidak ditautkan di UI publik/login/footer; hanya diketahui admin. Akun dibuat admin via Jazzmin. |

## 4. Peran & Hak Akses

| Fitur | Admin | Pelatih | Jurnalis | Atlet |
|-------|:-----:|:-------:|:--------:|:-----:|
| `/admin/` (Jazzmin, tidak di-link publik): user & semua data | ✅ | ❌ | ❌ | ❌ |
| Dashboard pelatih + CRUD atlet/kesiapan/jadwal/cabor/dokumen/profil | ✅ | ✅ | ❌ | ❌ |
| Input penilaian kesiapan | ✅ | ✅ | ❌ | ❌ |
| Kelola dokumen atlet (semua) | ✅ | ✅ | ❌ | ❌ |
| Dashboard jurnalis: berita + prestasi | ✅ | ❌ | ✅ | ❌ |
| Dashboard `/dashboard/saya/` (data + dokumen sendiri) | ❌ | ❌ | ❌ | ✅ |
| Landing + login | ✅ | ✅ | ✅ | ✅ |
| Registrasi publik | ❌ | ❌ | ❌ | ❌ |

Proteksi: `apps/accounts/decorators.py` (`role_required`, `admin_pelatih_required`, `jurnalis_required`, `admin_pelatih_jurnalis_required`);
superuser selalu lolos. Atlet hanya CRUD dokumen miliknya sendiri (`atlet` dikunci ke profilnya, delete 404 bila bukan miliknya). Jurnalis hanya edit/hapus berita miliknya sendiri (admin bebas). Atlet yang akunnya belum ditautkan ke `AtletProfile`
melihat halaman instruksi `atlet_noprofile.html`.

## 5. Struktur Project

```
SIMA/
├── manage.py
├── requirements.txt
├── .env / .env.example      # switch SQLite <-> MySQL
├── db.sqlite3               # dev saja
├── config/
│   ├── settings.py          # custom user, jazzmin, DB env, static/media, login URLs
│   └── urls.py              # admin, login/logout, dashboard/, landing /
├── apps/
│   ├── accounts/            # CustomUser(role: admin/pelatih/jurnalis/atlet), decorators, admin user
│   ├── atlets/              # Cabor, PerguruanProfil, AtletProfile, Prestasi, DokumenAtlet (+forms/admin)
│   ├── kesiapan/            # PenilaianKesiapan (+form/admin)
│   ├── jadwal/              # JadwalLatihan, AgendaEvent (+forms/admin) — internal saja
│   ├── dashboard/           # router + pelatih/atlet/jurnalis dashboards + CRUD dokumen/berita/prestasi
│   └── landing/             # homepage + tentang/berita(prestasi views+richtext+kategori)/prestasi/kontak + Berita/ContactMessage
├── templates/
│   ├── base.html            # nav modern sans (Outfit), palette slate/blue, typography 500-800 non-ramping, spacing 48px, shapes subtle, tanpa ikon berlebih — nav kini Kontak bukan Jadwal
│   ├── landing/home.html    # hero modern + KPI + berita ringkas + tentang/prestasi ringkas + kontak teaser (ganti jadwal)
│   ├── landing/tentang.html # modern non-klasik, visi/misi ringkas
│   ├── landing/berita_list.html + berita_detail.html  # kategori filter + views counter + rich-content safe HTML
│   ├── landing/prestasi.html  # filter ringkas
│   ├── landing/kontak.html  # form nama/email/subjek/pesan + info perguruan
│   ├── registration/login.html  # tanpa bocoran /admin
│   └── dashboard/           # layout 4 role + form-grid 2 kolom + Quill richtext untuk konten berita + list minimal
├── static/ / staticfiles/ / media/
└── scripts/
    └── seed_demo.py         # akun + data contoh
```

## 6. Model Data (ringkas)

- **CustomUser** — `username, password, role(admin/pelatih/jurnalis/atlet), no_hp`.
- **Cabor** — master cabang olahraga (diinput super admin).
- **PerguruanProfil** — 1 baris profil untuk landing (nama, tentang, visi, misi,
  alamat, kontak, logo).
- **AtletProfile** — `user(OneToOne, opsional)`, nama, JK, TTL, cabor FK,
  kelas/kategori, tahun masuk, `tinggi_cm`, `berat_kg`, status aktif, foto, kontak.
- **Prestasi** — atlet FK, kejuaraan, tingkat (kota/provinsi/nasional/internasional),
  hasil, tahun, bukti.
- **PenilaianKesiapan** — atlet FK + tanggal (unik), fisik/teknik/mental 0–100,
  `vo2max`, snapshot BB/TB, kehadiran (hadir/izin/sakit/alfa), `ada_cedera` +
  keterangan, catatan pelatih, `dinilai_oleh`. Properti: `rata_rata`, `status`
  (Siap Tanding ≥85 / Siap Latihan ≥70 / Perlu Pembinaan ≥50 / Belum Siap / Cedera).
- **JadwalLatihan** — cabor FK (kosong = umum), hari, jam mulai–selesai, lokasi,
  pelatih, kelompok, aktif.
- **AgendaEvent** — nama, jenis, tanggal mulai–selesai, lokasi, cabor, deskripsi.
- **Berita** — `judul/slug/kategori(umum/latihan/prestasi/event/pengumuman)`,
  ringkasan, `konten` (HTML rich text: heading/bold/italic/list/link/image via Quill, disimpan HTML, render `|safe`), cover, `views` (auto +1 tiap buka detail), `is_published/is_featured`, penulis FK, timestamps.
  Input kategori wajib ada; layout teks & gambar dapat diatur lewat editor. Slug auto dari judul.
- **ContactMessage** — `nama, email, subjek, pesan, is_read, created_at` — dari halaman Kontak publik.
- **DokumenAtlet** — `atlet FK, label(Char, bebas: KTP/KK/Akta/Ijazah/SKK dll), file, keterangan, uploaded_by FK, created_at`. Diinput admin/pelatih (untuk siapa saja) atau atlet sendiri (atlet dikunci ke profilnya).

## 7. Peta URL

```
GET  /                                  landing (kontak teaser ganti jadwal)
GET  /tentang/                          tentang kami (visi/misi, cabor)
GET  /berita/  GET /berita/<slug>/      berita list (filter kategori/q, tampil kategori & views) + detail (views +1, rich HTML, terkait)
GET  /prestasi/                         halaman prestasi publik (filter cabor/tingkat/q)
GET  /kontak/                           kontak publik (info perguruan + form → ContactMessage) — menggantikan Jadwal di landing
GET  /login/  POST /logout/             auth (tanpa register)
GET  /admin/                            jazzmin (tidak di-link di UI — akses langsung, admin only; kini termasuk Berita.views & ContactMessage)
GET  /dashboard/                        router by role (admin/pelatih→pelatih, jurnalis→jurnalis, atlet→saya)
GET  /dashboard/pelatih/                overview + Chart.js
GET  /dashboard/jurnalis/               overview jurnalis (berita+prestasi)
GET  /dashboard/saya/                   dashboard atlet (view-only + dokumen saya)
CRUD /dashboard/pelatih/atlet/... 
CRUD /dashboard/pelatih/kesiapan/...
CRUD /dashboard/pelatih/prestasi/...    (juga untuk jurnalis)
CRUD /dashboard/jurnalis/berita/...     (jurnalis, admin bebas; jurnalis hanya miliknya; form rich text Quill)
CRUD /dashboard/pelatih/dokumen/...     (admin/pelatih kelola semua)
CRUD /dashboard/saya/dokumen/...        (atlet kelola miliknya sendiri)
CRUD /dashboard/pelatih/jadwal/... + event/...   (internal dashboard, tidak tampil di landing)
     /dashboard/pelatih/cabor/ + profil-perguruan/
```

## 8. Cara Menjalankan (dev)

```bash
cd SIMA
.venv/bin/pip install -r requirements.txt
cp .env.example .env            # default SQLite, langsung jalan
.venv/bin/python manage.py migrate
.venv/bin/python scripts/seed_demo.py   # opsional: data contoh
.venv/bin/python manage.py runserver
```

Akun demo (ganti di production): `admin/admin123`, `pelatih1/pelatih123`,
`jurnalis1/jurnalis123`, `atlet1/atlet123` (juga `atlet2`, `atlet3`). Admin link tidak ditampilkan di UI.

## 9. Migrasi ke MySQL

1. Siapkan database MySQL/MariaDB (lokal/hosting) — host, port, database, user, password.
2. Isi `.env`: `DB_ENGINE=mysql`, `DB_HOST`, `DB_PORT=3306`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
3. `.venv/bin/python manage.py migrate` (+ `createsuperuser` bila DB kosong).
Tanpa perubahan kode — `config/settings.py` memilih engine dari `.env`.

## 10. Protokol Check & Test (wajib tiap pembaruan)

Setiap ada fitur baru / perubahan kode, jalankan minimal:

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py shell -c "..."   # smoke test Test Client:
# landing 200, login 200, anon redirect 302, dashboard pelatih 200,
# tiap list CRUD 200, POST valid -> 302 + tersimpan, POST invalid -> 200 (ditolak),
# atlet dashboard 200, atlet diblokir dari rute pelatih -> 403, /admin/login/ 200
```

Hasil terakhir (07-09-2026): `check` bersih, **15/15 test lolos** — kategori+views+rich text verified (views +1 per buka, HTML <h2>/<strong>/link/img disimpan & render safe), kontak (landing teaser + /kontak/ form → ContactMessage), jadwal diganti kontak (nav & landing). Full suite sebelumnya 27/27 & 12/12.

## 11. Desain — Modern Non-Klasik, Clear & Spacious (UI Pro Max)

- **Style:** Modern minimal — bukan klasik serif. Sans tegas: `Outfit` 800 untuk heading + `Plus Jakarta Sans` / `Space Grotesk` 500-700 untuk body. Weight tidak ramping (500-800), line-height 1.75, size 16px.
- **Spacing lega:** section `48px` vertikal, hero `64px`, card `28px`, grid `g-4/g-5` — tiap section diberi napas, teks di-clamp 2–3 baris agar tidak bosan membaca.
- **Palette:** paper `#F8F9FB`, stone `#F1F3F7`, ink `#0F172A`, line `#E6E9EF`, accent modern blue `#2563EB` / `#0EA5E9` (bukan champagne klasik).
- **Ikon minimal:** navbar & home tanpa `fa-*` berlebih (home 0 ikon), hanya huruf `S` brand-mark dan dot status — tidak membebani visual.
- **Layout input fleksibel:** `templates/dashboard/form.html:1` — `.form-grid` 2 kolom (1 kolom di mobile), checkbox full-width dengan background stone, tombol pill — tidak memanjang ke bawah.