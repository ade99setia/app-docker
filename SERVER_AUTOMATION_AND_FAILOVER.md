# ⚙️ Server Automation & Failover Documentation

Dokumentasi ini mencakup:

* Auto Shutdown & Auto Wake-up menggunakan RTC
* Failover halaman maintenance menggunakan Cloudflare Worker
* Infrastruktur Mini PC via Cloudflare Tunnel
* Troubleshooting & Best Practice

---

# 🖥️ 1. Auto Shutdown & Auto Wake-up (RTC)

## Persyaratan

| Komponen | Keterangan                   |
| -------- | ---------------------------- |
| OS       | Ubuntu / Kubuntu / Debian    |
| Akses    | sudo                         |
| Hardware | Motherboard dengan RTC       |
| Power    | Tidak boleh listrik terputus |

---

# 1.1 Cek Dukungan RTC

```bash
cat /proc/driver/rtc
```

### Output yang benar

| Field       | Status   |
| ----------- | -------- |
| rtc_time    | muncul   |
| rtc_date    | muncul   |
| batt_status | **okay** |

Jika `batt_status = okay` berarti CMOS battery masih baik.

---

# 1.2 Test Wake-up Manual

Matikan PC lalu nyala otomatis 60 detik:

```bash
sudo rtcwake -m off -s 60
```

Matikan PC lalu nyala otomatis 12 menit:

```bash
sudo rtcwake -m off -s $((60 * 12))
```

Matikan PC lalu nyala otomatis 8 Jam:

```bash
sudo rtcwake -m off -s $((60 * 60 * 8))
```

### Behavior

| Event    | Hasil              |
| -------- | ------------------ |
| SSH      | terputus           |
| PC       | mati               |
| 60 detik | otomatis hidup     |
| Boot     | masuk login screen |

Jika berhasil → RTC support OK

---

# 1.3 Konfigurasi Auto Schedule (Cron)

Buka crontab root

```bash
sudo crontab -e
```

---

# 1.4 Jadwal Contoh

## Mati 23:00 — Nyala 06:00 (Daily)

```bash
00 23 * * * /usr/sbin/rtcwake -m off -t $(date -d "tomorrow 06:00" +\%s)
```

## Mati 02:00 — Nyala 08:00 (Senin-Jumat)

```bash
00 02 * * 1-5 /usr/sbin/rtcwake -m off -t $(date -d "today 08:00" +\%s)
```

⚠️ `%s` wajib ditulis `\%s` dalam cron

---

# 1.5 Verifikasi Jadwal

```bash
sudo crontab -l
```

---

# 1.6 Catatan Penting

| Kondisi            | Dampak                |
| ------------------ | --------------------- |
| Listrik mati       | Tidak akan nyala      |
| Shutdown manual    | Alarm tidak tersimpan |
| Timezone salah     | Jadwal meleset        |
| CMOS battery lemah | Alarm gagal           |

Cek timezone:

```bash
date
```

---

# ☁️ 2. Failover Maintenance Page (Cloudflare Worker)

Digunakan untuk menampilkan halaman HTML saat Mini PC offline.

---

# 2.1 Flow Kerja

| Step | Deskripsi                       |
| ---- | ------------------------------- |
| 1    | User akses domain               |
| 2    | Worker intercept                |
| 3    | Worker fetch server             |
| 4    | Jika online → forward           |
| 5    | Jika error → tampil maintenance |

---

# 2.2 Error Yang Ditangani

| Status       | Keterangan     |
| ------------ | -------------- |
| 1033         | Tunnel Error   |
| 502          | Bad Gateway    |
| 504          | Timeout        |
| fetch failed | server offline |

---

# 2.3 Worker Configuration

| Parameter       | Nilai                  |
| --------------- | ---------------------- |
| Worker Name     | maintenance-checker    |
| Route           | *.ade-setiawan.my.id/* |
| Content-Type    | text/html              |
| Failover Status | 200                    |
| Mode            | Proxy only             |

---

# 2.4 Logic Worker

```
User
  │
Cloudflare Worker
  │
  ├── Server Online → forward
  └── Server Offline → custom HTML
```

---

# 2.5 HTML Maintenance

Disimpan dalam variable:

```javascript
const maintenanceHTML = `
HTML DISINI
`;
```

---

# 2.6 Edit Tampilan

Langkah:

1. Cloudflare Dashboard
2. Workers & Pages
3. maintenance-checker
4. Edit Code
5. Deploy

Perubahan realtime.

---

# 2.7 DNS Requirement

DNS harus:

| Setting    | Status |
| ---------- | ------ |
| Proxy      | ON     |
| Cloud icon | Orange |
| DNS Only   | ❌      |

Jika DNS only → Worker tidak berjalan

---

# 2.8 Troubleshooting

| Masalah                   | Solusi         |
| ------------------------- | -------------- |
| Masih maintenance         | Ctrl + F5      |
| Cache browser             | Incognito      |
| Tunnel hidup tapi offline | cek logs       |
| Subdomain baru            | auto protected |

---

# 2.9 Monitoring

Lihat statistik:

Cloudflare → Worker → Observability

Menampilkan:

* jumlah failover
* error rate
* traffic

---

# 🔁 3. Integrasi dengan Auto Shutdown

Flow lengkap:

```
Cron RTC Shutdown
        │
Mini PC Mati
        │
Cloudflare Worker aktif
        │
User lihat maintenance page
        │
RTC Alarm
        │
Mini PC hidup
        │
Worker forward traffic
```

---

# 📊 Ringkasan Sistem

| Komponen | Fungsi            |
| -------- | ----------------- |
| RTC      | Auto power on     |
| Cron     | schedule shutdown |
| Worker   | failover page     |
| Tunnel   | koneksi internet  |
| Mini PC  | hosting server    |

---

# ✅ Behavior Sistem

| Kondisi        | Hasil            |
| -------------- | ---------------- |
| PC hidup       | website normal   |
| PC mati        | maintenance page |
| PC bangun      | website kembali  |
| tunnel error   | maintenance page |
| restart server | normal           |

---

# 🚀 Keuntungan Sistem

| Fitur           | Benefit                |
| --------------- | ---------------------- |
| Auto shutdown   | hemat listrik          |
| Auto wake       | tanpa manual           |
| Worker failover | tidak terlihat offline |
| Single tunnel   | ringan                 |
| Cron RTC        | stabil                 |

---

# ⚠️ Best Practice

* gunakan timezone UTC+7 sesuai server
* jangan cabut listrik
* gunakan CMOS battery sehat
* monitor worker log
* test rtcwake sebelum production

---

# 🧪 Test Lengkap

Test end-to-end:

```bash
sudo rtcwake -m off -s 120
```

Expected:

1. server mati
2. worker tampil maintenance
3. server hidup
4. site normal

---

# 🟢 Status Infrastruktur

* Auto shutdown : aktif
* Auto wake : aktif
* Failover worker : aktif
* Tunnel : aktif
* Production ready : YES
