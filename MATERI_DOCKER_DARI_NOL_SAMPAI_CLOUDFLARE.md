# Materi Docker Dari Nol Sampai Deploy ke Cloudflare

Dokumen ini disusun untuk membantu menjelaskan Docker kepada siswa dari konsep paling dasar sampai dapat memahami alur deploy aplikasi menggunakan Cloudflare Tunnel.

Fokus materi ini adalah:

1. Memahami apa itu Docker
2. Memahami image, container, volume, dan network
3. Memahami peran Docker Compose
4. Memahami alur deploy project web sederhana
5. Memahami bagaimana project Docker dipublikasikan melalui Cloudflare Tunnel

---

# 1. Tujuan Pembelajaran

Setelah mempelajari materi ini, siswa diharapkan mampu:

1. Menjelaskan perbedaan aplikasi biasa dan aplikasi yang dijalankan dengan Docker
2. Menjelaskan fungsi image, container, volume, dan network
3. Menjalankan aplikasi sederhana dengan Docker Compose
4. Memahami arsitektur project yang terdiri dari web, app, dan database
5. Menjelaskan bagaimana Cloudflare Tunnel menghubungkan internet ke container web

---

# 2. Apa Itu Docker?

Docker adalah platform untuk menjalankan aplikasi di dalam container.

Container adalah lingkungan terisolasi yang berisi:

1. Aplikasi
2. Dependency yang dibutuhkan
3. Konfigurasi runtime

Dengan Docker, aplikasi dapat dijalankan dengan cara yang lebih konsisten di laptop, server, maupun cloud.

## Penjelasan sederhana untuk siswa

Bayangkan kita punya makanan yang ingin dikirim.

1. Aplikasi adalah makanannya
2. Dependency adalah bumbu dan alat makannya
3. Container adalah kotak makanannya
4. Docker adalah sistem yang menyiapkan dan mengirim kotak itu

Artinya, aplikasi tidak lagi tergantung pada kondisi komputer secara langsung, karena semua sudah dibungkus dalam container.

---

## Ruang Gambar 1

Tempatkan gambar yang menunjukkan perbandingan:

1. Aplikasi biasa diinstal langsung di sistem operasi
2. Aplikasi berjalan di dalam container Docker

Catatan pengajar:
Gunakan diagram sederhana agar siswa langsung melihat bahwa Docker membuat aplikasi lebih rapi dan terisolasi.

---

# 3. Mengapa Docker Penting?

Masalah yang sering terjadi tanpa Docker:

1. Di laptop guru berjalan, di laptop siswa tidak berjalan
2. Versi PHP, Node.js, Python, atau database berbeda
3. Instalasi dependency memakan waktu lama
4. Deployment ke server sering gagal karena environment berbeda

Keuntungan Docker:

1. Lingkungan aplikasi konsisten
2. Instalasi lebih cepat
3. Mudah dipindahkan ke server lain
4. Mudah di-scale dan dikelola
5. Cocok untuk pembelajaran DevOps dan deployment modern
6. Bisa menjalankan aplikasi lama dan aplikasi baru secara berdampingan
7. Memudahkan proses upgrade bertahap tanpa mematikan layanan lama
8. Mempermudah rollback jika versi baru bermasalah

## 3.1 Keunggulan Docker Dalam Dunia Nyata

Docker bukan hanya berguna untuk developer, tetapi juga sangat berguna untuk kebutuhan bisnis dan layanan pengguna.

Beberapa keunggulan tambahannya:

1. Satu server bisa menjalankan banyak aplikasi dengan dependency berbeda
2. Aplikasi versi lama tetap bisa hidup tanpa bentrok dengan aplikasi versi baru
3. Tim bisa melakukan migrasi sistem secara bertahap
4. Risiko gangguan layanan lebih kecil karena perubahan tidak harus dilakukan sekaligus
5. Pengguna lama tetap bisa memakai alur yang sudah mereka pahami

Contoh penjelasan untuk siswa:

Ada kondisi di mana sebuah perusahaan memiliki:

1. Aplikasi versi lama yang sudah dipakai bertahun-tahun
2. Aplikasi versi baru yang tampilannya lebih modern dan fiturnya lebih lengkap

Masalahnya, tidak semua pengguna siap pindah langsung ke versi baru.

Misalnya pada layanan digital skala besar seperti perbankan, sering ada kebutuhan untuk tetap menjaga layanan lama tetap aktif, karena sebagian pengguna lama lebih nyaman dengan tampilan dan alur yang sudah mereka kenal. Yang paling penting bagi mereka adalah transaksi tetap bisa dilakukan dengan mudah, tanpa harus belajar ulang seluruh tampilan baru dalam waktu singkat.

