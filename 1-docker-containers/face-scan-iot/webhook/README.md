# Face Scan Webhook Modes

Folder ini sekarang mendukung 2 mode:

- `polling` untuk ambil data dari device tiap 5 menit lalu forward ke endpoint Laravel
- `realtime` untuk menerima webhook trigger dari device, lalu Python langsung mengambil database dari IoT Face dan mengirim hasilnya ke endpoint Laravel

Script juga mendukung penyaringan record agar yang diproses hanya status yang dianggap berhasil, dan respons akhir seperti `409` atau `422` dapat dianggap final agar record yang sama tidak dikirim terus.

## File Utama

- `polling_forwarder.py` = mode polling 5 menit
- `realtime_webhook_receiver.py` = mode realtime receiver
- `collector.py` = wrapper kompatibilitas lama, akan menjalankan mode polling
- `docker-compose.yml` = Docker Compose dengan profile `polling` dan `realtime`
- `start_realtime.ps1` = jalankan mode realtime lokal tanpa Docker
- `start_polling.ps1` = jalankan mode polling lokal tanpa Docker
- `test_realtime.ps1` = kirim request test ke mode realtime lokal
- `nginx-face-scan-realtime.conf` = snippet Nginx untuk route `/api/hf/hf01`

## Jalankan Tanpa Docker

Gunakan Python 3.11.

### 1. Install dependency

PowerShell:

```powershell
cd d:\3-ProjectWebsite\app-docker\1-docker-containers\face-scan-iot\webhook
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Kalau Anda sudah punya virtualenv aktif lain, cukup jalankan:

```powershell
pip install -r requirements.txt
```

### 2. Siapkan file `.env`

PowerShell:

```powershell
Copy-Item .env.example .env
```

Kalau perlu, edit nilai di `.env` sesuai device dan endpoint yang ingin dipakai.

### 3. Jalankan mode realtime

PowerShell:

```powershell
python .\realtime_webhook_receiver.py
```

Atau pakai helper script:

```powershell
.\start_realtime.ps1
```

Endpoint lokal yang aktif:

- `http://localhost:8088/api/hf/hf01`
- `http://localhost:8088/health`

Pada mode realtime, request masuk tidak langsung diteruskan ke Laravel. Request itu hanya menjadi trigger bahwa device aktif atau selesai scan, lalu Python akan mengambil database dari device dan mengirim data checkin yang baru ke Laravel.

Kalau tidak memakai `.env`, Anda tetap bisa override dari PowerShell:

```powershell
$env:LISTEN_HOST = "0.0.0.0"
$env:LISTEN_PORT = "8088"
$env:EXPECTED_PATH = "/api/hf/hf01"
$env:FORWARD_WEBHOOK_URL = "https://idnsolo.com/api/iot/face-scan/auth/3/lFFkMi04oXwuAETrQwVEbQBjMqNuY3hZuWXTD4YGa0d0ee7f"
python .\realtime_webhook_receiver.py
```

### 4. Jalankan mode polling 5 menit

PowerShell:

```powershell
python .\polling_forwarder.py
```

Atau pakai helper script:

```powershell
.\start_polling.ps1
```

Kalau mau interval 1 menit untuk testing:

```powershell
$env:POLL_INTERVAL_SECONDS = "60"
python .\polling_forwarder.py
```

## Test Realtime Dengan Curl

Kalau server Python realtime sudah aktif di local:

```powershell
curl.exe -X POST "http://localhost:8088/api/hf/hf01" ^
  -H "Content-Type: application/json" ^
  -d "{\"device_id\":\"G013524JZXDD784\",\"product_key\":\"uniwin\",\"time\":\"1776344825\"}"
```

Response normal:

```json
{
  "status": "ok",
  "message": "data berhasil disinkronkan",
  "records_count": 3
}
```

Untuk health check:

```powershell
curl.exe "http://localhost:8088/health"
```

Atau pakai helper script:

```powershell
.\test_realtime.ps1
```

## Perilaku Mode Realtime

Script realtime menerima JSON trigger dari device. Payload trigger itu tidak diteruskan langsung ke Laravel.

Alurnya adalah:

1. IoT Face mengirim notifikasi singkat ke endpoint lokal `/api/hf/hf01`
2. Python realtime menerima notifikasi itu sebagai trigger
3. Python memanggil device IoT Face untuk export database log
4. Python mengunduh database log dari device
5. Python mengambil record checkin baru yang belum pernah dikirim
6. Python mengirim record checkin baru itu ke endpoint Laravel

Contoh request trigger masuk:

```json
{
  "device_id": "G013524JZXDD784",
  "product_key": "uniwin",
  "time": "1776344825"
}
```

Contoh data yang benar-benar dikirim ke Laravel setelah Python mengambil database device:

```json
[
  {
    "device_id": "G013524JZXDD784",
    "product_key": "uniwin",
    "time": "1776344825"
  }
]
```

## Jalankan Dengan Docker

Sebelum menjalankan Docker, siapkan file `.env` lebih dulu:

```powershell
Copy-Item .env.example .env
```

### Mode realtime

```powershell
docker compose --profile realtime up --build -d
```

Perintah ini setara dengan menjalankan lokal:

```powershell
python .\realtime_webhook_receiver.py
```

Di mode Docker ini:

- container membuka port `8088`
- container membaca konfigurasi dari file `.env`
- container memakai `last_checkin_time.txt` yang dimount dari host
- perilaku checkpoint sync sama seperti saat dijalankan langsung dengan Python

