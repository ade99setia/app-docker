# Panduan Client IoT Face Scan

## Ringkasan

Dokumen ini menjelaskan kondisi alat IoT Face Scan yang digunakan, keterbatasan bawaan dari perangkat, serta pengembangan tambahan yang sudah dibuat agar proses pengelolaan data dan sinkronisasi ke sistem menjadi lebih mudah, lebih aman, dan lebih fleksibel.

Secara singkat, perangkat IoT Face Scan ini tetap memiliki keterbatasan bawaan dari sisi perangkat keras dan firmware. Namun di sisi lain, perangkat ini sudah dikembangkan dengan bantuan sistem Python tambahan sehingga alur kerja operasional menjadi jauh lebih baik dibanding penggunaan standar dari alat saja.

## Kondisi Awal Alat

Sebelum dikembangkan, alat memiliki karakteristik sebagai berikut:

- Penambahan data wajah atau data personil cenderung dilakukan langsung dari alat, sehingga proses input awal menjadi lambat dan manual.
- Pengelolaan data dalam jumlah banyak kurang efisien jika hanya mengandalkan layar dan menu perangkat.
- Webhook atau notifikasi dari alat hanya memberi tahu bahwa perangkat aktif atau ada aktivitas scan.
- Notifikasi bawaan tidak langsung memberikan detail lengkap siapa yang scan dalam format yang siap dipakai sistem aplikasi.
- Untuk mendapatkan data scan yang benar-benar lengkap, sistem tetap perlu mengambil data log dari database perangkat.

Kesimpulannya, perangkat tetap bisa dipakai secara mandiri, tetapi pengalaman operasionalnya terbatas jika tidak dibantu sistem tambahan.

## Pengembangan Yang Sudah Ditambahkan

Di dalam folder proyek ini sudah dibuat beberapa alat bantu berbasis Python untuk menutupi kekurangan bawaan dari perangkat.

Pengembangan utamanya meliputi:

- Template input data personil agar proses pendaftaran awal tidak lagi harus dilakukan satu per satu dari perangkat.
- Script upload massal data personil ke perangkat.
- Script pengolahan foto agar file lebih sesuai dengan kebutuhan perangkat.
- Sistem sinkronisasi data scan dari perangkat ke aplikasi Laravel.
- Dua mode sinkronisasi data: realtime dan polling setiap 5 menit.
- Integrasi penuh ke platform `idnsolo.com` untuk pengaturan presensi, pemantauan, dan rekap data.

## Manfaat Pengembangan Ini

Dengan pengembangan tambahan, alat menjadi lebih layak dipakai dalam operasional harian karena:

- Proses pendaftaran awal jauh lebih cepat.
- Data bisa disiapkan dari laptop atau komputer kerja.
- Foto bisa dirapikan lebih dulu sebelum dikirim ke alat.
- Sistem aplikasi tidak lagi hanya menerima notifikasi kosong, tetapi bisa menerima data scan hasil sinkronisasi database perangkat.
- Tersedia dua strategi sinkronisasi sesuai kebutuhan beban sistem dan kestabilan jaringan.
- Pengaturan jadwal presensi tidak perlu dilakukan dari layar alat yang kecil dan manual.
- Semua proses bisa dipusatkan dalam satu platform kerja, yaitu `idnsolo.com`.

## Integrasi Dengan Platform idnsolo.com

Pengembangan ini tidak berdiri sendiri. Sistem IoT Face Scan sekarang sudah terintegrasi dengan platform `idnsolo.com`, sehingga pengelolaan presensi tidak lagi bergantung pada menu bawaan alat.

Integrasi yang sudah tersedia meliputi:

- halaman pengaturan aturan presensi
- halaman rekap attendance titles
- endpoint scan dan rekap yang terhubung ke aplikasi
- sinkronisasi data scan dari IoT Face Scan ke sistem pusat
- pemrosesan data presensi dalam satu alur kerja yang sama dengan fitur lain di platform

Artinya, alat IoT tidak lagi diposisikan sebagai sistem yang berdiri sendiri, tetapi sebagai bagian dari ekosistem aplikasi `idnsolo.com`.

## Keuntungan Integrasi Dengan idnsolo.com

