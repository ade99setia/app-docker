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

Konsep:
Memasang volume Laravel ke container Filebrowser sebagai **external volume**.

---

## 1. Cek Nama Volume

```bash
docker volume ls
```

Contoh hasil:

```
idn-solo_public_app
idn-solo_storage_app
```

---

## 2. Edit docker-compose Filebrowser

```yaml
services:
  filebrowser:
    image: filebrowser/filebrowser
    container_name: filebrowser_app
    ports:
      - "8086:80"
    volumes:
      - ./filebrowser-data:/srv/utama
      - idn-solo_public_app:/srv/Laravel-Public
      - idn-solo_storage_app:/srv/Laravel-Storage
    restart: unless-stopped

volumes:
  idn-solo_public_app:
    external: true
  idn-solo_storage_app:
    external: true
```

---

## 3. Restart Filebrowser

```bash
docker compose up -d
```

---

## 4. Hasil

Di UI Filebrowser akan muncul:

```
/Laravel-Public
/Laravel-Storage
```

Sekarang bisa:

* upload file
* delete file
* rename folder
* edit file
* drag & drop

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
