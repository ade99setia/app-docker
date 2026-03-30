# 🗂️ Panduan Mengelola Volume Docker (Tanpa Masuk Container)

Dokumentasi ini menjelaskan cara mengakses **Named Volume Docker** secara langsung tanpa perlu masuk ke dalam container.

Digunakan untuk:

* melihat file Laravel (`public`, `storage`)
* upload file manual
* hapus cache
* edit file langsung
* debugging cepat

---

# 🧠 Konsep Dasar

Named Volume Docker sebenarnya adalah folder fisik di server Linux:

```
/var/lib/docker/volumes/<volume_name>/_data/
```

Contoh:

```
/var/lib/docker/volumes/idn-solo_public_app/_data/
/var/lib/docker/volumes/idn-solo_storage_app/_data/
```

---

# 📊 Metode Akses

| Metode                  | Kapan Digunakan   | GUI | Direkomendasikan |
| ----------------------- | ----------------- | --- | ---------------- |
| Filebrowser             | penggunaan harian | ✅   | ⭐ paling aman    |
| SSH CLI                 | cepat / scripting | ❌   | advanced         |
| SFTP (WinSCP/FileZilla) | drag & drop       | ✅   | alternatif       |

---

# 🛠️ Cara 1 — Jalur Visual (Filebrowser) ⭐ Recommended

Dokumentasi ini menjelaskan cara menggabungkan akses folder lokal (Home) dan Volume Docker (Laravel) ke dalam satu tampilan Filebrowser.

## 🚀 Fitur yang Tersedia
Setelah konfigurasi ini diterapkan, kamu bisa melakukan operasi berikut langsung dari browser:
* ✅ **Upload & Download** file secara langsung.
* ✅ **Delete** file/folder yang tidak diperlukan.
* ✅ **Rename** folder untuk merapikan struktur.
* ✅ **Edit** file (seperti `.env`, `.php`, `.html`) dengan editor bawaan.
* ✅ **Drag & Drop** file dari komputer lokal ke server.

---

## 🛠️ Konfigurasi `docker-compose.yml`

Gunakan konfigurasi di bawah ini untuk menggabungkan akses folder Home dan Volume Laravel:

```yaml
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    ports:
      - "8085:80"
    volumes:
      # 1. Akses Folder Home (Lokal Server)
      - /home/ade-setia:/srv/ade-setia
      
      # 2. Akses Volume External (Laravel)
      - idn-solo_public_app:/srv/idn-solo_public_app
      - idn-solo_storage_app:/srv/idn-solo_storage_app
      
      # 3. Database & Konfigurasi Filebrowser (Agar user/pass tidak reset)
      - ./filebrowser.db:/database/filebrowser.db
      
    environment:
      - FB_DATABASE=/database/filebrowser.db
    restart: always

# Deklarasi volume yang dibuat oleh project lain (Laravel)
volumes:
  idn-solo_public_app:
    external: true
  idn-solo_storage_app:
    external: true
```

---

## 📖 Penjelasan Mapping Volume

Konsep yang digunakan adalah `- [SUMBER]:[TAMPILAN DI UI]`. Semua yang diarahkan ke dalam folder `/srv/` di sisi kanan akan muncul sebagai folder utama di tampilan Filebrowser.

| Sumber (Host/Volume) | Tampilan di Filebrowser | Keterangan |
| :--- | :--- | :--- |
| `/home/ade-setia` | `/ade-setia` | Folder home user di server lokal. |
| `idn-solo_public_app` | `/idn-solo_public_app` | Folder public Laravel (Assets, Index, dll). |
| `idn-solo_storage_app` | `/idn-solo_storage_app` | Folder storage Laravel (Logs, Uploads, dll). |

---

## ⚙️ Cara Menerapkan Perubahan

1.  Buka terminal di direktori file `docker-compose.yml` berada.
2.  Hentikan container yang lama (jika ada):
    ```bash
    docker compose down
    ```
3.  Jalankan kembali dengan konfigurasi baru:
    ```bash
    docker compose up -d
    ```
4.  Buka browser di alamat `http://alamat-ip-server:8085`.

---

> **Catatan:** Jika folder atau volume tidak muncul, pastikan nama volume di bagian `volumes: external: true` sudah sesuai dengan hasil dari perintah `docker volume ls`.

---

# 💻 Cara 2 — Jalur Direct (SSH CLI)

Digunakan untuk operasi cepat atau massal.

---

## 1. Masuk Root

```bash
sudo su
```

---

## 2. Masuk ke Volume

```bash
cd /var/lib/docker/volumes/idn-solo_public_app/_data
```

atau

```bash
cd /var/lib/docker/volumes/idn-solo_storage_app/_data
```

---

## 3. Perintah yang Bisa Digunakan

Lihat isi folder

```bash
ls -la
```

Hapus file

```bash
rm -rf nama_folder
```

Edit file

```bash
nano index.php
```

Buat folder

```bash
mkdir test
```

---

# 🖥️ Cara 3 — Jalur GUI via SFTP

Cocok jika ingin drag & drop dari komputer.

---

## Tools

* WinSCP (Windows)
* FileZilla
* Cyberduck (Mac)

---

## Langkah

1. Login ke server via SFTP
2. Gunakan user **root**
3. Masuk ke path:

```
/var/lib/docker/volumes/idn-solo_storage_app/_data/
```

atau

```
/var/lib/docker/volumes/idn-solo_public_app/_data/
```

4. Drag & drop file seperti flashdisk

---

# ⚠️ Penting

* Jangan hapus folder `_data`
* Jangan rename volume
* Jangan edit saat container sedang build
* Gunakan root hanya jika perlu

---

# 🔎 Cek Volume Terpasang di Container

```bash
docker inspect idn-solo_app
```

---

# 🧹 Hapus Volume (HATI-HATI)

```bash
docker volume rm idn-solo_public_app
```

⚠️ Akan menghapus semua file permanen

---

# 🧠 Best Practice

* gunakan Filebrowser untuk harian
* gunakan SSH untuk operasi massal
* gunakan SFTP jika butuh drag drop
* jangan edit file saat deploy berjalan
* backup sebelum hapus file penting

---

# 🎯 Use Case Umum

| Kebutuhan        | Cara        |
| ---------------- | ----------- |
| upload gambar    | Filebrowser |
| hapus cache      | SSH         |
| edit config      | Filebrowser |
| copy file banyak | SFTP        |
| debugging        | SSH         |

---

# 📦 Struktur Volume Laravel

```
public_app
 ├── index.php
 ├── build/
 └── assets/

storage_app
 ├── logs/
 ├── framework/
 └── app/
```

---

# 🚀 Ringkasan

* volume docker = folder fisik
* bisa diakses tanpa masuk container
* Filebrowser = paling mudah
* SSH = paling cepat
* SFTP = drag & drop GUI