Dengan integrasi ini, client mendapatkan keuntungan yang jauh lebih besar dibanding memakai alat tanpa pengembangan tambahan.

Keuntungan utamanya:

- pengaturan presensi dilakukan dari web admin, bukan dari layar alat
- data lebih mudah dipantau dan direkap dari sistem pusat
- aturan presensi bisa dibuat lebih fleksibel sesuai kebutuhan kegiatan
- sinkronisasi scan langsung masuk ke alur sistem yang sama dengan fitur lain di `idnsolo.com`
- operator tidak perlu bolak-balik mengatur perangkat secara manual

## Pengaturan Jadwal Presensi Dari Web

Salah satu kelebihan terbesar dari pengembangan ini adalah kemampuan membuat berbagai aturan atau jadwal presensi sendiri dari sistem web.

Sekarang client dapat membuat aturan presensi langsung dari panel `idnsolo.com` tanpa harus menyentuh pengaturan detail dari alat IoT satu per satu.

Contoh penggunaan yang bisa dibuat:

- jadwal presensi masuk sekolah
- jadwal presensi pulang
- jadwal sholat pada jam tertentu
- jadwal pengambilan makan
- jadwal kegiatan khusus harian
- jadwal kegiatan tertentu berdasarkan hari dan jam

Keunggulan pendekatan ini:

- lebih cepat dibanding setting manual di alat
- tidak terganggu keterbatasan layar perangkat yang kecil
- lebih mudah diubah bila ada perubahan kebutuhan
- bisa dibuat banyak skenario sesuai kebutuhan operasional
- aturan dapat dikelola dari satu tempat oleh admin sistem

## Fleksibilitas Aturan Presensi

Aturan presensi yang sudah terintegrasi ke `idnsolo.com` bukan hanya sekadar on atau off. Pengaturannya jauh lebih fleksibel.

Secara konsep, sistem sudah mendukung pengaturan seperti:

- nama title atau nama kegiatan presensi
- deskripsi kegiatan
- hari aktif
- jam mulai
- jam selesai
- jeda minimal untuk presensi kedua atau checkout
- urutan prioritas aturan
- beberapa rentang tanggal aktif
- status aktif atau nonaktif aturan

Dengan model ini, client bisa membuat banyak aturan presensi berbeda tanpa perlu ketergantungan langsung pada menu bawaan perangkat IoT.

## Scan Tidak Harus Dari Alat IoT Saja

Keuntungan lain yang sangat penting adalah proses scan sekarang tidak harus dipahami sebagai aktivitas yang hanya bisa hidup di perangkat IoT Face Scan saja.

Karena sistem sudah benar-benar terintegrasi dengan `idnsolo.com`, proses scan juga bisa dilakukan melalui device yang dapat membuka web, sesuai fitur yang sudah dibuat sebelumnya dalam platform.

Artinya, dalam implementasi tertentu:

- operator dapat membuka halaman terkait dari browser
- proses scan dapat memanfaatkan device yang mendukung akses web
- rekap dan pemantauan tetap masuk ke platform yang sama
- hasil akhirnya tetap terpusat di `idnsolo.com`

Ini memberi nilai tambah besar karena operasional tidak sepenuhnya terkunci pada satu perangkat fisik saja.

## Satu Platform, Banyak Kebutuhan

Dengan pendekatan yang sekarang, `idnsolo.com` menjadi pusat operasional utama.

Fungsinya tidak hanya menerima data dari alat, tetapi juga menjadi tempat untuk:

- mengatur title presensi
- melihat title yang aktif saat ini
- melihat rekap attendance
- menjalankan proses scan yang terintegrasi
- menyatukan data hasil presensi dengan fitur sistem lainnya

Bagi client, ini jauh lebih menguntungkan karena operasional menjadi lebih tertata dan tidak bergantung pada menu alat yang terbatas.

## Fitur Input Data Personil Yang Lebih Mudah

Untuk proses pendaftaran awal, sekarang tersedia pendekatan yang lebih praktis dibanding input manual dari alat.

Komponen yang sudah tersedia:

- Template Excel untuk data siswa.
- Template Excel untuk data guru.
- Folder foto personil.
- Script upload data ke perangkat.
- Script konversi dan kompres foto agar file lebih sesuai dengan perangkat.

