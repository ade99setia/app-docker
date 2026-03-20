# 🗺️ Peta Infrastruktur Server & Docker

Dokumentasi ini berisi daftar seluruh layanan, container, port, dan volume yang berjalan di server ini untuk mencegah terjadinya tabrakan port atau nama container di masa depan.

---

## 📌 1. Tabel Alokasi Port Utama (Host / Server)

Gunakan tabel ini sebagai acuan utama sebelum mengekspos port ke luar (menambahkan project baru) agar port tidak bentrok.

| Port Host | Digunakan Oleh      | Project / Aplikasi         | Keterangan                                |
|-----------|---------------------|----------------------------|-------------------------------------------|
| **8081** | Nginx Web Server    | bdn_karanganyar (Laravel)  | Akses Web UI Project 1                    |
| **8082** | Nginx Web Server    | undangan_pernikahan (CI4)  | Akses Web UI Project 2                    |
| **3306** | MySQL Database      | bdn_karanganyar (Laravel)  | Akses Remote DB Project 1 (Bawaan Server) |
| **3307** | MySQL Database      | undangan_pernikahan (CI4)  | Akses Remote DB Project 2                 |
| *(Kosong)*| --                  | --                         | Gunakan **8083** untuk Web App selanjutnya|
| *(Kosong)*| --                  | --                         | Gunakan **3308** untuk DB selanjutnya     |

> 💡 **Catatan Penting:** Port internal di dalam Docker (seperti port `80` untuk Nginx, `9000` untuk PHP, dan `3306` untuk MySQL) boleh sama antar project karena mereka diisolasi oleh Docker Network. Yang **TIDAK BOLEH SAMA** adalah "Port Host" (angka sebelah kiri pada konfigurasi `ports: - "HOST:CONTAINER"`).

---

## 📦 2. Detail Project 1: Sistem BDN Karanganyar (Laravel)

- **Framework:** Laravel
- **Status Image:** Immutable (Build dari PC lokal)
- **Lokasi Folder:** `~/app-docker/bdn_karanganyar` (Sesuaikan jika berbeda)

### Daftar Container & Image

| Nama Container        | Image Docker                               | Fungsi                | Port Internal | Port Eksternal |
|-----------------------|--------------------------------------------|-----------------------|---------------|----------------|
| `bdn_karanganyar_app` | `ghcr.io/.../bdn_karanganyar_app:latest`   | PHP-FPM & Laravel     | `9000`        | Tertutup       |
| `bdn_karanganyar_web` | `nginx:alpine`                             | Web Server (Jembatan) | `80`          | **`8081`** |
| `bdn_karanganyar_db`  | `mysql:8.0`                                | Database MySQL        | `3306`        | **`3306`** |

### Daftar Volumes (Data Persisten)
- `public_app` : Jembatan folder public dari App ke Nginx
- `db_data` : Menyimpan data asli database MySQL

---

## 💍 3. Detail Project 2: Undangan Pernikahan (CodeIgniter 4)

- **Framework:** CodeIgniter 4
- **Status Image:** Immutable (Build dari PC lokal)
- **Lokasi Folder:** `~/app-docker/undangan-pernikahan`

### Daftar Container & Image

| Nama Container            | Image Docker                                  | Fungsi                | Port Internal | Port Eksternal |
|---------------------------|-----------------------------------------------|-----------------------|---------------|----------------|
| `undangan_pernikahan_app` | `ghcr.io/.../undangan_pernikahan_app:latest`  | PHP-FPM & CI4         | `9000`        | Tertutup       |
| `undangan_pernikahan_web` | `nginx:alpine`                                | Web Server (Jembatan) | `80`          | **`8082`** |
| `undangan_pernikahan_db`  | `mysql:8.0`                                   | Database MySQL        | `3306`        | **`3307`** |

### Daftar Volumes (Data Persisten)
- `public_app` : Jembatan folder public (termasuk assets gambar) dari App ke Nginx
- `uploads_data` : Menyimpan foto/file yang di-upload oleh user/tamu (Aman saat restart)
- `private_data` : Menyimpan file rahasia/sistem CI4
- `db_data` : Menyimpan data asli database MySQL

