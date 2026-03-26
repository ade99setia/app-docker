# 🗺️ Infrastruktur: Single Tunnel — Multi Project

Menggunakan **1 Cloudflare Tunnel** sebagai pintu utama untuk beberapa project Docker melalui **external network bersama**.

---

# 1️⃣ Persiapan Network (Sekali Saja)

Buat shared network:

```bash
docker network create shared_web_network
```

Network ini akan menjadi jembatan antara semua Nginx container dan Cloudflare Tunnel.

---

# 2️⃣ Konfigurasi Project (Contoh: BDN Karanganyar)

Tambahkan `shared_web_network` hanya pada **service web (nginx)**.

`~/app-docker/docker-compose.yml`

```yaml
services:
  web_app:
    image: nginx:alpine
    container_name: app_web
    ports:
      - "8081:80"
    networks:
      - app_network
      - shared_web_network # Tambahkan ini agar bisa diakses cloudflare tunnel
    restart: unless-stopped

networks:
  app_network:
    driver: bridge
  shared_web_network:  # Tambahkan ini agar bisa diakses cloudflare tunnel
    external: true
```

---

# 3️⃣ Project Pintu Utama (Cloudflare Tunnel)

Folder khusus untuk tunnel:

`~/app-docker/cloudflare-tunnel/docker-compose.yml`

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared_main
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token <TOKEN_UTAMA_KAMU> --protocol http2
    networks:
      - shared_web_network

networks:
  shared_web_network:
    external: true
```

---

# 4️⃣ Routing Cloudflare Dashboard

Konfigurasi pada **Zero Trust → Public Hostname**

| Domain                      | Service | Target Container            |
| --------------------------- | ------- | --------------------------- |
| bdn.ade-setiawan.my.id      | HTTP    | bdn_karanganyar_web:80      |
| undangan.ade-setiawan.my.id | HTTP    | undangan_pernikahan_web:80  |
| porto.ade-setiawan.my.id    | HTTP    | web_portofolio_container:80 |

Gunakan **container_name** sebagai hostname internal.

---

# 5️⃣ Arsitektur Network

```
Internet
   │
Cloudflare
   │
cloudflared_main
   │
shared_web_network
   ├── bdn_karanganyar_web
   ├── undangan_pernikahan_web
   └── web_portofolio_container
```

Database tetap aman karena berada di network internal masing-masing.

---

# 6️⃣ Keuntungan Struktur Ini

| Fitur                   | Benefit                      |
| ----------------------- | ---------------------------- |
| Single Tunnel           | Hemat RAM                    |
| External Shared Network | Routing mudah                |
| Internal Network        | DB terisolasi                |
| Modular                 | Project bisa restart sendiri |
| Single Debug Point      | Cek hanya 1 container        |

---

# 7️⃣ Debug Tunnel

Cek log:

```bash
docker logs -f cloudflared_main
```

---

# 8️⃣ Menambah Project Baru

Langkah cepat:

1. Buat project baru
2. Tambahkan network ke service web

```yaml
networks:
  - project_internal
  - shared_web_network
```

3. Jalankan

```bash
docker compose up -d
```

4. Tambahkan route di Cloudflare Dashboard

---

# 9️⃣ Ringkasan Infrastruktur

| Komponen         | Nilai              |
| ---------------- | ------------------ |
| Tunnel           | 1 container        |
| Shared Network   | shared_web_network |
| Internal Network | per project        |
| Routing          | via container name |
| Debug            | cloudflared_main   |
| Skalabilitas     | Unlimited project  |

---

# ✅ Status

* Single Tunnel aktif
* Multi Project terhubung
* Database terisolasi
* Infrastruktur hemat resource
* Siap production
