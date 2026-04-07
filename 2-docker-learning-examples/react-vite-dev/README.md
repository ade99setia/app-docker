# React JS + Vite

Project ini adalah contoh React JavaScript biasa yang langsung siap dipakai untuk development.

## Menjalankan langsung di lokal

```bash
npm install
npm run dev
```

Dev server akan berjalan di `http://localhost:18089`.

## Menjalankan dengan Docker

```bash
docker compose up --build
```

Kalau container sudah pernah dibuild dan mau dijalankan lagi tanpa rebuild:

```bash
docker compose up
```

Stop container:

```bash
docker compose down
```

Setup Docker ini memakai bind mount ke folder project, jadi file React bisa tetap diedit langsung dari host. `node_modules` disimpan di volume terpisah supaya tidak bentrok dengan environment Windows.

## Struktur penting

- `src/App.jsx` komponen utama
- `src/main.jsx` entry point React
- `src/App.css` styling komponen
- `src/index.css` styling global
- `vite.config.js` konfigurasi Vite dan port dev server
- `Dockerfile` image development React
- `docker-compose.yml` service Docker untuk testing React di port 18089
