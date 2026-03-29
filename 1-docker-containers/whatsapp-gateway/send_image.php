<?php

// 1. KONFIGURASI
$baseUrl      = "http://localhost:8080"; 
$instanceName = trim("ade-setia"); 
$apiKey       = trim("KunciRahasiaSaya999");
$tujuan       = "6285728473920";

// 2. BACA FILE GAMBAR LOKAL & UBAH KE BASE64
$fileGambar = 'foto_promo.jpg'; // Pastikan ada file ini di folder yang sama!

if (!file_exists($fileGambar)) {
    die("Error: File gambar '$fileGambar' tidak ditemukan!\n");
}

$tipeMime  = mime_content_type($fileGambar);
$dataMedia = base64_encode(file_get_contents($fileGambar));

// 3. DATA PESAN (Format khusus untuk Media)
$data = [
    "number"    => $tujuan,
    "mediatype" => "image",            // Wajib diisi 'image'
    "mimetype"  => $tipeMime,          // Otomatis mendeteksi image/jpeg atau image/png
    "caption"   => "Halo! Ini adalah contoh pengiriman *GAMBAR* otomatis dari PHP 🖼️",
    "media"     => $dataMedia,         // File yang sudah diubah ke Base64
    "fileName"  => "foto_promo.jpg"
];

// 4. PROSES PENGIRIMAN (cURL)
$url = $baseUrl . "/message/sendMedia/" . urlencode($instanceName);
$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json",
    "apikey: $apiKey"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if (curl_errno($ch)) {
    echo "Gagal: " . curl_error($ch) . "\n";
} else {
    echo "HTTP Code: $httpCode\n";
    echo $httpCode == 201 ? "✅ Gambar terkirim!\n" : "❌ Gagal kirim gambar\n";
}

curl_close($ch);
?>