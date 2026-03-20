# Dokumentasi Deploy Laravel Docker Offline

## 1️⃣ File yang Diperlukan

### 1a. Di PC Lokal (Internet tersedia)

Pastikan kamu sudah memiliki image Docker yang dibutuhkan:

- `ghcr.io/ade99setia/bdn_karanganyar_app:latest`
- `nginx:alpine`
- `mysql:8.0`

Simpan image ke file `.tar` dengan perintah:

```sh
# Laravel App
docker save -o bdn_karanganyar_app.tar ghcr.io/ade99setia/bdn_karanganyar_app:latest

# Nginx
docker save -o nginx_alpine.tar nginx:alpine

# MySQL
docker save -o mysql_8.0.tar mysql:8.0
```

File `.tar` ini nantinya dibawa ke server offline.

### 1b. File yang harus dibawa ke server offline

Simpan semua file berikut di satu folder, misal `D:\docker-offline-deploy`:

```
docker-compose.yml
default.conf
.env
bdn_karanganyar_app.tar
nginx_alpine.tar
mysql_8.0.tar
optional: backup.sql
```

**Keterangan:**
- `.env` → Environment variables Laravel
- `docker-compose.yml` → Konfigurasi container app, web (Nginx), db
- `default.conf` → Konfigurasi Nginx
- `.tar` → Docker images dari PC lokal
- `backup.sql` → File dump database MySQL (opsional)

---
## 2️⃣ Load Docker Images ke Server

Buka PowerShell / Terminal di folder yang sama dengan `.tar`:

```sh
# Laravel App
docker load -i bdn_karanganyar_app.tar

# Nginx
docker load -i nginx_alpine.tar

# MySQL
docker load -i mysql_8.0.tar
```

Cek image berhasil load:

```sh
docker images
```

Harus muncul:
- `bdn_karanganyar_app:latest`
- `nginx:alpine`
- `mysql:8.0`

> ⚠️ Pastikan kamu berada di folder yang sama dengan `.tar`, kalau tidak, Docker tidak akan menemukan file.

---
## 3️⃣ Jalankan Docker Compose

Pastikan berada di folder yang sama dengan `docker-compose.yml`:

```sh
docker-compose up -d
```

- `-d` → Jalankan container di background

Container dibuat:
- **bdn_karanganyar_app** → PHP-FPM Laravel
- **bdn_karanganyar_web** → Nginx
- **bdn_karanganyar_db** → MySQL

Cek status container:

```sh
docker-compose ps
```

---
## 4️⃣ Cek Folder Public di Nginx

Pastikan Nginx dapat membaca folder Laravel public + build:

```sh
docker exec -it bdn_karanganyar_web ls -la /var/www/html/public
```

Harus ada: `index.php`, folder `build`, `assets`

Jika ada permission issue: pastikan folder/public readable oleh Nginx user (nginx di Alpine)

---
## 5️⃣ Migrasi Database Laravel

Jalankan migrate di container app:

```sh
# Masuk container app
docker exec -it bdn_karanganyar_app sh

# Jalankan migrate Laravel
php artisan migrate --force
```

**Keterangan:**
- `--force` wajib di production/offline supaya migrate berjalan tanpa prompt
- Path kerja: `/var/www/html` di container app

---
## 6️⃣ Import Database dari File SQL (Opsional)

Jika ada file dump `backup.sql`:

```sh
# Copy file sql ke container db
docker cp backup.sql bdn_karanganyar_db:/backup.sql

# Masuk container db
docker exec -it bdn_karanganyar_db sh

# Import SQL
mysql -u bdn_user -pstrongpassword123 bdn_karanganyar_db < /backup.sql
```

- Ganti `strongpassword123` sesuai `.env`
- Database harus sudah dibuat (`MYSQL_DATABASE=bdn_karanganyar_db`)

---
## 7️⃣ Akses Aplikasi

Buka browser di server PC atau jaringan lokal:

```
http://localhost:8081
```

Laravel harus berjalan → Nginx membaca `index.php` dan JS/CSS di `/build/assets/` → tidak ada 403/404

---
## 8️⃣ Command Penting Lainnya

| Tujuan              | Path / Container      | Command                                                      |
|---------------------|----------------------|--------------------------------------------------------------|
| Cek status container| Folder docker-compose | docker-compose ps                                           |
| Masuk container app | Container app        | docker exec -it bdn_karanganyar_app sh                      |
| Jalankan migrate    | Dalam container app  | php artisan migrate --force                                  |
| Masuk container db  | Container db         | docker exec -it bdn_karanganyar_db sh                        |
| Import SQL          | Dalam container db   | mysql -u bdn_user -pMYSQL_PASSWORD bdn_karanganyar_db < /backup.sql |
| Stop container      | Folder docker-compose | docker-compose down                                         |
| Recreate container  | Folder docker-compose | docker-compose up --build -d                                |
| Hapus volume DB     | Folder docker-compose | docker-compose down -v                                      |

---
## 9️⃣ Catatan Penting

- `.env` harus selalu ada di folder yang sama dengan `docker-compose.yml`

Untuk update image baru:

1. Copy file `.tar` baru
2. Jalankan:

```sh
docker load -i new_image.tar

docker-compose up -d --force-recreate
```

- Semua assets sudah build di image → tidak perlu npm / composer / internet

---
Dokumentasi ini lengkap untuk deploy Laravel Docker offline di server, termasuk migrate database dan import SQL.