Di sinilah Docker sangat unggul.

Dengan Docker, perusahaan dapat menjalankan:

1. Container aplikasi lama dengan image versi lama
2. Container aplikasi baru dengan image versi baru

Keduanya bisa berjalan bersamaan dalam server atau infrastruktur yang sama, selama pengaturan port, network, dan resource dibuat dengan benar.

Artinya:

1. Pengguna lama tetap terlayani
2. Pengguna baru bisa mulai memakai sistem modern
3. Tim pengembang tidak dipaksa migrasi total dalam satu malam
4. Perubahan bisa dilakukan bertahap dan lebih aman

Ini adalah salah satu nilai besar Docker: kompatibilitas dan transisi yang lebih halus.

## 3.2 Contoh Sederhana Menjalankan Dua Versi Aplikasi

Misalkan ada dua versi web:

1. `aplikasi-legacy:v1`
2. `aplikasi-modern:v2`

Keduanya dapat dijalankan bersamaan seperti ini:

```yaml
services:
  app_legacy:
    image: aplikasi-legacy:v1
    container_name: app_legacy
    ports:
      - "8088:80"

  app_modern:
    image: aplikasi-modern:v2
    container_name: app_modern
    ports:
      - "8089:80"
```

Dengan pendekatan ini:

1. Versi lama tetap bisa diakses
2. Versi baru juga bisa diuji atau dipakai paralel
3. Perbandingan performa dan penerimaan pengguna bisa diamati
4. Jika versi baru bermasalah, versi lama masih tersedia

Ini cocok dijelaskan ke siswa sebagai strategi transisi sistem, bukan sekadar teknik menjalankan container.

---

## Ruang Gambar 1A

Tempatkan gambar perbandingan strategi layanan:

1. Sistem lama dimatikan lalu langsung pindah ke sistem baru
2. Sistem lama dan sistem baru berjalan bersamaan

Catatan pengajar:
Tekankan bahwa pada banyak layanan besar, transisi bertahap sering lebih aman daripada migrasi mendadak.

---

# 4. Konsep Dasar Yang Harus Dipahami

## 4.1 Image

Image adalah blueprint atau cetakan.

Image berisi semua yang dibutuhkan untuk menjalankan aplikasi.

Contoh:

1. `nginx:alpine`
2. `mysql:8.0`
3. `cloudflare/cloudflared:latest`

Penjelasan sederhana:
Image seperti file installer atau template siap pakai.

## 4.2 Container

Container adalah hasil jadi yang berjalan dari image.

Jika image adalah cetakan, maka container adalah mesin yang benar-benar hidup dan bekerja.

Contoh:

1. Image `nginx:alpine`
2. Container `portofolio_web`

## 4.3 Volume

Volume adalah tempat penyimpanan data yang tetap ada walaupun container dihapus atau dibuat ulang.

Contoh fungsi volume:

1. Menyimpan data database MySQL
2. Menyimpan file upload
3. Menyimpan folder storage aplikasi

## 4.4 Network

Network adalah jalur komunikasi antar-container.

Contoh:

1. Container web terhubung ke container app
2. Container app terhubung ke container database
3. Container Cloudflare Tunnel terhubung ke container web melalui shared network

## 4.5 Port

Port adalah pintu akses.

Contoh:

1. `8083:80` artinya port 8083 di host diarahkan ke port 80 di container
2. Saat browser membuka `http://localhost:8083`, permintaan masuk ke port 80 milik container web

---

## Ruang Gambar 2

Tempatkan gambar konsep dasar Docker:

1. Image
2. Container
3. Volume
4. Network
5. Port mapping

Catatan pengajar:
Jika memungkinkan, buat satu diagram dengan ikon sederhana dan panah hubungan antar-komponen.

---

# 5. Perintah Dasar Docker Yang Perlu Dikenalkan

Berikut beberapa perintah dasar yang cukup penting untuk tahap awal.

```bash
docker ps
docker ps -a
docker images
docker logs -f nama_container
docker exec -it nama_container sh
docker stop nama_container
docker rm nama_container
docker network ls
docker volume ls
```

Penjelasan singkat:

1. `docker ps` melihat container yang sedang berjalan
2. `docker images` melihat image yang tersedia
3. `docker logs` melihat log aplikasi
4. `docker exec` masuk ke dalam container
5. `docker network ls` melihat daftar network
6. `docker volume ls` melihat daftar volume

Untuk pembelajaran awal, cukup fokus dulu pada membaca status, melihat log, dan memahami hubungan container.

---

# 6. Apa Itu Docker Compose?

