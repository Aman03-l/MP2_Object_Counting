# MP2_Object_Counting

## Identitas Mahasiswa
- **Nama**: Salman Al Ghifary
- **NRP**: 5024221003

## Hasil Deteksi
Berdasarkan pengujian program pada citra `parking.jpg`, program yang dibuat mendeteksi sebanyak:
**35 Mobil**

---

## Penjelasan Pipeline
Pendekatan yang digunakan pada program ini adalah **Threshold-based** yang dikombinasikan dengan **Morphological Operations** (Operasi Morfologi). Langkah-langkahnya adalah sebagai berikut:

1. **Preprocessing (Grayscale & Blur):**
   Citra asli dikonversi menjadi Grayscale untuk menghilangkan informasi warna yang tidak diperlukan. Kemudian, diterapkan Gaussian Blur dengan ukuran kernel `(5,5)` untuk mengurangi *noise* pada tekstur aspal agar tidak mengganggu proses thresholding.

2. **Adaptive Thresholding:**
   Fungsi `cv2.adaptiveThreshold` digunakan dengan metode `ADAPTIVE_THRESH_GAUSSIAN_C`, `blockSize = 31`, dan `C = 5`. 
   - **Alasan:** Karena intensitas cahaya pada gambar parkir tidak merata (ada yang terang dan gelap), threshold biasa tidak akan bekerja. *Adaptive Threshold* menghitung ambang batas berdasarkan rata-rata piksel di sekitar lokal, sehingga mampu memisahkan objek (mobil) dari latar belakang (aspal) dengan sangat baik.

3. **Morphological Opening (Erosi + Dilatasi):**
   Menggunakan kernel berukuran `(35, 35)`. 
   - **Alasan:** Garis parkir pada gambar memiliki ketebalan sekitar 5-10 piksel. Dengan melakukan Erosi menggunakan kernel 35x35, seluruh garis parkir putih yang tipis tersebut **terhapus total**, menyisakan hanya blok-blok besar milik mobil. Dilatasi setelahnya berfungsi mengembalikan ukuran mobil yang sempat mengecil.

4. **Morphological Closing (Dilatasi + Erosi):**
   Menggunakan kernel elips berukuran `(25, 25)`. 
   - **Alasan:** Proses thresholding seringkali memecah sebuah mobil (terutama bagian atap, kap mesin, dan bemper) menjadi potongan-potongan terpisah. Closing berfungsi untuk menggabungkan potongan-potongan tersebut menjadi satu gumpalan utuh.

5. **Contour Detection & Filtering:**
   `cv2.findContours` digunakan untuk menemukan semua kontur pada citra biner hasil morfologi. Selanjutnya, kontur disaring berdasarkan:
   - **Area:** Hanya kontur dengan luas antara `14.000` hingga `60.000 piksel` yang dianggap sebagai mobil. Ini membuang *noise* kecil atau gumpalan raksasa hasil penggabungan.
   - **Aspect Ratio:** Rasio lebar/tinggi antara `0.5` hingga `3.5`. Ini memastikan hanya bentuk persegi panjang yang proporsional yang dihitung.

---

## Visualisasi Tahapan
Visualisasi 4 tahapan dihasilkan secara otomatis saat program dijalankan:

1. **Citra Asli (RGB):** Gambar aerial parkir.
2. **Adaptive Threshold:** Aspal menjadi hitam, sedangkan semua mobil dan garis parkir berwarna putih.
3. **Morphological Operation:** Garis parkir putih sudah hilang (karena Opening 35x35), dan blok-blok mobil terlihat jelas.
4. **Hasil Akhir:** Semua mobil yang lolos filter ditandai dengan *Green Bounding Box*.

---

## Analisis dan Evaluasi

### Kendala yang Dihadapi
1. **Warna Mobil yang Sangat Gelap/Hitam:**
   Mobil berwarna hitam memiliki intensitas cahaya yang hampir mendekati warna bayangan aspal. Pada proses thresholding, atap dan bagian bawah mobil hitam sering terbelah menjadi 2 kontur yang berbeda.
2. **Keterbatasan Ukuran Kernel Closing:**
   Pada pipeline yang digunakan, kernel `(25, 25)` untuk Closing belum cukup besar untuk merekatkan sepenuhnya bagian-bagian mobil hitam yang terbelah tersebut. Alhasil, beberapa mobil hitam dihitung menjadi 2 objek terpisah.

### Akurasi
Secara visual, jumlah mobil sebenarnya pada gambar adalah **29 mobil** (14 kiri, 14 kanan, 1 merah tengah). Program ini mendeteksi **35 mobil**.
- **Kelebihan:** Program sangat sensitif dan berhasil mendeteksi semua mobil putih, merah, dan perak dengan sempurna tanpa ada yang terlewat.
- **Kekurangan:** Terjadi *Overcounting* (kelebihan hitung) karena beberapa mobil hitam terpecah menjadi 2 atau 3 bagian saat diproses.
