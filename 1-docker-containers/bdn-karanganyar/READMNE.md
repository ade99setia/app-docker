# 📄 Dokumentasi Deploy Laravel 12 BDN Karanganyar (Docker Offline)

Panduan ini digunakan untuk memindahkan aplikasi Laravel 12 dari lingkungan **Local (Windows/Laragon)** ke server secara offline, dengan tetap mempertahankan modifikasi manual di folder `vendor`.

---

## 1️⃣ Persiapan di Laptop (Online/Local)

Sebelum melakukan build, pastikan aset frontend sudah di-compile di laptop Windows kamu.

~~~powershell
# 1. Masuk ke direktori project
cd D:\3-ProjectWebsite\laragon\www\bdn-karanganyar

# 2. Compile Assets Frontend (Vite/Tailwind)
npm run build

# 3. Build Image Aplikasi (Membawa vendor & node_modules lokal)
docker build -t ghcr.io/ade99setia/bdn_karanganyar_app:latest .

# 4. Simpan (Save) semua Image menjadi file .tar
docker save -o bdn_karanganyar_app.tar ghcr.io/ade99setia/bdn_karanganyar_app:latest
docker save -o nginx_alpine.tar nginx:alpine
docker save -o mysql_8.0.tar mysql:8.0
~~~

---

## 2️⃣ Backup Database & Volume (Laptop Local)

Karena folder `storage` biasanya berisi file dinamis (seperti foto upload), kita akan mem-backup-nya secara terpisah.

### 2a. Jalankan Container & Backup Database
~~~powershell
# Jalankan service untuk export DB
docker-compose up -d

# Backup Database (SQL Dump)
docker exec bdn_karanganyar_db mysqldump -u root -proot bdn_karanganyar_db > backup_bdn_karanganyar.sql
~~~

### 2b. Export Volume Storage (Aset Dinamis)
Langkah ini membungkus folder `storage/app/public` agar data yang sudah ada di lokal ikut terbawa.

~~~powershell
# Export Volume Storage ke .tar.gz
docker run --rm -v bdn-karanganyar_storage_app:/from -v ${PWD}:/to alpine sh -c "cd /from && tar czf /to/storage_app.tar.gz ."
~~~

---

## 3️⃣ Daftar File yang Harus Dibawa ke Server

Pastikan flashdisk atau folder pindahan Anda berisi 8 file utama:
1. `docker-compose.yml`
2. `default.conf` (Konfigurasi Nginx)
3. `.env` (Pastikan DB_HOST=db_bdn_karanganyar)
4. `bdn_karanganyar_app.tar`
5. `nginx_alpine.tar`
6. `mysql_8.0.tar`
7. `storage_app.tar.gz`
8. `backup_bdn.sql`

---

## 4️⃣ Eksekusi di Server Offline

Pindahkan semua file ke server, lalu jalankan perintah berikut:

### 4a. Load Images & Up
~~~bash
# 1. Load semua image ke sistem Docker server
docker load -i bdn_karanganyar_app.tar
docker load -i nginx_alpine.tar
docker load -i mysql_8.0.tar

# 2. Jalankan Container
docker-compose up -d
~~~

### 4b. Restore Volume & Fix Permissions
Langkah ini sangat penting untuk Laravel agar folder `storage` dan `bootstrap/cache` bisa ditulisi oleh sistem.

~~~bash
# 1. Restore data storage (Foto/Uploads)
docker run --rm -v bdn-karanganyar_storage_app:/to -v $(pwd):/from alpine sh -c "cd /to && tar xzf /from/storage_app.tar.gz"

# 2. WAJIB: Fix Permissions untuk user www-data
docker exec -u root bdn_karanganyar_app chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache
docker exec -u root bdn_karanganyar_app chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache
~~~

### 4c. Import Database
~~~bash
cat backup_bdn_karanganyar.sql | docker exec -i bdn_karanganyar_db mysql -u root -proot bdn_karanganyar_db
~~~

---

## 5️⃣ Pengujian Akhir (Maintenance)

Jika aplikasi baru pertama kali naik, jalankan optimasi Laravel di dalam container:

| Tujuan | Perintah |
| :--- | :--- |
| Bersihkan Cache Config | `docker exec bdn_karanganyar_app php artisan config:clear` |
| Link Storage | `docker exec bdn_karanganyar_app php artisan storage:link` |
| Cek Log Laravel | `docker exec bdn_karanganyar_app tail -f storage/logs/laravel.log` |
| Cek Status Docker | `docker-compose ps` |

**Akses Aplikasi:** Buka browser di `http://[IP-SERVER]:8081`

---