Docker Compose adalah cara untuk menjalankan banyak container sekaligus menggunakan satu file konfigurasi `docker-compose.yml`.

Ini sangat penting karena aplikasi modern biasanya tidak hanya satu container.

Contoh satu project bisa terdiri dari:

1. Web server Nginx
2. App server PHP-FPM atau Node.js
3. Database MySQL atau PostgreSQL

Dengan Compose, semua service tersebut dapat didefinisikan dalam satu file dan dijalankan bersama.

Perintah umum:

```bash
docker compose up -d
docker compose up -d --build
docker compose down
docker compose ps
```

---

# 7. Membaca Struktur Docker Compose Sederhana

Contoh paling sederhana untuk web statis:

```yaml
services:
  web:
    image: nginx:alpine
    container_name: web_portofolio
    ports:
      - "8083:80"
    restart: unless-stopped
```

Penjelasan:

1. `services` berisi daftar layanan yang dijalankan
2. `web` adalah nama service
3. `image` adalah image yang dipakai
4. `container_name` adalah nama container yang mudah dikenali
5. `ports` menghubungkan host ke container
6. `restart: unless-stopped` membuat container otomatis hidup kembali jika server restart

---

## Ruang Gambar 3

Tempatkan screenshot:

1. File `docker-compose.yml`
2. Hasil `docker ps`
3. Browser membuka project di port lokal

Catatan pengajar:
Bagian ini bagus untuk menunjukkan bahwa satu file konfigurasi bisa langsung menghasilkan container yang jalan.

---

# 8. Studi Kasus Arsitektur Project Docker

Di dokumentasi server Anda, ada pola project yang sangat baik untuk dijadikan contoh mengajar.

Misalnya satu project Laravel atau CI4 biasanya terdiri dari:

1. Container app
2. Container web
3. Container database

Contoh alur komunikasi:

1. User membuka browser
2. Request masuk ke container web Nginx
3. Nginx meneruskan request ke container app
4. Container app mengambil atau menyimpan data ke database

Ilustrasi sederhana:

```text
Browser
  |
  v
Nginx (web)
  |
  v
App (PHP-FPM / Node.js)
  |
  v
Database (MySQL / PostgreSQL)
```

Poin penting untuk siswa:

1. Web bukan database
2. App bukan web server
3. Database tidak perlu dibuka ke publik jika tidak diperlukan
4. Setiap service punya tugas masing-masing

---

## Ruang Gambar 4

Tempatkan diagram arsitektur 3 lapis:

1. Browser
2. Web server
3. App server
4. Database

Catatan pengajar:
Gunakan warna berbeda untuk membedakan layer presentasi, logic, dan data.

---

# 9. Memahami Network Pada Docker

Secara konsep, Docker network memungkinkan container saling berbicara dengan aman.

Dalam project nyata, biasanya ada dua jenis network:

1. Network internal project
2. Network bersama untuk akses tertentu

Contoh dari dokumentasi Anda:

1. `app_network_idn_solo` untuk komunikasi internal project IDN Solo
2. `shared_web_network` untuk komunikasi ke Cloudflare Tunnel atau service lintas project

Mengapa ini penting?

1. Database tetap terisolasi di network project
2. Hanya service web yang perlu dibuka ke shared network
3. Cloudflare Tunnel cukup mengenal container web, tidak perlu langsung ke database

Ini adalah prinsip keamanan yang baik untuk dikenalkan sejak awal.

---

# 10. Memahami Shared Network dan Multi Project

Dalam dokumentasi infrastruktur, beberapa project dihubungkan ke network bersama bernama `shared_web_network`.

Tujuannya adalah agar:

1. Satu container Cloudflare Tunnel bisa mengakses banyak project
2. Masing-masing project tetap punya network internal sendiri
3. Routing menjadi lebih sederhana

Ilustrasi:

```text
Cloudflare Tunnel
       |
       v
shared_web_network
   |         |         |
   v         v         v
web_app_1  web_app_2  web_app_3
```

Yang perlu ditekankan ke siswa:

1. Tidak semua container harus masuk shared network
2. Biasanya cukup container web saja
3. Ini membuat desain lebih rapi dan aman

---

## Ruang Gambar 5

Tempatkan diagram network:

1. Internal network per project
2. Shared network bersama
3. Cloudflare Tunnel sebagai gerbang publik

Catatan pengajar:
Bagian ini sangat efektif jika divisualkan dengan panah dan kotak network.

---

# 11. Apa Itu Cloudflare Tunnel?

Cloudflare Tunnel adalah cara untuk mempublikasikan aplikasi ke internet tanpa harus membuka port publik langsung di server.

Secara sederhana:

