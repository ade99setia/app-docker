# Face Scan Camera Forwarder

Menerima webhook dari kamera VIID (protokol standar), mengekstrak `PersonID` yang berhasil dikenali, lalu meneruskannya ke API idnsolo.com.

---

## Arsitektur: Dua Mode Deployment

### Mode Saat Ini — Forwarder Lokal (Development)

Digunakan saat kamera terhubung langsung ke laptop via kabel LAN.

```
┌─────────────────────┐
│   Kamera VIID       │  IP: 192.168.1.200
│   (Face Recognition)│  Dashboard: http://192.168.1.200/#/login
└────────┬────────────┘
         │ Kabel LAN langsung ke laptop
         │ POST http://192.168.1.100:8089/VIID/Extend/...
         ▼
┌─────────────────────┐
│   Laptop (Kubuntu)  │  IP LAN : 192.168.1.100
│   camera_forwarder  │  Port   : 8089
│   (Python/Docker)   │
└────────┬────────────┘
         │ Buang Base64 gambar, ambil PersonID saja
         │ POST HTTPS via WiFi/internet
         ▼
┌─────────────────────┐
│   idnsolo.com       │
│   VPS / Shared Host │
└─────────────────────┘
```

### Mode Pengembangan Selanjutnya — Direct Hit ke VPS (Production)

Kamera dihubungkan ke **MikroTik** yang punya akses internet.
Kamera langsung POST ke `idnsolo.com` — **tanpa forwarder lokal sama sekali**.

```
┌─────────────────────┐
│   Kamera VIID       │  IP: 10.143.25.66 (dikunci via Static DHCP)
│   (Face Recognition)│  Dashboard: http://10.143.25.66/#/login
└────────┬────────────┘
         │ Terhubung ke MikroTik (LAN/WiFi)
         │ POST HTTPS langsung ke internet
         │ POST https://idnsolo.com/api/iot/face-scan-camera/...
         ▼
┌─────────────────────┐
│   idnsolo.com       │  VPS / Shared Hosting
│   Laravel API       │  Terima data, simpan ke DB
└─────────────────────┘
```

> **Keuntungan mode ini:**
> - Tidak perlu laptop/server lokal menyala terus
> - Bisa pasang kamera di mana saja selama ada internet
> - Multi-lokasi: semua kamera nembak ke satu server yang sama
> - Real-time: data masuk detik itu juga saat wajah terdeteksi

---

## Roadmap Migrasi ke Direct Hit

### Langkah 1 — Hubungkan Kamera ke MikroTik

Pindahkan kabel LAN kamera dari laptop ke port LAN MikroTik.

```
[Kamera] ──── Kabel LAN ──── [MikroTik Port LAN]
                                      │
                              [MikroTik WAN/Internet]
                                      │
                              [idnsolo.com di cloud]
```

### Langkah 2 — Kunci IP Kamera di MikroTik (Static DHCP Lease)

Agar IP kamera tidak berubah-ubah, kunci MAC Address kamera ke IP tertentu.

Di **Winbox / Web MikroTik:**
```
IP → DHCP Server → Leases
→ Cari MAC Address kamera
→ Klik kanan → Make Static
→ Set IP: 10.143.25.66 (atau sesuai subnet MikroTik)
```

Setelah ini kamera selalu dapat IP yang sama meski restart.

### Langkah 3 — Cari Menu Cloud/Server di Dashboard Kamera

Akses dashboard kamera via browser:
```
URL   : http://10.143.25.66/#/login
Login : username & password perangkat
```

Cari menu (nama bervariasi tergantung firmware):
```
Network → Platform / HTTP Upload / Cloud Settings
         atau
Alarm → Upload → HTTP Server
         atau
Configuration → Server Settings → Identify URL
```

> **Bedakan dua jenis URL di kamera:**
>
> | Kolom          | Fungsi                              | Yang diisi              |
> | -------------- | ----------------------------------- | ----------------------- |
> | Heartbeat URL  | "Saya masih online" (ping berkala)  | Boleh kosong / opsional |
> | Identify URL   | "Si Ade baru scan" (data absensi)   | ✅ **Isi URL ini**       |

### Langkah 4 — Isi URL idnsolo.com di Kamera

| Parameter   | Nilai                                                                          |
| ----------- | ------------------------------------------------------------------------------ |
| Server URL  | `https://idnsolo.com/api/iot/face-scan-camera/auth/3/lFFkMi04oXwuAETr...`     |
| Method      | `POST`                                                                         |
| Protocol    | `HTTPS` (atau `HTTP` jika kamera tidak support SSL — lihat catatan di bawah)   |

