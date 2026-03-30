# 📄 Dokumentasi Deploy CI4 Undangan Pernikahan (Docker Offline)

Panduan ini digunakan untuk memindahkan aplikasi dari lingkungan **Local (Windows/Laragon)** ke server **Produksi** secara offline menggunakan Docker.

---

## 1️⃣ Build & Save Docker Images (Laptop Online)

Langkah ini dilakukan di laptop yang memiliki koneksi internet untuk menarik base image dari Docker Hub dan menyimpannya menjadi file fisik.

~~~powershell
# 1. Masuk ke direktori project
cd D:\3-ProjectWebsite\laragon\www\undangan-pernikahan

# 2. Build Image Aplikasi (PHP-FPM + Source Code)
docker build -t ghcr.io/ade99setia/undangan_pernikahan_app:latest .

# 3. Simpan (Save) semua Image menjadi file .tar
docker save -o undangan_pernikahan_app.tar ghcr.io/ade99setia/undangan_pernikahan_app:latest
docker save -o nginx_alpine.tar nginx:alpine
docker save -o mysql_8.0.tar mysql:8.0
~~~

---

## 2️⃣ Persiapan Data & Backup Volumes (Laptop Online)

Langkah ini bertujuan memasukkan aset lokal (musik, foto, dll) ke dalam volume Docker agar data tersebut ikut terbawa saat di-backup.

### 2a. Jalankan Container & Import Data (Injection)
*PENTING: Ganti `undangan-pernikahan` dengan nama folder project Anda jika berbeda.*

~~~powershell
# 1. Jalankan semua service sementara agar volume terbentuk
docker compose up -d

# 2. Import folder 'public' dari Windows ke volume Docker
docker run --rm -v ${PWD}/public:/from -v undangan-pernikahan_public_app:/to alpine sh -c "cp -av /from/. /to/"

# 3. Import folder 'private' (Music/Images) dari Windows ke volume Docker
docker run --rm -v ${PWD}/private:/from -v undangan-pernikahan_data_private:/to alpine sh -c "cp -av /from/. /to/"

# 4. Import folder 'writable' dari Windows ke volume Docker
docker run --rm -v ${PWD}/writable:/from -v undangan-pernikahan_data_writable:/to alpine sh -c "cp -av /from/. /to/"

# 5. FIX PERMISSION: Agar PHP-FPM bisa membaca file yang baru diImport
docker exec -u root undangan_pernikahan_app chown -R www-data:www-data /var/www/html/private /var/www/html/writable
~~~

### 2b. Export Volume & Database ke File

~~~powershell
# 1. Export Volume Public ke .tar.gz
docker run --rm -v undangan-pernikahan_public_app:/from -v ${PWD}:/to alpine sh -c "cd /from && tar czf /to/public_app.tar.gz ."

# 2. Export Volume Private ke .tar.gz
docker run --rm -v undangan-pernikahan_data_private:/from -v ${PWD}:/to alpine sh -c "cd /from && tar czf /to/private.tar.gz ."

# 3. Export Volume Uploads ke .tar.gz
docker run --rm -v undangan-pernikahan_data_writable:/from -v ${PWD}:/to alpine sh -c "cd /from && tar czf /to/uploads.tar.gz ."

# 4. Backup Database (SQL Dump) dari container DB
docker exec undangan_pernikahan_db mysqldump -u root -proot undangan_pernikahan > backup_undangan_pernikahan.sql
~~~

Backup Data SQL di Local Windows
~~~bash
docker exec bdn_karanganyar_db `
  sh -c 'exec mysqldump --single-transaction --quick -u root -proot bdn_karanganyar' `
  > backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql
~~~

---

## 3️⃣ Daftar File yang Harus Dibawa ke Server

Pastikan folder "pindahan" Anda berisi file-file berikut:
1. `docker-compose.yml`
2. `default.conf` (Konfigurasi Nginx)
3. `.env` (Pastikan DB_HOST mengarah ke `db_undangan_pernikahan`)
4. `undangan_pernikahan_app.tar`
5. `nginx_alpine.tar`
6. `mysql_8.0.tar`
7. `private.tar.gz`
8. `uploads.tar.gz`
9. `backup_undangan_pernikahan.sql`

---

## 4️⃣ Eksekusi di Server Offline

Pindahkan semua file di atas ke satu folder di server, lalu jalankan perintah berikut:

### 4a. Load Images & Up

~~~bash
# 1. Load semua image ke sistem Docker server
docker load -i undangan_pernikahan_app.tar
docker image prune -f

# opsional
docker load -i nginx_alpine.tar
docker load -i mysql_8.0.tar

# 2. Jalankan Container
docker compose up -d
~~~

### 4b. Restore Volume Data (Aset Musik & Gambar)

~~~bash
# 1. Restore Public
docker run --rm -v undangan-pernikahan_public_app:/to -v $(pwd):/from alpine sh -c "cd /to && tar xzf /from/public_app.tar.gz"

# 2. Restore Private (Musik/Gambar)
docker run --rm -v undangan-pernikahan_data_private:/to -v $(pwd):/from alpine sh -c "cd /to && tar xzf /from/private.tar.gz"

# 3. Restore Uploads
docker run --rm -v undangan-pernikahan_data_writable:/to -v $(pwd):/from alpine sh -c "cd /to && tar xzf /from/uploads.tar.gz"

# 3. WAJIB: Perbaiki izin akses di server agar PHP bisa membaca file
docker exec -u root undangan_pernikahan_app chown -R www-data:www-data /var/www/html/private /var/www/html/writable
~~~

### 4c. Import Database

### 4c. Backup & Import Database
Sesuaikan nama file backup database:
~~~bash
cat backup_undangan_pernikahan.sql | docker exec -i undangan_pernikahan_db mysql -u root -proot undangan_pernikahan
~~~

---

## 5️⃣ Pengujian Akhir

| Cek Lis | Perintah |
| :--- | :--- |
| Cek Status Container | `docker compose ps` |
| Cek Log Error PHP | `docker logs -f undangan_pernikahan_app` |
| Cek Isi Tabel DB | `docker exec -it undangan_pernikahan_db mysql -u root -proot -e "USE undangan_pernikahan; SHOW TABLES;"` |

**Akses Aplikasi:** Buka browser di `http://[IP-SERVER]:8082`