1. Server kita membuat koneksi keluar ke Cloudflare
2. Cloudflare menerima request dari internet
3. Cloudflare meneruskan request ke service internal yang kita tentukan

Keuntungan Cloudflare Tunnel:

1. Tidak perlu membuka port publik satu per satu di router atau firewall
2. Domain bisa diarahkan ke service internal dengan lebih aman
3. Cocok untuk publish aplikasi Docker dari server rumah atau VPS

---

# 12. Alur Deploy ke Cloudflare Tunnel

Urutan sederhananya seperti ini:

1. Aplikasi berjalan di container web
2. Container web terhubung ke `shared_web_network`
3. Container `cloudflared` juga terhubung ke `shared_web_network`
4. Di dashboard Cloudflare dibuat route domain ke nama container web
5. User mengakses domain dari internet
6. Request diteruskan oleh Cloudflare ke container web

Ilustrasi:

```text
Internet
   |
   v
Cloudflare
   |
   v
cloudflared
   |
   v
shared_web_network
   |
   v
container_web:80
```

---

## Ruang Gambar 6

Tempatkan gambar alur request dari internet:

1. User
2. Cloudflare
3. Cloudflared container
4. Shared network
5. Container web

Catatan pengajar:
Bagian ini ideal dijadikan diagram utama saat menjelaskan bagaimana domain bisa sampai ke container.

---

# 13. Contoh Compose Untuk Web Yang Siap Diakses Tunnel

Berikut contoh yang disederhanakan dari pola yang sudah Anda gunakan:

```yaml
services:
  web_portofolio:
    image: ghcr.io/ade99setia/portofolio:latest
    container_name: portofolio_web
    restart: unless-stopped
    ports:
      - "8083:80"
    networks:
      - portfolio_network
      - shared_web_network

networks:
  portfolio_network:
    driver: bridge
  shared_web_network:
    external: true
```

Hal yang perlu dijelaskan ke siswa:

1. Service web tetap punya network internal sendiri
2. Service web juga masuk `shared_web_network`
3. Karena masuk `shared_web_network`, Cloudflare Tunnel dapat mengaksesnya

---

# 14. Contoh Compose Untuk Cloudflare Tunnel

Berikut contoh struktur compose untuk tunnel:

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared_idn_server
    command: tunnel --no-autoupdate run --token ${CLOUDFLARE_TUNNEL_TOKEN} --protocol http2
    networks:
      - shared_web_network
    restart: unless-stopped

networks:
  shared_web_network:
    external: true
```

Penekanan penting:

1. Container tunnel tidak perlu expose port web ke publik secara langsung
2. Tunnel cukup terhubung ke network yang sama dengan container web
3. Sebaiknya token disimpan di `.env` atau secret, jangan di-hardcode di file publik

---

# 15. Langkah Mengajar Siswa Secara Praktik

Urutan praktik yang mudah dipahami siswa:

## Tahap 1: Kenalkan Docker

1. Jelaskan image dan container
2. Tunjukkan `docker ps` dan `docker images`
3. Jalankan satu container Nginx sederhana

Contoh:

```bash
docker run -d --name web-demo -p 8088:80 nginx:alpine
```

Lalu buka browser ke `http://localhost:8088`.

## Tahap 2: Kenalkan Docker Compose

1. Tunjukkan file `docker-compose.yml`
2. Jalankan `docker compose up -d`
3. Lihat hasil container dengan `docker compose ps`

## Tahap 3: Kenalkan Network

1. Jelaskan kenapa container perlu saling terhubung
2. Tunjukkan network internal project
3. Jelaskan konsep `shared_web_network`

## Tahap 4: Kenalkan Cloudflare Tunnel

1. Jelaskan bahwa domain dari internet tidak langsung masuk ke server melalui port terbuka
2. Jelaskan bahwa server membuat koneksi keluar ke Cloudflare
3. Tunjukkan container `cloudflared` yang menjadi jembatan ke container web

---

# 16. Urutan Deploy Sampai Bisa Diakses Domain

Berikut urutan langkah logis dari awal sampai publish:

1. Siapkan aplikasi web
2. Jalankan dengan Docker atau Docker Compose
3. Pastikan aplikasi bisa diakses lokal melalui port host
4. Buat network bersama jika belum ada
5. Hubungkan container web ke `shared_web_network`
6. Jalankan container `cloudflared`
7. Atur route domain di Cloudflare ke container web
8. Uji akses dari internet

Contoh membuat network bersama:

```bash
docker network create shared_web_network
```

Contoh cek container:

```bash
docker ps
docker network ls
docker logs -f cloudflared_idn_server
```