> ⚠️ **Jika kamera tidak support HTTPS:**
> Kamera VIID lama hanya bisa HTTP. Solusinya:
> - Pasang Nginx di VPS sebagai reverse proxy HTTP → HTTPS
> - Atau buka endpoint HTTP khusus di Laravel (tidak direkomendasikan untuk production)

### Langkah 5 — Verifikasi Data Masuk

Setelah setting tersimpan dan kamera restart, cek di Laravel:

```bash
# Tail log Laravel di VPS
tail -f /var/www/idnsolo.com/storage/logs/laravel.log

# Atau cek langsung di database
# Tabel attendance / face_scan_logs
```

Atau buat endpoint debug sementara di Laravel:
```php
// routes/api.php — hanya untuk testing, hapus setelah selesai
Route::post('/iot/face-scan-camera/debug', function (Request $request) {
    \Log::info('Face scan debug', $request->all());
    return response()->json(['message' => 'received']);
});
```

---

## Perbandingan Dua Mode

| Aspek               | Mode Lokal (Sekarang)           | Mode Direct Hit (Target)         |
| ------------------- | ------------------------------- | -------------------------------- |
| Infrastruktur       | Laptop harus menyala            | Tidak perlu laptop               |
| Koneksi kamera      | Kabel LAN ke laptop             | LAN ke MikroTik                  |
| IP kamera           | `192.168.1.200`                 | `10.143.25.x` (subnet MikroTik)  |
| Forwarder           | ✅ Diperlukan                    | ❌ Tidak diperlukan               |
| Multi-lokasi        | ❌ Satu laptop per lokasi        | ✅ Semua kamera ke satu server    |
| Setup complexity    | Sederhana                       | Perlu konfigurasi MikroTik       |
| Cocok untuk         | Development / testing           | Production                       |

---

## Koneksi Fisik & Jaringan (Mode Lokal)

### 1. Skema Koneksi Fisik

```
[Kamera] ──── Kabel LAN ──── [Port Ethernet Laptop]
                                       │
                              [WiFi ke Router/Internet]
                                       │
                              [idnsolo.com di cloud]
```

### 2. Konfigurasi IP Laptop (Windows)

**Cara set IP manual:**
```
Settings → Network & Internet → Ethernet → IP Assignment → Manual → IPv4
```

| Parameter   | Nilai           |
| ----------- | --------------- |
| IP Address  | `192.168.1.100` |
| Subnet Mask | `255.255.255.0` |
| Gateway     | *(kosongkan)*   |

> **Kenapa ada banyak IP saat server start?**
>
> | IP               | Interface   | Keterangan                                       |
> | ---------------- | ----------- | ------------------------------------------------ |
> | `192.168.1.100`  | LAN (kabel) | ✅ **Gunakan ini** — terhubung langsung ke kamera |
> | `10.x.x.x`       | WiFi        | Menuju router/internet, bukan ke kamera          |
> | `169.254.x.x`    | APIPA       | IP darurat Windows, abaikan                      |

### 3. Akses Dashboard Kamera

```
URL   : http://192.168.1.200/#/login
Login : username & password perangkat kamera
```

### 4. Setting Webhook di Dashboard Kamera

Cari menu: `Network → Advanced Setup → HTTP Platform` atau `Alarm Upload`

| Parameter   | Nilai                                | Keterangan                          |
| ----------- | ------------------------------------ | ----------------------------------- |
| Server IP   | `192.168.1.100`                      | IP laptop (interface LAN ke kamera) |
| Server Port | `8089`                               | Port forwarder                      |
| Upload Path | `/VIID/Extend/ExtendFaceRecognition` | Path protokol VIID standar          |
| Protocol    | `HTTP`                               | Format JSON                         |

> IP yang tepat **otomatis ditampilkan saat server start** di banner `📡`.

---

## Payload yang Dikirim ke idnsolo.com

```json
[
  {
    "person_id": "1",
    "name": "Ade Setiawan",
    "group_id": "idn-solo",
    "device_id": "D00230000319748",
    "similarity": "0.905",
    "recognition_time": "20200101081718"
  }
]
```

| Field              | Sumber dari kamera | Keterangan                         |
| ------------------ | ------------------ | ---------------------------------- |
| `person_id`        | `PersonID`         | ID unik orang di database kamera   |
| `name`             | `Name`             | Nama lengkap                       |
| `group_id`         | `GroupID`          | Grup/departemen                    |
| `device_id`        | `DeviceID`         | Serial number kamera               |
| `similarity`       | `Similarity`       | Tingkat kecocokan wajah (0–1)      |
| `recognition_time` | `RecognitionTime`  | Waktu scan format `YYYYMMDDHHmmss` |

