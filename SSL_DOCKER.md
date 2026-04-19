Tentu, ini adalah versi dokumentasi yang sudah dilengkapi dengan langkah perbaikan izin akses (*permission*), konfigurasi **Vite** agar tidak *error* saat menggunakan HTTPS, serta pengaturan **Firewall** untuk akses remote via Ethernet.

---

## 🛠 Panduan Lengkap Setup HTTPS Lokal Docker (Laravel + Vite + Nginx)

Dokumentasi ini memastikan lingkungan pengembangan Anda berjalan dengan SSL yang dipercaya browser (gembok hijau), termasuk sinkronisasi dengan Vite/React.

### 1. Persiapan Host (Laptop/Remote Server)
Pastikan sistem paket dalam kondisi sehat dan `mkcert` terinstal untuk mendaftarkan Local CA.

* **Perbaiki & Install mkcert:**
    ```bash
    sudo dpkg --configure -a
    sudo apt update && sudo apt install mkcert -y
    ```
* **Install Local CA:** (Wajib agar sertifikat dianggap sah oleh browser)
    ```bash
    mkcert -install
    ```

---

### 2. Generate Sertifikat SSL (Dengan Perizinan)
Karena folder mungkin dibuat oleh sistem, pastikan user Anda memiliki hak akses penuh.

* **Setup Folder & Izin:**
    ```bash
    cd ~/development/idn-solo
    mkdir -p ssl
    sudo chown -R $USER:$USER ssl
    cd ssl
    ```
* **Generate File:** (Masukkan localhost dan IP Ethernet remote Anda)
    ```bash
    mkcert -cert-file local.crt -key-file local.key "localhost" "10.42.0.1" "127.0.0.1"
    ```

---

### 3. Konfigurasi `docker-compose.yml`
Pastikan folder `ssl` di-mount ke **Nginx** (untuk web) dan **Vite** (untuk HMR).

```yaml
  # Web: Nginx
  web_idn_solo_dev:
    image: nginx:alpine
    container_name: idn_solo_web_dev
    ports:
      - "18084:80"   # HTTP
      - "19084:443"  # HTTPS
    volumes:
      - ./default.dev.conf:/etc/nginx/conf.d/default.conf
      - .:/var/www/html
      - ./ssl:/etc/nginx/ssl
    networks:
      - app_network_idn_solo_dev

  # Vite: Node
  vite_idn_solo:
    image: node:20-alpine
    container_name: idn_solo_dev_vite
    volumes:
      - .:/var/www/html
      - ./ssl:/var/www/html/ssl # Penting untuk HTTPS Vite
    ports:
      - "5173:5173"
    command: sh -c "if [ ! -d 'node_modules' ]; then npm install; fi && npm run dev -- --host"
    networks:
      - app_network_idn_solo_dev
```

---

### 4. Konfigurasi Vite (`vite.config.js`)
Agar tidak terjadi *Mixed Content error*, Vite harus berjalan di protokol `wss` (Secure WebSocket).

```javascript
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';
import fs from 'node:fs';

export default defineConfig({
    server: {
        host: '0.0.0.0',
        port: 5173,
        https: {
            key: fs.readFileSync('./ssl/local.key'),
            cert: fs.readFileSync('./ssl/local.crt'),
        },
        hmr: {
            host: '10.42.0.1',
            protocol: 'wss', // Wajib WSS untuk HTTPS
        },
    },
    // ... plugin lainnya (laravel, react, tailwind)
});
```

---

### 5. Konfigurasi Nginx (`default.dev.conf`)
Update blok server untuk menangani SSL dan jalur sertifikat di dalam container.

```nginx
server {
    listen 443 ssl;
    server_name localhost 10.42.0.1;
    root /var/www/html/public;

    ssl_certificate /etc/nginx/ssl/local.crt;
    ssl_certificate_key /etc/nginx/ssl/local.key;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass idn_solo_app_dev:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    }
}
```

---

### 6. Pengaturan Jaringan & Firewall
Karena diakses secara remote melalui Ethernet, port harus dibuka di sisi server (Kubuntu).

* **Buka Port di UFW:**
    ```bash
    sudo ufw allow 18084/tcp
    sudo ufw allow 19084/tcp
    sudo ufw allow 5173/tcp
    sudo ufw reload
    ```

---

### 7. Aktivasi & Verifikasi
Jalankan ulang semua layanan untuk menerapkan perubahan volume dan konfigurasi.

1.  **Restart:** `docker compose down && docker compose up -d`
2.  **Akses:** [https://10.42.0.1:19084](https://10.42.0.1:19084)
3.  **Verifikasi Vite:** Buka *Inspect Element* (F12) > *Console*. Pastikan tidak ada error bertuliskan `Mixed Content` atau `WebSocket connection failed`.

---

### 💡 Penanganan Masalah (Troubleshooting)
* **Connection Timed Out:** Cek ulang IP dengan `hostname -I`. Pastikan IP Ethernet tidak berubah.
* **Permission Denied:** Jalankan `sudo chmod -R 755 ssl` untuk memastikan container bisa membaca file sertifikat.
* **Bukan Gembok Hijau:** Pastikan Anda sudah menjalankan `mkcert -install` di komputer yang **membuka browser**, bukan hanya di server remote (jika berbeda perangkat).