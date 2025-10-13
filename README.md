# Analisis Pertandingan Tenis WTA & Dashboard Prediktabilitas Odds

![WTA Dashboard Preview](wta-dashboard.png)

### ► [Link ke Dashboard Interaktif ([(https://drive.google.com/file/d/1oN-kCm_NKus6WUjQYlcA-1yjQF2bkxat/view?usp=drive_link))]()

---


Proyek ini merupakan analisis data end-to-end yang menyelami lebih dari **42,000 pertandingan** tenis putri (WTA) dari tahun 2006 hingga 2025. Tujuan utamanya adalah untuk menemukan pola dan tren dalam distribusi pertandingan, performa pemain, serta menganalisis secara mendalam akurasi prediksi *bookmaker* berdasarkan *odds* yang diberikan.

Hasil analisis divisualisasikan dalam sebuah dashboard Power BI interaktif yang terdiri dari dua halaman utama: **Gambaran Umum Pertandingan** dan **Analisis Prediktabilitas Odds**.

---

## Dataset

Dataset yang digunakan dalam proyek ini bersumber dari [**Kaggle**]. Dataset ini mencakup informasi detail untuk setiap pertandingan, termasuk:
- Informasi turnamen (nama, tanggal, jenis lapangan).
- Informasi pemain (pemenang dan yang kalah).
- Statistik pertandingan (jumlah set).
- Data betting odds dari berbagai *bookmaker*.

---

## Metodologi & Teknologi

1.  **Data Wrangling & EDA (Exploratory Data Analysis):** Proses pembersihan, transformasi, dan analisis eksplorasi data awal dilakukan menggunakan **Python** dengan library **Pandas** dan **NumPy**.
2.  **Visualisasi Data & Dashboarding:** Data yang telah diproses kemudian dimuat ke **Power BI** untuk pembuatan model data dan visualisasi interaktif.

---

## Analisis Mendalam Dashboard

Dashboard ini terbagi menjadi dua bagian analisis utama:

### 1. Halaman: WTA Matches Overview (2006–2025)
Halaman ini memberikan gambaran umum tentang lanskap turnamen WTA.

**KPI Utama:**
- **Total Pertandingan:** 42,815
- **Pemain Unik:** 2,148
- **Rata-rata Set per Pertandingan:** 2.33
- **Tingkat Kemenangan Tak Terduga (Upset Rate):** 34.8%

**Visualisasi Kunci:**
- **Tren Pertandingan & Upset Rate Tahunan:** Menunjukkan fluktuasi jumlah pertandingan dan tingkat *upset* dari tahun ke tahun.
- **Top 10 Pemain dengan Kemenangan Terbanyak:** Mengidentifikasi pemain paling dominan dalam dataset, dipimpin oleh Wozniacki (588 kemenangan).
- **Distribusi Pertandingan per Babak:** Menunjukkan bahwa hampir setengah (47.3%) dari semua pertandingan terjadi di babak pertama.
- **Distribusi Pertandingan per Jenis Lapangan:** Menyoroti dominasi lapangan **Hard Court** (26K pertandingan) dibandingkan dengan Clay (12K) dan Grass (5K).

### 2. Halaman: Predictability of Matches by Odds
Halaman ini fokus menganalisis seberapa akurat *odds* dari *bookmaker* dalam memprediksi hasil pertandingan.

**KPI Utama:**
- **Akurasi Odds Keseluruhan:** 49.70% (hampir seperti lemparan koin).
- **Rata-rata Selisih Odds (Odds Gap):** 50%
- **Total Upset:** 34.8% dari pertandingan dimenangkan oleh pemain yang tidak diunggulkan.

**Visualisasi Kunci:**
- **Tren Akurasi Odds Tahunan:** Menunjukkan bagaimana akurasi *bookmaker* berfluktuasi sepanjang waktu, umumnya berada di antara 40-55%.
- **Akurasi Odds per Jenis Lapangan:** Memberikan wawasan bahwa prediksi paling akurat terjadi di lapangan **Greenset (59%)** dan paling tidak akurat di lapangan **Carpet (47%)**.
- **Hubungan Odds Gap vs Prediksi Benar:** Mengkonfirmasi hipotesis bahwa semakin besar selisih *odds* antara pemain, semakin tinggi kemungkinan prediksi *bookmaker* benar.
- **Matriks Akurasi per Babak dan Lapangan:** Menyediakan analisis granular yang menunjukkan bagaimana akurasi bervariasi tergantung pada kombinasi babak turnamen dan jenis lapangan.

---

## Temuan & Wawasan Kunci (Key Insights)

- **Prediksi Bookmaker Tidak Selalu Akurat:** Dengan akurasi hanya **49.70%**, *odds* tidak bisa dijadikan satu-satunya patokan untuk hasil pertandingan.
- **Upset adalah Hal yang Umum:** Lebih dari sepertiga (34.8%) pertandingan berakhir dengan kemenangan pemain yang tidak diunggulkan, menunjukkan tingkat kompetisi yang tinggi di WTA Tour.
- **Spesialisasi Lapangan itu Nyata:** Dominasi pertandingan di Hard Court menunjukkan pentingnya kemampuan bermain di permukaan ini. Selain itu, akurasi *odds* yang berbeda-beda antar jenis lapangan menandakan adanya variabel performa yang unik di setiap permukaan.
- **Pemain Dominan:** Terdapat sekelompok kecil pemain seperti Wozniacki, Azarenka, dan Serena Williams yang secara konsisten memenangkan pertandingan dalam jumlah besar selama periode waktu ini.
