# 📄 Dokumentasi Deploy Laravel 12 BDN Karanganyar (Docker Offline)

Panduan ini digunakan untuk memindahkan aplikasi Laravel 12 dari lingkungan **Local (Windows/Laragon)** ke server secara offline, dengan tetap mempertahankan modifikasi manual di folder `vendor`.

---

## 1️⃣ Persiapan di Laptop (Online/Local)

Sebelum melakukan build, pastikan aset frontend sudah di-compile di laptop Windows kamu.

~~~powershell
# 1. Masuk ke direktori project
cd D:\3-ProjectWebsite\laragon\www\bdn-karanganyar

# 2. Build Image Aplikasi (Membawa vendor & node_modules lokal)
docker build -t ghcr.io/ade99setia/bdn_karanganyar_app:latest .

# 3. Simpan (Save) semua Image menjadi file .tar
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
docker compose up -d

# Backup Database (SQL Dump)
docker exec bdn_karanganyar_db mysqldump -u root -proot bdn_karanganyar > backup_bdn_karanganyar.sql
~~~

Backup Data SQL di Local Windows
~~~powershell
docker exec bdn_karanganyar_db `
  sh -c 'exec mysqldump --single-transaction --quick -u root -proot bdn_karanganyar' `
  > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql
~~~

### 2b. Import Data (Injection)
*PENTING: Ganti `bdn-karanganyar` dengan nama folder project Anda jika berbeda.*

~~~powershell
# 2. Compile Assets Frontend (Vite/Tailwind)
npm run build

# 3. Import and Rebuild folder 'public' dari Windows ke volume Docker
docker run --rm -v ${PWD}/public:/from -v bdn-karanganyar_public_app:/to alpine sh -c "rm -rf /to/* && cp -av /from/. /to/"

# 4. Import folder 'storage' dari Windows ke volume Docker
docker run --rm -v ${PWD}/storage:/from -v bdn-karanganyar_storage_app:/to alpine sh -c "apk add --no-cache rsync && rsync -av --exclude='framework/cache/*' --exclude='framework/sessions/*' --exclude='framework/views/*.php' --exclude='logs/*.log' /from/ /to/"
~~~


### 2c. Export Volume (Aset Dinamis)
Langkah ini membungkus folder `storage/app/public` agar data yang sudah ada di lokal ikut terbawa.

~~~powershell
# Export Volume Public ke .tar.gz
docker run --rm -v bdn-karanganyar_public_app:/from -v ${PWD}:/to alpine sh -c "cd /from && tar czf /to/public_app.tar.gz ."

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
5. `nginx_alpine.tar` ❌
6. `mysql_8.0.tar` ❌
7. `public_app.tar.gz`
8. `storage_app.tar.gz`
9. `backup_bdn_karanganyar.sql`

---

## 4️⃣ Eksekusi di Server Offline

Pindahkan semua file ke server, lalu jalankan perintah berikut:

### 4a. Load Images & Up
~~~bash
# 1. Load semua image ke sistem Docker server

# Opsional
docker load -i nginx_alpine.tar
docker load -i mysql_8.0.tar

# Load Images
docker load -i bdn_karanganyar_app.tar
docker image prune -f

# 2. Jalankan Container
docker compose up -d
~~~

### 4b. Restore Volume & Fix Permissions
Langkah ini sangat penting untuk Laravel agar folder `storage` dan `bootstrap/cache` bisa ditulisi oleh sistem.

~~~bash
# 1. Restore data public (Assets Public)
docker run --rm -v bdn-karanganyar_public_app:/to -v $(pwd):/from alpine sh -c "rm -rf /to/* && cd /to && tar xzf /from/public_app.tar.gz"

# 2. Restore data storage (Uploads)
docker run --rm -v bdn-karanganyar_storage_app:/to -v $(pwd):/from alpine sh -c "cd /to && tar xzf /from/storage_app.tar.gz"

# 3. SEPERTINYA TIDAK PERLU: Fix Permissions untuk user www-data
docker exec -u root bdn_karanganyar_app chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache /var/www/html/public
docker exec -u root bdn_karanganyar_app chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache /var/www/html/public
~~~

### 4c. Import Database
Sesuaikan nama file backup database:
~~~bash
cat backup_bdn_karanganyar.sql | docker exec -i bdn_karanganyar_db mysql -u root -proot bdn_karanganyar
~~~

---

## 5️⃣ Pengujian Akhir (Maintenance)

Jika aplikasi baru pertama kali naik, jalankan optimasi Laravel di dalam container:

| Tujuan | Perintah |
| :--- | :--- |
| Bersihkan Cache Config | `docker exec bdn_karanganyar_app php artisan config:clear` |
| Link Storage | `docker exec bdn_karanganyar_app php artisan storage:link` |
| Cek Log Laravel | `docker exec bdn_karanganyar_app tail -f storage/logs/laravel.log` |
| Cek Status Docker | `docker compose ps` |

**Akses Aplikasi:** Buka browser di `http://[IP-SERVER]:8081`

---