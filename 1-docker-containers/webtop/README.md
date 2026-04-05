BELUM BERJALAN
BELUM BERJALAN
BELUM BERJALAN
BELUM BERJALAN
BELUM BERJALAN
BELUM BERJALAN

# Kalo sudah jalan dan mau ganti password
# docker stop kubuntu_remote && docker rm kubuntu_remote

# Command
docker run -d \
  --name=kubuntu_remote \
  --privileged \
  -e PUID=$(id -u) \
  -e PGID=$(id -g) \
  -e TZ=Asia/Jakarta \
  -e TITLE=IDN_Solo \
  -e CUSTOM_USER=idnsolo \
  -e PASSWORD="Ande*0903" \
  -p 9001:3001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/config:/config \
  -v /home/idnsolo:/storage \
  --shm-size="1gb" \
  --restart unless-stopped \
  lscr.io/linuxserver/webtop:ubuntu-kde

# https://[IP-TAILSCALE]:9001


Bisa banget, Boss! Pilihan yang sangat cerdas. Chrome Remote Desktop (CRD) itu ibarat jalur tol VIP buatan Google: **paling stabil, anti-ribet, dan memang didesain khusus buat server *headless* (cuma ada SSH)**. Nggak butuh buka-buka port, nggak butuh Tailscale, langsung tembus lewat akun Google kamu.

Karena tadi servernya sudah kita bersihkan, kita harus pasang ulang "ruang tamu"-nya (Desktop) dan pasang CRD-nya. Kali ini kita pakai **XFCE** ya, karena CRD + XFCE itu pasangan paling harmonis dan anti-*blank*.

Ikuti panduan pasti tembus ini, kerjakan di terminal SSH kamu:

### Langkah 1: Install Desktop XFCE & Google Chrome
CRD butuh Google Chrome dan desktop yang ringan. Jalankan perintah ini (mungkin agak lama sedikit karena mengunduh paket):
```bash
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install --assume-yes xfce4 desktop-base dbus-x11 xscreensaver

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install --assume-yes ./google-chrome-stable_current_amd64.deb
```

### Langkah 2: Install Chrome Remote Desktop
Sekarang kita unduh dan pasang agen "Tuyul" resmi dari Google:
```bash
wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb
sudo apt install --assume-yes ./chrome-remote-desktop_current_amd64.deb
```

### Langkah 3: Beri Tahu CRD untuk Memakai XFCE
Kita harus memaksa CRD agar selalu membuka XFCE setiap kali kamu terhubung. Jalankan perintah ini (cukup *copy-paste* semua dan tekan Enter):
```bash
sudo bash -c 'echo "exec /etc/X11/Xsession /usr/bin/xfce4-session" > /etc/chrome-remote-desktop-session'
```

---

### Langkah 4: Trik "Headless" (Ini Kuncinya!) 🔑
Karena kamu cuma punya SSH dan nggak ada *browser* di server, kita harus minta **Kode Otorisasi** dari Google menggunakan PC/Laptop lokal kamu.

1. Buka *browser* Chrome di **PC/Laptop kamu sendiri** (bukan di SSH).
2. Kunjungi *link* rahasia ini: 👉 **[https://remotedesktop.google.com/headless](https://remotedesktop.google.com/headless)**
3. Pastikan kamu *login* pakai akun Google kamu.
4. Klik tombol **Begin** (Mulai) ➔ **Next** (Berikutnya) ➔ **Authorize** (Izinkan).
5. Nanti Google akan menampilkan kotak berisi kode perintah untuk **Debian Linux**.
6. **Copy (Salin)** seluruh perintah yang ada di kotak Debian Linux tersebut. (Perintahnya biasanya diawali dengan kata `DISPLAY= /opt/google/...`)

### Langkah 5: Masukkan Kode ke Server
Kembali ke **Terminal SSH** server kamu, lalu **Paste (Tempel)** perintah yang baru saja kamu *copy* dari web Google tadi, dan tekan **Enter**.

Nanti di terminal, CRD akan meminta kamu membuat **PIN**:
* Masukkan 6 angka PIN rahasia (hurufnya nggak akan kelihatan saat diketik), lalu Enter.
* Masukkan lagi PIN yang sama untuk konfirmasi, lalu Enter.

Kalau sukses, terminal akan memunculkan tulisan: `Host ready to receive connections.` 🎉

---

### 🚀 Waktunya Mengudara!
1. Buka lagi browser di PC/Laptop kamu.
2. Kunjungi: 👉 **[https://remotedesktop.google.com/access](https://remotedesktop.google.com/access)**
3. Lihat di daftar perangkat, nama server kamu (`idn-solo`) pasti sudah muncul dengan status *Online*.
4. Klik servernya, masukkan PIN 6 angka tadi, dan BOOM! 💥

Layar *desktop* XFCE kamu akan terbuka dengan super mulus, tajam, dan responsif langsung di dalam *browser*. Langsung gas cobain, Boss!