# 🛡️ Econo Shield: Bankruptcy Predictor

**Econo Shield** adalah aplikasi berbasis web yang dirancang untuk menganalisis kesehatan keuangan individu, memprediksi skor risiko finansial, dan menghitung persentase probabilitas kebangkrutan berdasarkan beberapa parameter indikator keuangan. 

Aplikasi ini mendukung input data secara manual maupun impor data masal menggunakan berkas dokumen spreadsheet.

---

## 🚀 Daftar Library & Dependensi yang Digunakan

Proyek ini dibangun menggunakan bahasa pemrograman **Python 3.x** dengan ekosistem pustaka berikut:

1.  **Streamlit (`streamlit`)**
    * **Kegunaan:** Framework utama untuk membangun antarmuka web (UI) interaktif secara cepat tanpa memerlukan kompilasi HTML/CSS/JS terpisah.
2.  **Pandas (`pandas`)**
    * **Kegunaan:** Manipulasi dan analisis struktur data berbentuk DataFrame. Digunakan untuk membersihkan data hasil pembacaan berkas Excel serta konversi tipe data dari basis data.
3.  **Plotly Express (`plotly`)**
    * **Kegunaan:** Membuat visualisasi grafik interaktif (grafik batang perbandingan aset-utang dan diagram lingkaran distribusi risiko) pada menu Dashboard dan Prediksi.
4.  **OpenPyXL (`openpyxl`)** *(Diperlukan di balik layar oleh Pandas)*
    * **Kegunaan:** Engine pembaca dan pemroses mesin (*engine*) berkas Excel (`.xlsx`) saat pengguna menggunakan fitur menu "Upload Data".
5.  **SQLite3 (`sqlite3`)** *(Pustaka bawaan Python)*
    * **Kegunaan:** Mesin basis data relasional (*relational database*) lokal bertipe *serverless* yang digunakan untuk menyimpan catatan finansial secara permanen di berkas `database.db`.

---

## 📊 Struktur Arsitektur Data

Aplikasi ini menggunakan tabel tunggal pada SQLite bernama `financial_data` dengan pemetaan kolom sebagai berikut:

| Nama Kolom di DB | Tipe Data | Keterangan di Aplikasi |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto Increment) |
| `name` | TEXT | Nama Individu / Nasabah |
| `income` | REAL | Pemasukan Bulanan |
| `expense` | REAL | Pengeluaran Bulanan |
| `assets` | REAL | Total Nilai Aset |
| `liabilities` | REAL | Total Nilai Hutang |
| `savings` | REAL | Total Nilai Tabungan |

---

## 🧠 Logika & Aturan Perhitungan Skor Risiko

Skor Risiko Finansial dihitung menggunakan fungsi `calculate_risk_score()` dengan akumulasi batas nilai maksimal sebesar **100%**. Aturan kalkulasi penalti poinnya adalah sebagai berikut:

1.  **Kondisi Profitabilitas (Maksimal +30 Poin):**
    * Jika $\text{Pemasukan} - \text{Pengeluaran} < 0$ (Kondisi Minus/Defisit) $\rightarrow$ **+30 Poin**.
2.  **Kondisi Rasio Utang Terhadap Aset / Debt Ratio (Maksimal +40 Poin):**
    * Jika $\text{Hutang} / \text{Aset} > 0.8$ $\rightarrow$ **+40 Poin**.
    * Jika $\text{Hutang} / \text{Aset} > 0.5$ sampai $0.8$ $\rightarrow$ **+20 Poin**.
3.  **Kondisi Tabungan (Maksimal +30 Poin):**
    * Jika $\text{Tabungan} \le 0$ $\rightarrow$ **+30 Poin**.

### Klasifikasi Kategori Risiko:
* 🟢 **Rendah:** Skor $< 30\%$
* 🟡 **Sedang:** Skor $30\% - 59\%$
* 🔴 **Tinggi:** Skor $\ge 60\%$

---

## 🛠️ Cara Instalasi dan Menjalankan Aplikasi

### 1. Kloning Repositori
```bash
git clone ([https://github.com/donsanderr-cmyk/Dashbord_Finance.git])
cd econoshield-app
