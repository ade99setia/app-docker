# 📄 Dokumentasi Deploy HTML CSS Javascript (Docker Offline)

Panduan ini digunakan untuk memindahkan aplikasi dari lingkungan **Local (Windows/Laragon)** ke server **Produksi** secara offline menggunakan Docker.

---

## 1️⃣ Build & Save Docker Images (Laptop Online)

Langkah ini dilakukan di laptop yang memiliki koneksi internet untuk menarik base image dari Docker Hub dan menyimpannya menjadi file fisik.

~~~powershell
# 1. Masuk ke direktori project
cd D:\3-ProjectWebsite\laragon\www\undangan-pernikahan\portofolio

# 2. Build Image Aplikasi (HTML CSS Javascript + Source Code)
docker build -t ghcr.io/ade99setia/portofolio:latest .

# 3. Simpan (Save) semua Image menjadi file .tar
docker save -o portofolio.tar ghcr.io/ade99setia/portofolio:latest
docker save -o nginx_alpine.tar nginx:alpine
~~~

---

## 2️⃣ Daftar File yang Harus Dibawa ke Server

Pastikan folder "pindahan" Anda berisi file-file berikut:
1. `docker-compose.yml`
2. `default.conf` (Konfigurasi Nginx)
3. `portofolio.tar`
4. `nginx_alpine.tar`

---

## 3️⃣ Eksekusi di Server Offline

Pindahkan semua file di atas ke satu folder di server, lalu jalankan perintah berikut:

### 4️⃣ Load Images & Up

~~~bash
# 1. Load semua image ke sistem Docker server
docker load -i portofolio.tar
docker image prune -f

# opsional
docker load -i nginx_alpine.tar

# 2. Jalankan Container
docker compose up -d
~~~

---

## 5️⃣ Pengujian Akhir

| Cek Lis | Perintah |
| :--- | :--- |
| Cek Status Container | `docker compose ps` |
| Cek Log Error | `docker logs -f portofolio` |

**Akses Aplikasi:** Buka browser di `http://[IP-SERVER]:8083`