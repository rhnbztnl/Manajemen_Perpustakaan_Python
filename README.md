# 📚 Sistem Manajemen Perpustakaan (Library Management System)

Aplikasi desktop modern untuk pengelolaan perpustakaan yang dibangun dengan **Python** dan **PySide6 (Qt)**.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## ✨ Fitur Utama

- **Dashboard Interaktif**: Ringkasan cepat statistik perpustakaan (Total Buku, Anggota, Peminjaman).
- **Manajemen Buku**: Tambah, edit, hapus, dan cari data buku dengan mudah.
- **Manajemen Anggota**: Kelola data anggota, status aktif/nonaktif.
- **Sistem Peminjaman**: 
  - Catat peminjaman dan pengembalian buku.
  - Perhitungan denda otomatis untuk keterlambatan.
- **Laporan Komprehensif**:
  - Analisa peminjaman per periode.
  - Daftar keterlambatan (Overdue).
  - Statistik buku terpopuler & stok mati.
  - **Export ke CSV** untuk analisa lebih lanjut.
- **Pengaturan Aplikasi**: Konfigurasi denda, durasi pinjam, dan tema aplikasi (Light/Dark Mode).

## 🛠️ Teknologi yang Digunakan

- **Bahasa**: Python 3.10+
- **GUI Framework**: PySide6 (Qt for Python)
- **Database**: SQLite3
- **Struktur Proyek**: Modular MVC (Model-View-Controller) pattern

## 🚀 Cara Instalasi

### Prasyarat
Pastikan Python sudah terinstal di komputer Anda.

1. **Clone Repository**
   ```bash
   git clone https://github.com/rhnbztnl/Manajemen_Perpustakaan_Python.git
   cd Manajemen_Perpustakaan_Python
   ```

2. **Buat Virtual Environment (Opsional tapi Disarankan)**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Jika file `requirements.txt` belum ada, install PySide6 secara manual:*
   ```bash
   pip install PySide6
   ```

4. **Jalankan Aplikasi**
   ```bash
   python main_app.py
   ```

## 📂 Struktur Folder

```
Manajemen-Perpustakaan/
├── library_system/        # Source code utama
│   ├── database/          # Koneksi & inisialisasi SQLite
│   ├── managers/          # Logika bisnis & settings
│   ├── models/            # Model data untuk QTableView
│   ├── pages/             # Halaman UI (Dashboard, Books, dll)
│   ├── services/          # Service layer (Query SQL)
│   ├── ui/                # Komponen UI reusable (Sidebar, Dialogs)
│   └── utils/             # Utility helper (Export, Paths)
├── main_app.py            # Entry point aplikasi
├── library.db             # File database SQLite (otomatis dibuat)
└── README.md              # Dokumentasi proyek
```

## 🖼️ Screenshot

*(Tambahkan screenshot aplikasi di sini)*

## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan buat *Pull Request* atau laporkan *Issues*.

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).