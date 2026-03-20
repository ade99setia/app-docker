## Dokumentasi Deploy CI4 Docker Offline (Undangan Pernikahan)

---

### 1️⃣ File yang Diperlukan

#### 1a. Di PC Lokal (Internet tersedia)
Pastikan kamu sudah melakukan docker build dan memiliki image Docker berikut di laptop/PC lokal:
- `ghcr.io/ade99setia/undangan_pernikahan_app:latest`
- `nginx:alpine`
- `mysql:8.0`

Simpan image ke file `.tar` dengan perintah berikut:

```sh
# App CI4 (Pastikan sudah di-build versi terbarunya)
docker save -o undangan_pernikahan_app.tar ghcr.io/ade99setia/undangan_pernikahan_app:latest

# Nginx
docker save -o nginx_alpine.tar nginx:alpine

# MySQL
docker save -o mysql_8.0.tar mysql:8.0
```

Ketiga file `.tar` ini nantinya dibawa ke server offline/production.

#### 1b. File yang harus dibawa ke server offline
Simpan semua file berikut di satu folder di server, misal `/home/user/undangan-deploy`:

```
docker-compose.yml
default.conf
.env
undangan_pernikahan_app.tar
nginx_alpine.tar
mysql_8.0.tar
optional: backup_undangan.sql
```

**Keterangan:**
- `.env` → Konfigurasi environment CI4 (Pastikan `database.default.hostname = db`)
- `docker-compose.yml` → Konfigurasi container app, web (Nginx), db
- `default.conf` → Konfigurasi rute Nginx ke folder public
- `.tar` → Docker images (berisi sistem, kode aplikasi, dan assets)
- `backup_undangan.sql` → File dump/export database MySQL dari PC lokal (opsional)

---

### 2️⃣ Load Docker Images ke Server

Buka terminal/SSH di server dan masuk ke folder tempat file `.tar` berada:

```sh
# Load App CI4
docker load -i undangan_pernikahan_app.tar

# Load Nginx
docker load -i nginx_alpine.tar

# Load MySQL
docker load -i mysql_8.0.tar
```

Cek apakah image berhasil masuk ke Docker server:

```sh
docker images
```

Harus muncul daftar image:
- `ghcr.io/ade99setia/undangan_pernikahan_app`
- `nginx`
- `mysql`

> ⚠️ Jika gagal, pastikan kamu menjalankan perintah di folder yang sama dengan file `.tar`.

---

### 3️⃣ Jalankan Docker Compose

Pastikan kamu berada di folder yang sama dengan `docker-compose.yml` dan `.env`:

```sh
docker-compose up -d
```

- `-d` → Menjalankan container di background

Container yang akan dibuat:
- **undangan_pernikahan_app** → PHP-FPM & CodeIgniter 4
- **undangan_pernikahan_web** → Nginx Web Server
- **undangan_pernikahan_db** → MySQL Database

Cek status container:

```sh
docker-compose ps
```

---

### 4️⃣ Cek Jembatan Folder Public di Nginx

Pastikan Nginx berhasil membaca folder public dan assets dari dalam image aplikasi:

```sh
docker exec -it undangan_pernikahan_web ls -la /var/www/html/public
```

Harus muncul file `index.php` dan folder `assets` (beserta isinya). Jika muncul, berarti jembatan volume `public_app` bekerja sempurna.

---

### 5️⃣ Migrasi Database CodeIgniter 4 (Opsional)

Jika kamu membuat tabel baru menggunakan sistem migrasi bawaan CI4, jalankan perintah ini di dalam container app:

```sh
# Jalankan migrate CI4 tanpa perlu masuk bash dulu
docker exec -it undangan_pernikahan_app php spark migrate
```

Path kerja di dalam container otomatis berada di `/var/www/html`.

---

### 6️⃣ Import Database dari File SQL (Penting!)

Jika kamu punya file dump `backup_undangan.sql` dari laptop lokal (berisi data tamu, dll), lakukan import ke server:

```sh
# 1. Copy file sql ke dalam container db
docker cp backup_undangan.sql undangan_pernikahan_db:/backup.sql

# 2. Masuk ke dalam container db
docker exec -it undangan_pernikahan_db bash

# 3. Import SQL ke dalam database
mysql -u ci4_user -psecret undangan_pernikahan < /backup.sql

# 4. Keluar dari container db
exit
```

**Credential Database:**
- User: `ci4_user`
- Password: `secret`
- Database: `undangan_pernikahan`

---

### 7️⃣ Akses Aplikasi

Buka browser dan akses IP Server atau Localhost dengan port 8082:

```
http://localhost:8082
```

(Atau ganti `localhost` dengan IP Public Server jika sudah di VPS).

Website undangan harus tampil sempurna lengkap dengan gambar dan tidak muncul halaman error "Whoops!".

---

### 8️⃣ Command Penting Lainnya

| Tujuan                  | Command / Eksekusi                                      |
|------------------------|--------------------------------------------------------|
| Cek status container   | docker-compose ps                                       |
| Cek log error CI4/PHP  | docker logs undangan_pernikahan_app                     |
| Cek log error Nginx    | docker logs undangan_pernikahan_web                     |
| Masuk ke container App | docker exec -it undangan_pernikahan_app bash            |
| Jalankan Migrate CI4   | docker exec -it undangan_pernikahan_app php spark migrate|
| Stop semua container   | docker-compose down                                     |
| Recreate container     | docker-compose up -d --force-recreate                   |
| Hapus Database         | docker-compose down -v                                  |

> ⚠️ `docker-compose down -v` menghapus volume database dan foto upload user (hati-hati!)

---

### 9️⃣ Catatan Pemeliharaan & Update

Karena aplikasi ini menggunakan mode Immutable Image (Nasi Bungkus):

- **JANGAN** mengedit kode PHP atau menaruh file assets secara manual langsung di server. File akan hilang saat container di-restart.
- Folder yang aman dan permanen (karena menggunakan volume terpisah) hanyalah `writable/uploads` dan `private`.

#### Cara Update Aplikasi / Ganti Gambar Baru

1. Lakukan perubahan kode/gambar di PC Lokal.
2. Build ulang image:

    ```sh
    docker build -t ghcr.io/ade99setia/undangan_pernikahan_app:latest .
    ```
3. Export ke `.tar` baru.
4. Bawa `.tar` ke server, load imagenya:

    ```sh
    docker load -i undangan_pernikahan_app.tar
    ```
5. Restart container agar menggunakan versi terbaru:

    ```sh
    docker-compose up -d --force-recreate
    ```

---