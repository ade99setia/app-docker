
---

## 🏗️ Arsitektur Container
Setup ini menggunakan 4 container yang saling terhubung dalam satu network (`app_network_idn_solo`):
1. **`idn_solo_app_dev`**: Mesin utama (PHP 8.3 FPM) tempat kode Laravel berjalan.
2. **`idn_solo_vite`**: Mesin Node.js untuk melakukan kompilasi aset (CSS/JS) secara *real-time* dengan Vite.
3. **`idn_solo_web_dev`**: Server Nginx sebagai pintu masuk utama yang menerima *request* dari browser.
4. **`idn_solo_db_dev`**: Database MySQL 8.0.

---

## 📄 1. Konfigurasi Dockerfile (`Dockerfile.dev`)
**Fungsi:** Membuat *image* kustom untuk PHP-FPM dengan menginstall semua ekstensi yang dibutuhkan Laravel (seperti PDO, GD, Zip) dan menyertakan Composer.

```dockerfile
# Dockerfile.dev
FROM php:8.3-fpm-alpine

# Install sistem dependencies
RUN apk add --no-cache \
    bash curl git libpng-dev libzip-dev icu-dev libxml2-dev \
    zlib-dev oniguruma-dev mariadb-connector-c-dev make autoconf g++ gcc musl-dev

# PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql intl zip gd

# Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

EXPOSE 9000
CMD ["php-fpm"]
```

---

## 📄 2. Orkestrasi Container (`docker-compose.dev.yml`)
**Fungsi:** Merangkai ke-4 container agar bisa berjalan bersamaan. 

*(⚠️ **Catatan Penting:** Saya sudah **memperbaiki** bagian volumes Nginx di bawah ini menjadi `default.conf` agar masalah 404 tidak terulang lagi).*

```yaml
services:
  # =========================
  # App: PHP-FPM Laravel (Dev)
  # =========================
  app_idn_solo_dev:
    build:
      context: .
      dockerfile: Dockerfile.dev # Gunakan Dockerfile dev
    container_name: idn_solo_app_dev
    env_file:
      - ./.env
    volumes:
      - .:/var/www/html # BIND MOUNT: Folder saat ini disambung langsung ke dalam docker
    networks:
      - app_network_idn_solo

  # =========================
  # Vite / Node (Untuk npm run dev)
  # =========================
  vite_idn_solo:
    image: node:20-alpine
    container_name: idn_solo_vite
    working_dir: /var/www/html
    volumes:
      - .:/var/www/html
    ports:
      - "5173:5173" # Port default Vite
    # Otomatis install NPM dan jalankan Vite saat container up
    command: sh -c "npm install && npm run dev"
    networks:
      - app_network_idn_solo

  # =========================
  # Web: Nginx
  # =========================
  web_idn_solo_dev:
    image: nginx:alpine
    container_name: idn_solo_web_dev
    ports:
      - "18084:80"  # Akses web di port 5 digit (http://10.159.76.115:18084)
    volumes:
      # WAJIB NAMA KANANNYA default.conf!
      - ./default.dev.conf:/etc/nginx/conf.d/default.conf
      - .:/var/www/html  # Nginx juga butuh akses ke seluruh project untuk dev
    depends_on:
      - app_idn_solo_dev
    networks:
      - app_network_idn_solo

  # =========================
  # Database: MySQL
  # =========================
  db_idn_solo_dev:
    image: mysql:8.0
    container_name: idn_solo_db_dev
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: idn_solo
      MYSQL_USER: idn_user
      MYSQL_PASSWORD: strongpassword123
    ports:
      - "3331:3306"
    volumes:
      - db_data_dev:/var/lib/mysql
    networks:
      - app_network_idn_solo

# =========================
# Networks & Volumes
# =========================
networks:
  app_network_idn_solo:
    driver: bridge

volumes:
  db_data_dev: # Cukup DB saja yang pakai named volume di dev
```

---

## 📄 3. Konfigurasi Server Web (`default.dev.conf`)
**Fungsi:** Mengatur Nginx agar mengarahkan *request* ke folder `public` Laravel dan meneruskan eksekusi file `.php` ke container `idn_solo_app_dev`.

```nginx
server {
    listen 80;
    server_name localhost;

    root /var/www/html/public;
    index index.php index.html;

    # Aktifkan Gzip agar loading web lebih ringan
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # Optimasi Assets: Serve langsung oleh Nginx & simpan di cache browser
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|otf)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
        access_log off;
    }

    location ~ \.php$ {
        include fastcgi_params;
        fastcgi_pass idn_solo_app_dev:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME /var/www/html/public$fastcgi_script_name;
        
        # Tambahan Buffer untuk kestabilan response Laravel yang berat
        fastcgi_buffer_size 128k;
        fastcgi_buffers 4 256k;
        fastcgi_busy_buffers_size 256k;
    }

    # Blokir akses ke file .env, .git, atau .ht
    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

---

## 📄 4. Konfigurasi Vite (`vite.config.ts`)
**Fungsi:** Memastikan fitur *Hot Module Replacement* (HMR) tetap berfungsi meskipun Vite berjalan di dalam Docker dan diakses dari IP WSL/Kubuntu (`10.159.76.115`).

```typescript
    server: {
        host: '0.0.0.0', // Wajib agar bisa diakses dari luar container
        port: 5173,
        cors: true,
        hmr: {
            host: '10.159.76.115', // IP Kubuntu/Server Anda
        },
    },
```

---

## 📄 5. Konfigurasi Environment Laravel (`.env`)
**Fungsi:** Menyambungkan Laravel dengan container Database. 
*Kunci utamanya adalah `DB_HOST` harus sama persis dengan nama container database di `docker-compose.dev.yml`.*

```env
# DATABASE
DB_CONNECTION=mysql
DB_HOST=db_idn_solo_dev
DB_PORT=3306
DB_DATABASE=idn_solo
DB_USERNAME=idn_user
DB_PASSWORD=strongpassword123
```

---

## 💡 Contekan Perintah Terminal (Cheat Sheet)

Biar tidak lupa, ini perintah-perintah sakti yang sering dipakai saat *development*:

| Kebutuhan | Perintah Terminal (Jalankan di server/Kubuntu) |
| :--- | :--- |
| **Nyalakan Semua Container** | `docker compose -f docker-compose.dev.yml up -d` |
| **Matikan Semua Container** | `docker compose -f docker-compose.dev.yml down` |
| **Jalankan Artisan Migrate** | `docker exec -it idn_solo_app_dev php artisan migrate` |
| **Clear Cache Laravel** | `docker exec -it idn_solo_app_dev php artisan optimize:clear` |
| **Install Paket Composer** | `docker exec -it idn_solo_app_dev composer install` |
| **Install Paket NPM** | `docker exec -it idn_solo_vite npm install` |
| **Paksa Build Vite (Jika Error)**| `docker exec -it idn_solo_vite npm run build` |
| **Lihat Log Laravel** | `docker exec -it idn_solo_app_dev tail -f storage/logs/laravel.log` |