---

## Yang Perlu Disiapkan di idnsolo.com

### 1. Route API

**`routes/api.php`**
```php
Route::post(
    '/iot/face-scan-camera/auth/{school_id}/{token}',
    [FaceScanController::class, 'receive']
);
```

### 2. Controller

**`app/Http/Controllers/FaceScanController.php`**
```php
public function receive(Request $request, $school_id, $token)
{
    if ($token !== config('iot.face_scan_token')) {
        return response()->json(['message' => 'Unauthorized'], 401);
    }

    $persons = $request->json()->all();

    foreach ($persons as $person) {
        Attendance::create([
            'person_id'        => $person['person_id'],
            'name'             => $person['name'],
            'group_id'         => $person['group_id'],
            'device_id'        => $person['device_id'],
            'similarity'       => $person['similarity'],
            'recognition_time' => $person['recognition_time'],
            'scanned_at'       => now(),
        ]);
    }

    return response()->json(['message' => 'ok'], 200);
}
```

### 3. Response yang Diharapkan

| HTTP Status | Perilaku Forwarder                       |
| ----------- | ---------------------------------------- |
| 200–299     | ✅ Sukses, log `[OK]`                     |
| 409, 422    | ⏭️ Dianggap final, tidak retry            |
| 5xx / error | 🔁 Retry otomatis hingga 3x (backoff 1s) |

---

## Cara Running (Mode Lokal)

### Mode Python Langsung

```bash
cd 1-docker-containers/face-scan-camera/webhook/forwarder

pip install -r requirements.txt
python camera_forwarder.py
```

### Mode Docker (Kubuntu/Linux)

```bash
cd 1-docker-containers/face-scan-camera/webhook/forwarder

docker compose up -d --build
docker logs -f face-scan-camera-forwarder
docker compose down
```

> `network_mode: host` di `docker-compose.yml` memastikan container
> pakai IP host langsung — kamera di LAN bisa menjangkau port 8089.
> Mode ini hanya bekerja di **Linux** (termasuk Kubuntu). ✅

---

## Konfigurasi `.env`

```bash
cp .env.example .env
```

| Variable                   | Default     | Keterangan                         |
| -------------------------- | ----------- | ---------------------------------- |
| `LISTEN_HOST`              | `0.0.0.0`   | Interface yang didengarkan         |
| `LISTEN_PORT`              | `8089`      | Port server                        |
| `FORWARD_WEBHOOK_URL`      | *(lihat .env.example)* | URL tujuan forward    |
| `WEBHOOK_CONNECT_TIMEOUT`  | `5`         | Timeout koneksi (detik)            |
| `WEBHOOK_READ_TIMEOUT`     | `30`        | Timeout baca response (detik)      |
| `FINAL_ERROR_STATUS_CODES` | `409,422`   | Status HTTP yang tidak di-retry    |
| `DEBUG`                    | `true`      | Tampilkan raw payload di console   |

---

## Troubleshooting

| Gejala | Penyebab | Solusi |
| ------ | -------- | ------ |
| Kamera tidak kirim data | Koneksi LAN putus | Cek kabel, `ping 192.168.1.200` |
| `ping` → Request Timed Out | IP laptop salah | Set ulang IP ke `192.168.1.100` |
| Ping OK tapi data tidak masuk | Firewall memblokir | Izinkan port `8089` |
| `[ERROR] Gagal forward` | WiFi/internet mati | Pastikan koneksi internet aktif |
| Mode Direct Hit tidak kirim | Kamera tidak support HTTPS | Pasang Nginx HTTP proxy di VPS |

---

## Test Manual

```bash
curl -X POST http://localhost:8089/VIID/Extend/ExtendFaceRecognition \
  -H "Content-Type: application/json" \
  -d '{
    "PersonRecognitionResultListObject": {
      "PersonRecognitionObject": [
        {
          "PersonID": "1",
          "Name": "Ade Setiawan",
          "GroupID": "idn-solo",
          "DeviceID": "D00230000319748",
          "Similarity": "0.905",
          "RecognitionTime": "20200101081718"
        }
      ]
    }
  }'
```

---

## Struktur File

```
forwarder/
├── camera_forwarder.py   ← server utama (mode lokal)
├── config_env.py         ← loader .env
├── .env                  ← konfigurasi aktif (tidak di-commit)
├── .env.example          ← template konfigurasi
├── requirements.txt      ← dependency Python
├── Dockerfile            ← image Docker
├── docker-compose.yml    ← orchestration (network_mode: host)
└── README.md             ← dokumentasi ini
```