Folder yang digunakan:

- `insertEmployee/data_students.xlsx`
- `insertEmployee/data_teachers.xlsx`
- `insertEmployee/student_photos/`
- `insertEmployee/teacher_photos/`
- `insertEmployee/staf_photos/`
- `insertEmployee/upload_script.py`
- `insertEmployee/convert_photo.py`

Dengan alur ini, operator tidak perlu memasukkan data satu per satu langsung melalui layar perangkat. Data bisa disiapkan lebih dulu dalam bentuk template, lalu diunggah dengan proses yang lebih cepat dan lebih konsisten.

Nilai tambahnya bukan hanya cepat, tetapi juga membuat perangkat lebih mudah diintegrasikan ke alur kerja administrasi yang sudah berjalan di `idnsolo.com`.

## Cara Kerja Upload Data Awal

Secara umum, alurnya sebagai berikut:

1. Siapkan data personil pada file template Excel.
2. Siapkan foto sesuai nama file yang dicantumkan di template.
3. Jika perlu, rapikan atau kompres foto menggunakan script konversi.
4. Jalankan script upload agar data personil dikirim ke perangkat IoT Face Scan.

Manfaat dari alur ini:

- mengurangi kesalahan input manual
- mempercepat proses pendaftaran awal
- memudahkan pengelolaan data dalam jumlah banyak
- memudahkan revisi data bila ada perubahan

## Cara Kerja Sinkronisasi Scan

Perlu dipahami bahwa perangkat IoT Face Scan tidak langsung mengirim data scan lengkap ke aplikasi dalam format yang siap dipakai. Karena itu, sistem Python dibuat untuk mengambil data log dari perangkat, lalu mengirimkannya ke aplikasi.

Tujuan utamanya adalah memastikan aplikasi menerima data scan yang lebih lengkap dan lebih berguna dibanding hanya notifikasi bahwa perangkat sedang aktif.

Endpoint tujuan aplikasi saat ini adalah:

- `https://idnsolo.com/api/iot/face-scan/auth/3/lFFkMi04oXwuAETrQwVEbQBjMqNuY3hZuWXTD4YGa0d0ee7f`

## Dua Mode Sinkronisasi

Sistem mendukung dua mode sinkronisasi.

### 1. Mode Realtime

Mode realtime digunakan ketika perangkat mengirim trigger ke jaringan lokal bahwa ada aktivitas scan atau perangkat aktif.

Alurnya:

1. IoT Face Scan mengirim notifikasi singkat ke endpoint lokal.
2. Python menerima trigger tersebut.
3. Python mengambil database log dari perangkat.
4. Python membaca data scan terbaru yang valid.
5. Python mengirim hasilnya ke aplikasi.

Kelebihan mode realtime:

- respons lebih cepat
- cocok untuk kebutuhan monitoring yang lebih dekat ke waktu sebenarnya
- aplikasi tidak perlu menunggu interval lama untuk menerima data baru
- cocok untuk kebutuhan kegiatan yang ingin segera tercatat di platform pusat

Kekurangan mode realtime:

- perangkat bisa mengirim trigger berkali-kali
- jaringan lokal harus stabil
- butuh proses Python yang selalu aktif

Catatan penting:

- trigger dari perangkat bukan data scan final
- trigger hanya menjadi pemicu agar Python mengambil log dari database perangkat

### 2. Mode Polling Setiap 5 Menit

Mode polling digunakan ketika sistem ingin lebih ringan dan tidak ingin bergantung pada trigger dari perangkat.

Alurnya:

1. Python berjalan mandiri.
2. Setiap 5 menit Python memeriksa database perangkat.
3. Python mengambil data scan baru yang valid.
4. Python mengirim hasilnya ke aplikasi.

Kelebihan mode polling:

- lebih ringan untuk operasional
- tidak bergantung pada trigger webhook dari alat
- lebih sederhana untuk dijaga stabilitasnya
- cocok untuk kondisi jaringan yang tidak selalu ideal
- cocok untuk kebutuhan operasional yang lebih tenang dan efisien

Kekurangan mode polling:

- data tidak langsung masuk detik itu juga
- ada jeda sesuai interval yang ditentukan