---

## 🕸️ 4. Isolasi Network (Jaringan)

Masing-masing project berada di jaringannya sendiri dan **tidak saling terhubung**.

- **Network Project 1:** `app_network` (Milik BDN Karanganyar)
- **Network Project 2:** `app_network` (Milik Undangan Pernikahan)
*(Diisolasi otomatis oleh Docker berdasarkan nama folder project).*

Karena beda network:
- Nginx project 1 **tidak bisa** membaca aplikasi project 2.
- Aplikasi CI4 **tidak bisa** diam-diam membaca database Laravel, begitu pula sebaliknya.

---

## 🛠️ 5. SOP Penambahan Project Baru

Jika ada project ke-3 di masa depan, ikuti aturan ini di file `docker-compose.yml` yang baru:

1. **Nama Container:** Wajib diberi prefix nama project (contoh: `project3_app`, `project3_web`, `project3_db`).
2. **Port Web Nginx:** Gunakan port **`8083`** (Format: `"8083:80"`).
3. **Port Database:** Gunakan port **`3308`** (Format: `"3308:3306"`).
4. **Nama Volume:** Gunakan prefix (contoh: `project3_db_data`) agar tidak menimpa volume project lama.

---

## 🔄 6. SOP Update Aplikasi (Deploy Versi Baru)

Jika ada perubahan kode (fitur baru/bug fix), berikut adalah cara memperbarui aplikasi di server agar data database dan file *upload* tetap aman.

### Skenario A: Menggunakan Tag Image `:latest`
Gunakan cara ini jika mem-build image baru dengan nama dan tag yang sama persis dengan yang ada di server.

1. **Upload & Load Image Baru:**
    ```bash
    docker load -i undangan_pernikahan_app.tar
    ```
2. **Paksa Docker Membuat Ulang Container:**
    *(Masuk ke folder project, lalu jalankan)*
    ```bash
    docker-compose up -d --force-recreate
    ```

### Skenario B: Menggunakan Tag Versi Spesifik (Best Practice)
Gunakan cara ini jika mem-build image dengan tag spesifik (misal: `:v1.1`, `:v2.0`). Memudahkan *rollback* jika ada *error*.

1. **Upload & Load Image Baru:**
    ```bash
    docker load -i undangan_pernikahan_app_v1.1.tar
    ```
2. **Edit `docker-compose.yml`:**
    Ubah tag image di bagian `app`:
    ```yaml
    app:
      image: ghcr.io/ade99setia/undangan_pernikahan_app:v1.1
    ```
3. **Terapkan Perubahan:**
    ```bash
    docker-compose up -d
    ```

---

## 🧪 7. SOP Menjalankan 2 Versi Bersamaan (Staging / A-B Testing)

Jika ingin menjalankan versi baru (V2) tanpa mematikan versi lama (V1) yang sedang *live*:

1. **Buat Folder Baru:** Buat folder terpisah (misal: `undangan-pernikahan-v2`).
2. **Copy `docker-compose.yml`:** Salin file compose ke folder baru.
3. **Edit 4 Komponen Wajib** di dalam file compose yang baru:
    - **Tag Image:** Ubah ke versi baru (misal `:v2.0`).
    - **Nama Container:** Tambahkan akhiran `_v2` (contoh: `undangan_pernikahan_app_v2`) agar tidak bentrok.
    - **Port Host:** Gunakan port yang masih kosong (contoh Web: `"8084:80"`, DB: `"3309:3306"`).
    - **Nama Volume:** Tambahkan akhiran `_v2` (contoh: `public_app_v2`, `db_data_v2`) agar data tidak menimpa versi lama.
4. **Jalankan di Folder Baru:**
    ```bash
    docker-compose up -d
    ```
Hasilnya: V1 tetap jalan di port `8082`, dan V2 jalan beriringan di port `8084`.

---

### 🧹 Maintenance Rutin: Membersihkan Image Lama
Agar *storage* server tidak penuh oleh image lama yang menumpuk setelah update, jalankan perintah ini berkala:
```bash
docker image prune -a
```

(Perintah ini hanya akan menghapus image yang sedang tidak dipakai oleh container yang aktif).