### Mode polling

```powershell
docker compose --profile polling up --build -d
```

Perintah ini setara dengan menjalankan lokal:

```powershell
python .\polling_forwarder.py
```

Di mode Docker ini:

- container berjalan mandiri tanpa menunggu trigger dari IoT
- container membaca konfigurasi dari file `.env`
- container memakai `last_checkin_time.txt` yang dimount dari host
- interval polling tetap mengikuti `POLL_INTERVAL_SECONDS` di `.env`

### Stop mode yang sedang aktif

```powershell
docker compose --profile realtime down
docker compose --profile polling down
```

Kalau ingin melihat log Docker:

```powershell
docker logs -f face-scan-webhook-realtime
docker logs -f face-scan-webhook-polling
```

## Catatan Routing

Kalau testing masih lokal, cukup kirim request trigger ke:

- `http://localhost:8088/api/hf/hf01`

Kalau nanti produksi memakai domain `https://idnsolo.com/api/hf/hf01`, route Nginx atau reverse proxy harus diarahkan ke service realtime ini di port `8088`.

Contoh Nginx reverse proxy:

```nginx
location /api/hf/hf01 {
  proxy_pass http://127.0.0.1:8088;
  proxy_http_version 1.1;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
}
```

Jika Nginx berjalan di dalam container Docker dan Python realtime dipublish ke host port `8088`, gunakan snippet siap pakai di `nginx-face-scan-realtime.conf` yang memakai `host.docker.internal:8088`.

Konfigurasi IDN Solo di project ini sudah dipatch langsung pada file Nginx prod dan dev agar `/api/hf/hf01` diteruskan ke Python realtime di port `8088`.

## Deploy Routing IDN Solo

Patch routing sudah dipasang langsung pada file berikut:

- `..\..\idn-solo\default.conf`
- `..\..\idn-solo\default.dev.conf`
- `..\..\idn-solo\docker-compose.yml`
- `..\..\idn-solo\docker-compose.dev.yml`

Artinya route `/api/hf/hf01` di Nginx IDN Solo sekarang diarahkan ke Python realtime pada host port `8088` lewat `host.docker.internal`.

### Reload Nginx IDN Solo Prod

PowerShell:

```powershell
cd d:\3-ProjectWebsite\app-docker\1-docker-containers\idn-solo
docker compose up -d --force-recreate web_idn_solo
```

### Reload Nginx IDN Solo Dev

PowerShell:

```powershell
cd d:\3-ProjectWebsite\app-docker\1-docker-containers\idn-solo
docker compose -f docker-compose.dev.yml up -d --force-recreate web_idn_solo_dev
```

### Urutan Aktivasi Yang Benar

Untuk mode realtime agar domain `https://idnsolo.com/api/hf/hf01` benar-benar bekerja:

1. Jalankan Python realtime di PC atau host yang membuka port `8088`
2. Pastikan test lokal `http://localhost:8088/health` merespons normal
3. Recreate container Nginx IDN Solo prod atau dev
4. Uji endpoint domain atau server yang melewati Nginx
5. Pastikan Python dapat menjangkau device IoT Face pada IP local yang sama

### Verifikasi Setelah Deploy

Tes health lokal Python:

```powershell
curl.exe "http://localhost:8088/health"
```

Tes endpoint realtime lokal:

```powershell
curl.exe -X POST "http://localhost:8088/api/hf/hf01" ^
  -H "Content-Type: application/json" ^
  -d "{\"device_id\":\"G013524JZXDD784\",\"product_key\":\"uniwin\",\"time\":\"1776344825\"}"
```

Tes endpoint yang lewat Nginx IDN Solo:

```powershell
curl.exe -X POST "http://localhost:8084/api/hf/hf01" ^
  -H "Content-Type: application/json" ^
  -d "{\"device_id\":\"G013524JZXDD784\",\"product_key\":\"uniwin\",\"time\":\"1776344825\"}"
```

Kalau container IDN Solo berjalan di server lain, ganti `localhost:8084` dengan host atau domain server tersebut.

## Environment Variable

### Realtime

- `LISTEN_HOST` default `0.0.0.0`
- `LISTEN_PORT` default `8088`
- `EXPECTED_PATH` default `/api/hf/hf01`
- `FORWARD_WEBHOOK_URL` target endpoint Laravel untuk data hasil sync database

### Polling

- `DEVICE_IP` IP device face scan
- `DEVICE_PASSWORD` password device
- `POLL_INTERVAL_SECONDS` default `300`
- `FORWARD_WEBHOOK_URL` target endpoint Laravel
- `LAST_SYNC_FILE` default `last_checkin_time.txt`
- `DEVICE_CONNECT_TIMEOUT` default `3`
- `DEVICE_READ_TIMEOUT` default `20`
- `DEVICE_RETRIES` default `2`
- `DEVICE_RETRY_BACKOFF` default `2`
- `SUCCESS_ONLY` default `true`
- `SUCCESS_FIELD_CANDIDATES` daftar field status dari database device yang dicek sebagai indikator sukses
- `SUCCESS_VALUES` daftar nilai yang dianggap sukses
- `FAILURE_VALUES` daftar nilai yang dianggap gagal
- `FINAL_ERROR_STATUS_CODES` status HTTP yang dianggap final sehingga checkpoint tetap maju dan data tidak dikirim ulang