Kesimpulan praktis:

- jika ingin respons lebih cepat, gunakan realtime
- jika ingin lebih stabil dan lebih ringan, gunakan polling 5 menit

## Penyaringan Data Yang Dikirim

Sistem Python juga sudah ditingkatkan agar tidak semua catatan dari alat langsung dikirim begitu saja.

Perilaku yang sudah diterapkan:

- sistem berusaha memfilter hanya data yang dianggap valid atau berhasil
- data yang dianggap gagal tidak diprioritaskan untuk dikirim
- jika aplikasi memberikan respons final tertentu seperti data sudah tidak perlu diproses ulang, sistem tidak akan terus mengirim data yang sama

Tujuannya adalah mengurangi pengiriman berulang yang tidak perlu dan menjaga log sistem tetap lebih bersih.

## Kelebihan Solusi Yang Sudah Dikembangkan

Setelah dikembangkan dengan Python, sistem ini memiliki kelebihan berikut:

- pengelolaan data awal lebih mudah karena sudah tersedia template
- upload data personil menjadi lebih cepat dibanding input manual dari alat
- foto dapat diproses lebih dulu agar lebih sesuai dengan kebutuhan perangkat
- sinkronisasi data ke aplikasi menjadi lebih fleksibel
- ada pilihan mode realtime atau polling 5 menit
- sistem dapat menyimpan checkpoint agar tidak selalu mengirim data lama berulang kali
- integrasi ke aplikasi Laravel menjadi lebih rapi
- aturan presensi bisa dibuat langsung dari web sesuai kebutuhan client
- sistem lebih mudah dipakai untuk banyak skenario kegiatan, tidak hanya satu jenis presensi
- operasional lebih nyaman karena tidak perlu banyak setting langsung di alat
- scan dan pemantauan bisa dipusatkan dalam satu platform `idnsolo.com`

## Keterbatasan Yang Tetap Ada

Walaupun sudah dikembangkan, ada beberapa keterbatasan yang tetap perlu dipahami oleh client:

- perangkat asli tetap memiliki batasan dari firmware dan API bawaan
- kualitas sinkronisasi tetap bergantung pada kestabilan jaringan lokal
- jika perangkat tidak dapat dijangkau, Python tidak bisa mengambil database log
- akurasi dan kelengkapan data tetap dipengaruhi oleh data yang disimpan oleh perangkat itu sendiri
- mode realtime tetap membutuhkan proses Python yang aktif terus di jaringan lokal

Dengan kata lain, pengembangan Python ini sangat membantu, tetapi tidak mengubah keterbatasan dasar dari alat secara total.

## Rekomendasi Pemakaian

Untuk penggunaan operasional, pendekatan yang disarankan adalah:

- gunakan template Excel untuk pendaftaran awal data personil
- gunakan script upload agar input data tidak manual dari alat
- gunakan mode realtime jika ingin data lebih cepat masuk
- gunakan mode polling 5 menit jika ingin sistem lebih ringan dan stabil
- gunakan panel `idnsolo.com` untuk mengatur title dan aturan presensi
- pastikan perangkat dan komputer Python berada di jaringan lokal yang sama

## Penutup

Perangkat IoT Face Scan ini pada dasarnya memiliki keterbatasan jika digunakan apa adanya. Namun setelah dikembangkan dengan sistem Python tambahan, alat ini menjadi jauh lebih siap digunakan dalam operasional nyata.

Nilai tambah utama dari pengembangan ini bukan pada mengubah perangkat menjadi alat baru, melainkan pada membuat perangkat yang ada menjadi lebih mudah dikelola, lebih fleksibel, dan lebih terintegrasi dengan sistem aplikasi.

Jika dilihat dari sisi client, poin pentingnya adalah:

- alat tetap memiliki kekurangan bawaan
- proses manual sudah banyak dipermudah
- sinkronisasi data sudah lebih baik
- tersedia pilihan mode kerja sesuai kebutuhan operasional
- jadwal presensi bisa dibuat sendiri dari web tanpa mengatur manual di alat
- scan dan pengelolaan presensi sudah benar-benar masuk ke satu platform yaitu `idnsolo.com`
- sistem sekarang lebih layak dipakai untuk kebutuhan riil di lapangan