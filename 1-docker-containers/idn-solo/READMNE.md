# 📄 Dokumentasi Deploy Laravel 12 IDN Solo (Docker Offline)

Panduan ini digunakan untuk memindahkan aplikasi Laravel 12 dari lingkungan **Local (Windows/Laragon)** ke server secara offline, dengan tetap mempertahankan modifikasi manual di folder `vendor`.

---

## 1️⃣ Persiapan di Laptop (Online/Local)

Sebelum melakukan build, pastikan aset frontend sudah di-compile di laptop Windows kamu.

~~~powershell
# 1. Masuk ke direktori project
cd D:\3-ProjectWebsite\laragon\www\idn-solo

# 2. Build Image Aplikasi (Membawa vendor & node_modules lokal)
docker build -t ghcr.io/ade99setia/idn_solo_app:latest .

# 3. Simpan (Save) semua Image menjadi file .tar
docker save -o idn_solo_app.tar ghcr.io/ade99setia/idn_solo_app:latest
docker save -o nginx_alpine.tar nginx:alpine
docker save -o mysql_8.0.tar mysql:8.0
~~~

---

## 2️⃣ Backup Database & Volume (Laptop Local)

Karena folder `storage` biasanya berisi file dinamis (seperti foto upload), kita akan mem-backup-nya secara terpisah.

### 2a. Jalankan Container & Backup Database
~~~powershell
# Jalankan service untuk export DB
docker compose up -d

# Backup Database (SQL Dump)
docker exec idn_solo_db mysqldump -u root -proot idn_solo > backup_idn_solo.sql
~~~

Backup Data SQL di Local Windows
~~~powershell
docker exec idn_solo_db `
  sh -c 'exec mysqldump --single-transaction --quick -u root -proot idn_solo' `
  > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql
~~~

### 2b. Import Data (Injection)
*PENTING: Ganti `idn-solo` dengan nama folder project Anda jika berbeda.*

~~~powershell
# 0. Jalankan bila belum
docker compose up -d

# 1. Compile Assets Frontend (Vite/Tailwind)
npm run build

# 2. Import and Rebuild folder 'public' dari Windows ke volume Docker
docker run --rm -v ${PWD}/public:/from -v idn-solo_public_app:/to alpine sh -c "rm -rf /to/* && cp -av /from/. /to/"

# 3. Import folder 'storage' dari Windows ke volume Docker
docker run --rm -v ${PWD}/storage:/from -v idn-solo_storage_app:/to alpine sh -c "apk add --no-cache rsync && rsync -av --exclude='framework/cache/*' --exclude='framework/sessions/*' --exclude='framework/views/*.php' --exclude='logs/*.log' /from/ /to/"
~~~


### 2c. Export Volume (Aset Dinamis)
Langkah ini membungkus folder `storage/app/public` agar data yang sudah ada di lokal ikut terbawa.

~~~powershell
# Export Volume Public ke .tar.gz
docker run --rm -v idn-solo_public_app:/from -v ${PWD}:/to alpine sh -c "cd /from && tar czf /to/public_app.tar.gz ."

# Export Volume Storage ke .tar.gz
docker run --rm -v idn-solo_storage_app:/from -v ${PWD}:/to alpine sh -c "cd /from && tar czf /to/storage_app.tar.gz ."
~~~

---

## 3️⃣ Daftar File yang Harus Dibawa ke Server


Pastikan flashdisk atau folder pindahan Anda berisi 8 file utama:
1. `docker-compose.yml`
2. `default.conf` (Konfigurasi Nginx)
3. `.env` (Pastikan DB_HOST=db_idn_solo)
4. `idn_solo_app.tar`
5. `nginx_alpine.tar` ❌
6. `mysql_8.0.tar` ❌
7. `public_app.tar.gz`
8. `storage_app.tar.gz`
9. `backup_idn_solo.sql`

---

## 4️⃣ Eksekusi di Server Offline

Pindahkan semua file ke server, lalu jalankan perintah berikut:

### 4a. Load Images & Up
~~~bash
# 1. Load semua image ke sistem Docker server

# Opsional
docker load -i nginx_alpine.tar
docker load -i mysql_8.0.tar

# Load image
docker load -i idn_solo_app.tar
docker image prune -f

# 2. Jalankan Container
docker compose up -d
~~~

### 4b. Restore Volume & Fix Permissions
Langkah ini sangat penting untuk Laravel agar folder `storage` dan `bootstrap/cache` bisa ditulisi oleh sistem.

~~~bash
# 1. Restore data public (Assets Public)
docker run --rm -v idn-solo_public_app:/to -v $(pwd):/from alpine sh -c "rm -rf /to/* && cd /to && tar xzf /from/public_app.tar.gz"

# 2. Restore data storage (Uploads)
docker run --rm -v idn-solo_storage_app:/to -v $(pwd):/from alpine sh -c "cd /to && tar xzf /from/storage_app.tar.gz"

# 3. SEPERTINYA TIDAK PERLU: Fix Permissions untuk user www-data
docker exec -u root idn_solo_app chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache /var/www/html/public
docker exec -u root idn_solo_app chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache /var/www/html/public
~~~

### 4c. Import Database
Sesuaikan nama file backup database:
~~~bash
cat backup_idn_solo.sql | docker exec -i idn_solo_db mysql -u root -proot idn_solo
~~~

---

## 5️⃣ Pengujian Akhir (Maintenance)

Jika aplikasi baru pertama kali naik, jalankan optimasi Laravel di dalam container:

| Tujuan | Perintah |
| :--- | :--- |
| Bersihkan Cache Config | `docker exec idn_solo_app php artisan config:clear` |
| Link Storage | `docker exec idn_solo_app php artisan storage:link` |
| Cek Log Laravel | `docker exec idn_solo_app tail -f storage/logs/laravel.log` |
| Cek Status Docker | `docker compose ps` |

**Akses Aplikasi:** Buka browser di `http://[IP-SERVER]:8084`

---