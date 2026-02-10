# 🔨 Build & Release Guide

Panduan ini menjelaskan cara melakukan build otomatis aplikasi Perpustakaan menjadi file executable (`.exe` untuk Windows, Binary untuk Linux) menggunakan GitHub Actions.

## 📄 Tentang Workflow (`.github/workflows/build.yml`)

File konfigurasi ini mengatur proses build otomatis. Berikut penjelasan singkat bagian-bagiannya:

### 1. Triggers (`on`)
- **`push`**: Build akan otomatis berjalan setiap kali Anda melakukan push ke branch `main` atau `master`.
- **`workflow_dispatch`**: Tombol manual untuk menjalan build kapan saja dari tab "Actions" di GitHub.

### 2. Jobs (`build-windows` & `build-linux`)
Workflow ini menjalankan dua proses parallel:
- **Windows**: Menggunakan runner `windows-latest`.
- **Linux**: Menggunakan runner `ubuntu-latest`.

Setiap job melakukan langkah berikut:
1. **Checkout**: Mengambil kode terbaru dari repository.
2. **Setup Python**: Menginstall Python 3.11.
3. **Install Dependencies**: Menginstall library yang diperlukan (`PySide6`, `pyinstaller`, dll) dari `requirements.txt`.
4. **Build**: Menjalankan perintah `pyinstaller` untuk mengemas aplikasi menjadi satu file (`--onefile`).
   - Folder `assets` disertakan secara otomatis.
5. **Upload Artifact**: Mengunggah hasil build agar bisa didownload.

---

## 🚀 Cara Menjalankan Build

### Otomatis
Cukup lakukan commit dan push perubahan ke GitHub:
```bash
git add .
git commit -m "Update kode"
git push origin main
```
Build akan otomatis berjalan.

### Manual
1. Buka repository Anda di GitHub.
2. Klik tab **Actions**.
3. Pilih workflow **"Build Application"** di sidebar kiri.
4. Klik tombol **Run workflow** di sebelah kanan.

---

## 📥 Cara Download Hasil Build

Setelah proses build selesai (centang hijau):

1. Buka tab **Actions** di GitHub.
2. Klik pada **workflow run** terbaru (paling atas).
3. Scroll ke bawah ke bagian **Artifacts**.
4. Anda akan melihat dua file:
   - `windows-build` (Berisi file `.exe`)
   - `linux-build` (Berisi binary Linux)
5. Klik nama artifact untuk mendownload file `.zip`.
6. Ekstrak file tersebut untuk mendapatkan aplikasi siap pakai.

---

## ⚠️ Catatan Penting
- **Database**: File `library.db` tidak disertakan dalam build. Aplikasi akan otomatis membuat database baru saat pertama kali dijalankan di komputer pengguna.
- **Assets**: Pastikan file aset (gambar/ikon) ada di dalam folder `library_system/assets` agar ikut ter-build.

## 🛠️ Troubleshooting

### Linux: Permission Denied
Jika Anda mengalami error `Permission denied` saat menjalankan binary di Linux:
1. Buka terminal.
2. Berikan izin eksekusi:
   ```bash
   chmod +x library-system-linux
   ```
3. Jalankan kembali:
   ```bash
   ./library-system-linux
   ```

---

## 📦 Otomatisasi Release (v1.0, v2.0, dll)

Untuk membuat **GitHub Release** resmi beserta file binary yang siap didownload secara publik:

1. Buat **Tag** baru di git (misal `v1.0`):
   ```bash
   git tag v1.0
   git push origin v1.0
   ```
2. GitHub Actions akan otomatis:
   - Membuat Release baru dengan judul "v1.0".
   - Membuild aplikasi untuk Windows & Linux.
   - Mengupload file `.exe` dan binary ke halaman Releases.