---

## Ruang Gambar 7

Tempatkan screenshot langkah deploy:

1. `docker network create shared_web_network`
2. `docker compose up -d`
3. Container cloudflared berjalan
4. Dashboard Cloudflare Public Hostname
5. Hasil domain berhasil dibuka di browser

---

# 17. Kesalahan Yang Sering Terjadi

Ini penting untuk bahan diskusi saat mengajar.

## 17.1 Container jalan, tapi web tidak bisa dibuka

Kemungkinan:

1. Port mapping salah
2. Nginx belum benar
3. Container crash dan restart terus

## 17.2 Cloudflare Tunnel hidup, tapi domain tidak tembus

Kemungkinan:

1. Container web belum masuk `shared_web_network`
2. Nama target di dashboard Cloudflare salah
3. Service web tidak berjalan di port yang benar

## 17.3 Database hilang setelah container dibuat ulang

Kemungkinan:

1. Tidak menggunakan volume
2. Volume salah konfigurasi

## 17.4 Siswa bingung bedanya image dan container

Solusi:

1. Ulangi analogi cetakan dan hasil jadi
2. Tunjukkan satu image bisa melahirkan beberapa container

---

# 18. Tips Penjelasan Agar Mudah Dipahami Siswa

Saat mengajar, gunakan urutan berpikir berikut:

1. Mulai dari masalah nyata: "Kenapa aplikasi di laptop A jalan tapi di laptop B tidak?"
2. Baru masuk ke solusi: Docker menyamakan environment
3. Kenalkan istilah sedikit demi sedikit
4. Gunakan diagram lebih banyak daripada definisi panjang
5. Tunjukkan langsung contoh container yang hidup
6. Hubungkan teori ke project asli yang benar-benar Anda jalankan

Kalimat sederhana yang efektif:

1. Image adalah cetakan
2. Container adalah hasil jadi yang berjalan
3. Volume adalah tempat menyimpan data
4. Network adalah jalur komunikasi
5. Cloudflare Tunnel adalah jembatan dari internet ke container web

---

# 19. Ringkasan Singkat Untuk Siswa

Docker membantu kita menjalankan aplikasi dalam container yang konsisten dan terisolasi.

Komponen pentingnya adalah:

1. Image untuk cetakan aplikasi
2. Container untuk aplikasi yang berjalan
3. Volume untuk menyimpan data
4. Network untuk komunikasi antar-service
5. Docker Compose untuk menjalankan banyak service sekaligus

Ketika aplikasi ingin dipublikasikan ke internet:

1. Container web dijalankan
2. Container web dihubungkan ke network bersama
3. Cloudflare Tunnel dihubungkan ke network yang sama
4. Domain di Cloudflare diarahkan ke container web
5. Aplikasi dapat diakses dari internet tanpa membuka port publik secara langsung

Docker juga unggul karena memungkinkan organisasi menjalankan beberapa versi aplikasi secara bersamaan. Ini sangat membantu saat layanan lama masih dibutuhkan oleh pengguna lama, sementara layanan baru mulai diperkenalkan ke pengguna baru.

---

# 20. Tugas atau Diskusi Untuk Siswa

Gunakan pertanyaan ini setelah materi selesai.

1. Apa perbedaan image dan container?
2. Mengapa database sebaiknya tidak langsung dibuka ke internet?
3. Mengapa volume penting untuk project database?
4. Mengapa Cloudflare Tunnel cukup diarahkan ke container web, bukan ke database?
5. Apa manfaat `shared_web_network` pada arsitektur multi project?
6. Mengapa perusahaan kadang perlu menjalankan aplikasi versi lama dan versi baru secara bersamaan?
7. Apa keuntungan Docker dalam proses migrasi bertahap dari sistem lama ke sistem baru?

---

# 21. Penutup

Jika siswa sudah memahami alur pada materi ini, maka mereka sudah memiliki fondasi penting untuk:

1. Menjalankan aplikasi dengan Docker
2. Membaca file Docker Compose
3. Memahami arsitektur service sederhana
4. Memahami cara publish aplikasi ke internet menggunakan Cloudflare Tunnel

Materi ini sengaja difokuskan sampai tahap deploy ke Cloudflare agar siswa memperoleh gambaran utuh dari konsep lokal sampai akses publik.

---

# Lampiran Ringkas Untuk Demo Cepat

```bash
docker network create shared_web_network
docker compose up -d
docker ps
docker logs -f cloudflared_idn_server
```

Checklist demo:

1. Container web berjalan
2. Container tunnel berjalan
3. Shared network tersedia
4. Route domain di Cloudflare benar
5. Domain bisa diakses dari browser