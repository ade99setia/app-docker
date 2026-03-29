<?php

// ==========================================
// 1. KONFIGURASI API EVOLUTION
// ==========================================
$baseUrl      = "http://localhost:8080"; 

// Ini nama Instance Anda di Dashboard (bukan nomor WA pengirim)
$instanceName = trim("ade-setia"); 

// Global API Key yang ada di docker-compose.yml
$apiKey       = trim("KunciRahasiaSaya999");


// ==========================================
// 2. DATA PESAN YANG AKAN DIKIRIM
// ==========================================
$data = [
    "number"      => "6285728473920", // Nomor tujuan (harus pakai 62)
    "text"        => "Halo! Ini adalah pesan otomatis dari script PHP lokal saya. Gateway WhatsApp berhasil jalan 100%!",
    "delay"       => 1200,            // Jeda pengetikan 1.2 detik biar natural
    "linkPreview" => true             // Munculkan preview jika ada link di dalam teks
];


// ==========================================
// 3. PROSES PENGIRIMAN (cURL)
// ==========================================
// Menggabungkan URL dengan aman
$url = $baseUrl . "/message/sendText/" . urlencode($instanceName);

// Mulai sesi cURL
$ch = curl_init();

// Ubah array data menjadi format JSON
$payload = json_encode($data);

// Setting cURL
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json",
    "apikey: $apiKey"
]);

// Eksekusi cURL dan tangkap responnya
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

// ==========================================
// 4. CEK HASIL
// ==========================================
if (curl_errno($ch)) {
    echo "Gagal ngirim! Error cURL: " . curl_error($ch) . "\n";
} else {
    echo "====================================\n";
    echo "Status HTTP: $httpCode \n";
    echo "====================================\n";
    
    if ($httpCode == 201 || $httpCode == 200) {
        echo "✅ BERHASIL! Pesan sudah terkirim ke WhatsApp.\n";
    } else {
        echo "❌ GAGAL! Ada yang salah. Respon dari server:\n";
    }
    
    // Tampilkan detail respon dari server Evolution
    echo $response . "\n";
}

// Tutup sesi cURL
curl_close($ch);

?>