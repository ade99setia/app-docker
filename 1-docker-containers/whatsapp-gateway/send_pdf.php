<?php

// 1. KONFIGURASI
$baseUrl      = "http://localhost:8080"; 
$instanceName = trim("ade-setia"); 
$apiKey       = trim("KunciRahasiaSaya999");
$tujuan       = "6285728473920";

// 2. BACA FILE PDF LOKAL & UBAH KE BASE64
$filePdf = 'invoice_001.pdf'; // Pastikan ada file ini di folder yang sama!

if (!file_exists($filePdf)) {
    die("Error: File dokumen '$filePdf' tidak ditemukan!\n");
}

$dataMedia = base64_encode(file_get_contents($filePdf));

// 3. DATA PESAN (Format khusus Dokumen)
$data = [
    "number"    => $tujuan,
    "mediatype" => "document",         // Wajib diisi 'document'
    "mimetype"  => "application/pdf",  // Standar tipe file PDF
    "caption"   => "Halo! Berikut saya lampirkan dokumen Invoice Anda 📄", // Caption seringkali tidak muncul di PDF, tergantung versi WA
    "media"     => $dataMedia,
    "fileName"  => "Invoice_Pembelian.pdf" // Nama file saat diterima di WA
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
    echo $httpCode == 201 ? "✅ Dokumen PDF terkirim!\n" : "❌ Gagal kirim PDF\n";
}

curl_close($ch);
?>