# UJIAN PRAKTIK DOCKER

## Instruksi Umum
- Kerjakan semua soal secara mandiri.
- Tidak diperbolehkan menggunakan AI atau mencari referensi dari internet.
- https://idnsolo.com/quiz-offline
- Gunakan hanya file dan konfigurasi yang sudah tersedia.
- Dokumentasikan setiap langkah (screenshot / perintah).
- Pastikan semua service berjalan dengan baik sebelum dikumpulkan.

---

## Aturan Penting (WAJIB DIBACA)

Karena semua siswa menggunakan **1 PC yang sama**, perhatikan hal berikut:


### 1. Gunakan Port Masing-Masing
- **Username dan Password untuk IP:8085 dibagikan melalui selembar kertas**
- idnsolo_remote/personal/{username}

### 2. Gunakan Port Masing-Masing
- Setiap siswa memiliki port yang berbeda.
- **WAJIB menggunakan port sesuai pembagian**
- Dilarang menggunakan port milik siswa lain.

---

### 3. Hindari Bentrok Container
Jika terjadi error seperti:
- `port already in use`
- `container name already exists`

Maka lakukan:

- Hentikan container:
  
      docker stop <nama_container>

- Hapus container:
  
      docker rm <nama_container>

---

### 3. Gunakan Nama Container Unik (Jika Diperlukan)
Jika ada konflik, ubah:
- `container_name`
- atau project name di docker-compose

Contoh:
- tambahkan inisial nama kalian

---

### 4. Cek Container yang Berjalan
Gunakan:

    docker ps

Pastikan:
- Container milik kalian berjalan
- Tidak mengganggu container siswa lain

---

### 5. Jika Port Bentrok
Tanda:
- Tidak bisa diakses di browser
- Error saat menjalankan container

Solusi:
- Pastikan port sesuai tabel
- Cek dengan:

      docker ps

- Ubah hanya **port di host**, bukan di dalam container

---

### 6. Dilarang
- Menghapus container milik siswa lain
- Mengubah project siswa lain
- Menggunakan port sembarangan

---

## Soal 1: Akses Project melalui SFTP

### Gunakan:
    "host": "192.168.51.250",
    "protocol": "sftp",
    "port": 22,
    "username": "idnsolo_remote",
    "password": "idnsolo*0903",
    "remotePath": "/home/idnsolo_remote/personal/{username}",

1. Akses PC server internal sekolah menggunakan SFTP.
2. Gunakan informasi login dan lokasi folder yang telah dibagikan.
3. Pastikan kamu dapat:
   - Masuk ke direktori project masing-masing
   - Melihat isi file project
4. Tunjukkan bukti akses (screenshot file/folder project).

---

## Soal 2: Docker Compose (php-nginx-dev-prod)

1. Jalankan:
   - docker-compose.dev.yml
   - docker-compose.prod.yml
2. Catat perbedaan mode **dev** dan **prod**.
3. Ubah docker-compose.dev.yml:
   - Akses aplikasi melalui **port masing-masing**
   - Tidak mengubah port dalam container
4. Tampilkan hasil di browser.

---

## Soal 3: Nginx Static Web (html-nginx-static)

1. Jalankan container Nginx.
2. Akses:
   - index.html
   - style.css
   - script.js
3. Tulis URL masing-masing file.
4. Ubah konfigurasi:
   - /js/* → arahkan ke src/js/
5. Tunjukkan hasilnya.

---

## Soal 4: React App (react-vite-dev)

1. Build image dari Dockerfile.
2. Jalankan container.
3. Akses aplikasi di browser (port masing-masing).
4. Jelaskan:
   - Proses build
   - Menjalankan container
   - Hingga bisa diakses

---

## Soal 5: Analisis Project UJIKOM

1. Jalankan project UJIKOM.
2. Pastikan berjalan di **port masing-masing**.
3. Jelaskan:
   - Fungsi tiap container
   - Port mapping
   - Volume (jika ada)
   - Network (jika ada)
4. Tampilkan:
   - Browser
   - docker ps
5. Jika error:
   - Jelaskan penyebab
   - Cara mengatasi

---

## Pembagian Port

Gunakan port sesuai nama:

| Nama | Port: Soal 1 / Soal 2 / Soal 3 / Soal 4 |
|------|------|
| Alif Satria Mandala Kusuma | 1101 / 1201 / 1301 / 1401 |
| Dzikral Isa Fadli | 1102 / 1202 / 1302 / 1402 |
| Hammam Mubarak | 1103 / 1203 / 1303 / 1403 |
| Iqbal Muhammad Adiatma | 1104 / 1204 / 1304 / 1404 |
| Jose Shabra Shatilla Rajjawani | 1105 / 1205 / 1305 / 1405 |
| Khaizuran Malvin Qatrunnadiaqsa | 1106 / 1206 / 1306 / 1406 |
| M. Galih Rafiqul Islam | 1107 / 1207 / 1307 / 1407 |
| Miftahunnaufal Hidayat | 1108 / 1208 / 1308 / 1408 |
| Mochammad Wibowo Assariy | 1109 / 1209 / 1309 / 1409 |
| Mohamad Ghifari Atallah | 1110 / 1210 / 1310 / 1410 |
| Muhammad Arkandi Syahputra Santosa | 1111 / 1211 / 1311 / 1411 |
| Muhammad Azzam | 1112 / 1212 / 1312 / 1412 |
| Muhammad Hanif Baihaqi | 1113 / 1213 / 1313 / 1413 |
| Nufail | 1114 / 1214 / 1314 / 1414 |
| Rafif Pranaja Arliansyah | 1115 / 1215 / 1315 / 1415 |
| Rainadiz Danendra Nugroho | 1116 / 1216 / 1316 / 1416 |
| Rakhan Ataya Prayetno | 1117 / 1217 / 1317 / 1417 |
| Rifai Gusnian Ahmad | 1118 / 1218 / 1318 / 1418 |
| Yusuf Nawaf Albana | 1119 / 1219 / 1319 / 1419 |
| Abdurrohman | 1120 / 1220 / 1320 / 1420 |
| Kenaz Saktamulya Wiraputra | 1121 / 1221 / 1321 / 1421 |

---