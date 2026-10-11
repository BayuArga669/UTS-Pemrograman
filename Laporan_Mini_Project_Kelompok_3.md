# LAPORAN MINI PROJECT PEMROGRAMAN DASAR (BAHASA C)

## HALAMAN SAMPUL

- **Judul Project:** Sistem Rental Film
- **Kelompok:** Kelompok 3
- **Anggota Kelompok:**
  1. NRP – Nama Mahasiswa 1 (Data Pelanggan & Film)
  2. NRP – Nama Mahasiswa 2 (Proses Sewa & Denda)
  3. NRP – Nama Mahasiswa 3 (Transaksi & Pengujian)
- **Mata Kuliah:** Pemrograman Dasar
- **Dosen Pengampu:** ........................................
- **Program Studi:** ........................................
- **Institusi:** ........................................
- **Tahun:** 2026

---

## BAB I — PENDAHULUAN

### 1.1 Latar Belakang
Proses penyewaan (rental) film secara manual membutuhkan pencatatan data pelanggan, pemilihan film yang tersedia, serta perhitungan biaya sewa dan denda keterlambatan secara terstruktur. Selain itu, pelanggan terkadang juga melakukan perpanjangan masa peminjaman sebelum film dikembalikan. Oleh karena itu, dibuat sebuah program sederhana menggunakan bahasa C untuk membantu proses transaksi rental film mulai dari validasi pilihan film hingga pencetakan bukti rental.

### 1.2 Rumusan Masalah
1. Bagaimana membuat program Sistem Rental Film menggunakan bahasa C?
2. Bagaimana melakukan input data pelanggan serta validasi pilihan dan ketersediaan film menggunakan `do-while` dan `switch-case`?
3. Bagaimana menentukan biaya sewa, perpanjangan lama peminjaman, denda keterlambatan (`Rp2000/hari`), dan status pengembalian menggunakan `if-else`?
4. Bagaimana menampilkan bukti rental lengkap serta menguji skenario peminjaman tepat waktu dan terlambat?

### 1.3 Tujuan
1. Membuat program Sistem Rental Film menggunakan bahasa C.
2. Menerapkan struktur percabangan `if`, `if-else`, dan `switch-case`.
3. Menerapkan struktur perulangan `do-while` untuk validasi input pilihan film.
4. Menghitung biaya sewa, perpanjangan waktu pinjam, dan denda keterlambatan secara tepat.
5. Mengembangkan kemampuan bekerja dalam kelompok.

### 1.4 Batasan Masalah
- Program dibuat menggunakan bahasa C (`<stdio.h>` dan `<string.h>`).
- Program **tidak menggunakan array** untuk daftar film (menggunakan konstanta `#define`).
- Program **tidak menggunakan struct** maupun konsep OOP.
- Program **tidak menggunakan pointer**.
- Struktur kontrol yang digunakan adalah `do-while`, `switch-case`, `if`, dan `if-else`.
- Data hanya disimpan selama program berjalan.

---

## BAB II — ANALISIS DAN PERANCANGAN

### 2.1 Deskripsi Sistem
Program dimulai dengan memasukkan ID pelanggan (`id`) dan nama pelanggan (`nama`), kemudian menampilkan daftar 5 film beserta biaya sewa per hari dan status ketersediaannya (`Tersedia` / `Dipinjam`). Selanjutnya pelanggan memilih nomor film (1–5) dan program memvalidasi pilihan serta stok film menggunakan `do-while` dan `switch-case`. Setelah film valid dipilih, pelanggan memasukkan lama peminjaman (`lama`), memilih apakah ingin memperpanjang peminjaman (`y/n`), dan memasukkan hari ke-berapa film dikembalikan (`hariKembali`). Program menghitung biaya sewa, mengecek keterlambatan (`hariKembali > lama`) untuk menghitung denda (`Rp2000/hari`) dan menentukan status (`Terlambat` / `Tepat waktu`), kemudian menampilkan Bukti Rental.

### 2.2 Input – Proses – Output

| Input | Proses | Output |
| :--- | :--- | :--- |
| ID pelanggan (`id`) | Validasi nomor & stok film (`do-while` & `switch`) | Daftar 5 film & status |
| Nama pelanggan (`nama`) | Menentukan judul & harga film terpilih | Konfirmasi film terpilih |
| Pilihan nomor film (`pilih`) | Menambah lama pinjam jika diperpanjang (`if`) | Data pelanggan (`id / nama`) |
| Lama peminjaman (`lama`) | Menghitung `biaya = harga * lama` | Biaya sewa (`biaya`) |
| Perpanjangan (`jawab`, `tambah`) | Mengecek `hariKembali > lama` (`if-else`) | Denda keterlambatan (`denda`) |
| Hari pengembalian (`hariKembali`) | Menghitung `denda` & `total bayar` (`biaya + denda`) | Total bayar & Status (`Tepat waktu` / `Terlambat`) |

### 2.3 Algoritma / Pseudocode

```text
Mulai
    Input id pelanggan
    Input nama pelanggan
    Tampilkan daftar 5 film beserta Biaya/Hari dan Status (Tersedia/Dipinjam)

    Ulangi (do-while !valid)
        valid = 0
        Input pilih (nomor film 1-5)
        Switch (pilih)
            Case 1..5:
                Jika STOK tersedia Maka
                    Salin JUDUL ke judul, simpan HARGA ke harga
                    valid = 1
                Jika tidak
                    Tampilkan "Film sedang dipinjam, pilih yang lain!"
            Default:
                Tampilkan "Nomor tidak valid, ulangi!"
    Selama !valid

    Tampilkan film dan harga yang dipilih
    Input lama peminjaman (hari)
    Input jawab ("Perpanjang peminjaman? (y/n)")
    Jika jawab == 'y' atau jawab == 'Y' Maka
        Input tambah hari
        lama = lama + tambah
        Tampilkan lama peminjaman sekarang

    Input hariKembali ("Film dikembalikan pada hari ke-")
    biaya = harga * lama

    Jika hariKembali > lama Maka
        denda = (hariKembali - lama) * 2000
        status = "Terlambat"
    Jika tidak
        denda = 0
        status = "Tepat waktu"

    Tampilkan Bukti Rental (id, nama, judul, harga, lama, hariKembali, biaya, denda, biaya + denda, status)
Selesai
```

### 2.4 Flowchart

```mermaid
flowchart TD
    A([Mulai]) --> B[/Input ID & Nama Pelanggan/]
    B --> C[Tampilkan Daftar 5 Film]
    C --> D[/Input Pilih Nomor Film 1-5/]
    D --> E{Nomor 1-5 & STOK == 1?}
    E -- Tidak --> F[Tampilkan Pesan Error / Dipinjam] --> D
    E -- Ya --> G[/Input Lama Peminjaman/]
    G --> H{Perpanjang? y/n}
    H -- Ya --> I[/Input Tambah Hari/\nlama += tambah] --> J
    H -- Tidak --> J[/Input Hari Dikembalikan/]
    J --> K[biaya = harga * lama]
    K --> L{hariKembali > lama?}
    L -- Ya --> M[denda = (hariKembali - lama) * 2000\nstatus = Terlambat]
    L -- Tidak --> N[denda = 0\nstatus = Tepat waktu]
    M --> O[/Tampilkan Bukti Rental & Total Bayar/]
    N --> O
    O --> P([Selesai])
```

---

## BAB III — IMPLEMENTASI PROGRAM

### 3.1 Lingkungan Pengembangan

| Komponen | Keterangan |
| :--- | :--- |
| **Bahasa pemrograman** | Bahasa C |
| **Compiler/IDE** | GCC (MinGW) / Visual Studio Code |
| **Sistem operasi** | Microsoft Windows 10 / 11 |
| **Editor** | Visual Studio Code |

### 3.2 Struktur Program
1. **Bagian definisi konstanta film (`#define`):** Mendefinisikan `DENDA_PER_HARI` (`2000`), `JUDUL1..5`, `HARGA1..5`, dan `STOK1..5`.
2. **Bagian input pelanggan:** Membaca `id` dan `nama` pelanggan.
3. **Bagian penampilan & validasi pilihan film:** Menampilkan tabel 5 film dan memvalidasi pilihan dengan `do-while` dan `switch-case`.
4. **Bagian lama peminjaman & perpanjangan:** Membaca `lama` pinjam awal dan menambah durasi jika pelanggan memilih perpanjangan (`y/Y`).
5. **Bagian perhitungan biaya & denda:** Menghitung `biaya = harga * lama` serta menentukan `denda` dan `status` menggunakan `if-else`.
6. **Bagian output bukti rental:** Menampilkan struk `BUKTI RENTAL` lengkap ke layar.

### 3.3 Source Code
Source code lengkap terdapat pada file [`rental_film.c`](file:///c:/Users/Bayu%20Arga/Documents/Coding/Kuliah/Semester%201/Pemrograman/UTS/rental_film.c).

### 3.4 Penjelasan Source Code
- **`if`:** Digunakan untuk memeriksa apakah pelanggan ingin memperpanjang waktu sewa (`if (jawab == 'y' || jawab == 'Y')`).
- **`if-else`:** Digunakan di dalam tiap `case` untuk memeriksa apakah stok film tersedia (`if (STOK1) ... else ...`) serta untuk menentukan denda keterlambatan dan status pengembalian (`if (hariKembali > lama) ... else ...`).
- **`switch-case`:** Digunakan untuk mencocokkan nomor pilihan film (`1` sampai `5`) dan menangani pilihan di luar rentang pada bagian `default`.
- **`do-while`:** Digunakan untuk mengulang input pemilihan nomor film selama `valid` masih bernilai `0` (`while (!valid)`).
- **Variabel:** Menggunakan variabel `int` (`id`, `harga`, `pilih`, `valid`, `lama`, `hariKembali`, `tambah`, `biaya`, `denda`) dan `char` (`nama[50]`, `judul[50]`, `status[20]`, `jawab`).
- **Operator:** Menggunakan operator aritmatika (`*`, `-`, `+`, `+=`), relasional (`>`, `==`), logika (`||`, `!`), dan operator ternary (`?:`).
- **Input/Output:** Menggunakan `printf()` untuk output terformat dan `scanf()` untuk membaca input angka, karakter, maupun teks berspasi (`" %[^\n]"`).

---

## BAB IV — PEMBAGIAN KONTRIBUSI

### 4.1 Mahasiswa 1 — Data Pelanggan & Film
- **NRP:** ................................
- **Nama:** ................................
- **Tugas:**
  - Input ID dan nama pelanggan.
  - Menampilkan pilihan film beserta biaya/hari dan statusnya.
  - Input dan validasi pilihan film menggunakan `do-while`.
- **Kode yang dikerjakan:**
  - Definisi `#define JUDUL1..5`, `HARGA1..5`, `STOK1..5`
  - Input `id` dan `nama`, tampilan tabel `DAFTAR FILM`, serta perulangan `do-while` dan `switch (pilih)`
- **Kontribusi pada integrasi program:**
  - Menyediakan data pelanggan (`id`, `nama`) serta data film terpilih (`judul`, `harga`) yang sudah valid.

### 4.2 Mahasiswa 2 — Proses Sewa & Denda
- **NRP:** ................................
- **Nama:** ................................
- **Tugas:**
  - Menentukan biaya sewa.
  - Menghitung lama peminjaman (termasuk fitur perpanjangan peminjaman).
  - Menghitung denda keterlambatan dan menentukan status pengembalian menggunakan `if-else`.
- **Kode yang dikerjakan:**
  - Input `lama`, percabangan perpanjangan sewa (`jawab`, `tambah`), dan input `hariKembali`
  - Perhitungan `biaya = harga * lama` serta blok `if (hariKembali > lama)` untuk menghitung `denda` dan mengisi `status`
- **Kontribusi pada integrasi program:**
  - Mengolah variabel `harga` dari Mahasiswa 1 menjadi `biaya`, `denda`, dan `status` untuk ditampilkan pada bagian Mahasiswa 3.

### 4.3 Mahasiswa 3 — Transaksi & Pengujian
- **NRP:** ................................
- **Nama:** ................................
- **Tugas:**
  - Menampilkan bukti rental lengkap.
  - Menampilkan biaya sewa, denda, total bayar, dan status pengembalian.
  - Menguji skenario peminjaman tepat waktu dan terlambat serta mengintegrasikan program.
- **Kode yang dikerjakan:**
  - Bagian pencetakan `========== BUKTI RENTAL ==========`
  - Integrasi seluruh bagian kode di dalam `main()` dan pengujian 5 skenario program
- **Kontribusi pada integrasi program:**
  - Menyatukan hasil kerja Mahasiswa 1 dan Mahasiswa 2 ke dalam tampilan output akhir dan memverifikasi kebenaran perhitungan.

---

## BAB V — PENGUJIAN PROGRAM

### 5.1 Skenario Pengujian

| No. | Skenario | Input | Hasil yang Diharapkan | Hasil Aktual | Status |
| :--: | :--- | :--- | :--- | :--- | :--: |
| 1 | Peminjaman tepat waktu | `pilih=1`, `lama=3`, `jawab=n`, `hariKembali=3` | Biaya `Rp15000`, Denda `Rp0`, Total `Rp15000`, Status `Tepat waktu` | Biaya `Rp15000`, Denda `Rp0`, Total `Rp15000`, Status `Tepat waktu` | **Berhasil** |
| 2 | Pilihan nomor tidak valid | `pilih=9` | Muncul `Nomor tidak valid, ulangi!` dan diminta input ulang | Muncul `Nomor tidak valid, ulangi!` dan `do-while` mengulang input | **Berhasil** |
| 3 | Pilih film sedang dipinjam | `pilih=3` (*Interstellar*, `STOK3=0`) | Muncul `Film sedang dipinjam, pilih yang lain!` dan minta input ulang | Muncul `Film sedang dipinjam, pilih yang lain!` | **Berhasil** |
| 4 | Perpanjangan peminjaman | `pilih=2`, `lama=2`, `jawab=y`, `tambah=2`, `hariKembali=4` | Lama pinjam menjadi `4 hari`, Biaya `Rp24000`, Denda `Rp0`, `Tepat waktu` | Lama pinjam `4 hari`, Biaya `Rp24000`, Denda `Rp0`, `Tepat waktu` | **Berhasil** |
| 5 | Pengembalian terlambat | `pilih=5`, `lama=2`, `jawab=n`, `hariKembali=5` | Terlambat 3 hari, Biaya `Rp13000`, Denda `Rp6000`, Total `Rp19000`, `Terlambat` | Biaya `Rp13000`, Denda `Rp6000`, Total `Rp19000`, `Terlambat` | **Berhasil** |

### 5.2 Bukti Pengujian

#### Pengujian 1 — Peminjaman Tepat Waktu
```text
Masukkan ID pelanggan   : 101
Masukkan nama pelanggan : Budi Santoso

=============== DAFTAR FILM ===============
No   Nama Film                  Biaya/Hari   Status    
--------------------------------------------------------
1    Avengers: Endgame          Rp5000       Tersedia  
2    Spider-Man: No Way Home    Rp6000       Tersedia  
3    Interstellar               Rp7000       Dipinjam  
4    Your Name                  Rp5000       Tersedia  
5    Inception                  Rp6500       Tersedia  

Pilih nomor film (1-5): 1

Anda memilih: Avengers: Endgame (Rp5000/hari)
Lama peminjaman (hari): 3
Perpanjang peminjaman? (y/n): n
Film dikembalikan pada hari ke-: 3

========== BUKTI RENTAL ==========
ID / Nama    : 101 / Budi Santoso
Film         : Avengers: Endgame
Biaya/hari   : Rp5000
Lama pinjam  : 3 hari
Dikembalikan : hari ke-3
Biaya sewa   : Rp15000
Denda        : Rp0
Total bayar  : Rp15000
Status       : Tepat waktu
==================================
```

#### Pengujian 2 — Validasi Film Dipinjam & Pengembalian Terlambat
```text
Masukkan ID pelanggan   : 102
Masukkan nama pelanggan : Siti Aminah

Pilih nomor film (1-5): 3
Film sedang dipinjam, pilih yang lain!

Pilih nomor film (1-5): 5

Anda memilih: Inception (Rp6500/hari)
Lama peminjaman (hari): 2
Perpanjang peminjaman? (y/n): n
Film dikembalikan pada hari ke-: 5

========== BUKTI RENTAL ==========
ID / Nama    : 102 / Siti Aminah
Film         : Inception
Biaya/hari   : Rp6500
Lama pinjam  : 2 hari
Dikembalikan : hari ke-5
Biaya sewa   : Rp13000
Denda        : Rp6000
Total bayar  : Rp19000
Status       : Terlambat
==================================
```

---

## BAB VI — HASIL DAN PEMBAHASAN

### 6.1 Hasil Program
Program berjalan sesuai spesifikasi tugas Kelompok 3. Pengguna dapat menginput ID dan nama pelanggan, melihat daftar 5 film beserta statusnya, memvalidasi pilihan film dengan `do-while`, memperpanjang waktu peminjaman jika diperlukan, menghitung biaya sewa dan denda keterlambatan secara otomatis, serta menampilkan bukti rental.

### 6.2 Penerapan Struktur Kontrol

| Struktur | Penggunaan dalam Program |
| :--- | :--- |
| `if` | Mengecek apakah pelanggan ingin memperpanjang lama peminjaman (`jawab == 'y' \|\| jawab == 'Y'`) |
| `if-else` | Mengecek ketersediaan stok film (`STOK1..5`) serta menentukan `denda` dan `status` (`Terlambat` / `Tepat waktu`) |
| `switch-case` | Memilih film ke-1 sampai ke-5 berdasarkan nomor pilihan pelanggan |
| `do-while` | Mengulang input pilihan nomor film selama pilihan tidak valid atau stok film sedang dipinjam (`!valid`) |

### 6.3 Kendala dan Solusi

| Kendala | Solusi |
| :--- | :--- |
| Input pilihan film tidak valid (di luar 1–5) atau film sedang dipinjam | Menggunakan perulangan `do-while` dan `switch-case` dengan variabel penanda `valid` |
| Menyimpan daftar 5 film tanpa menggunakan array maupun `struct` | Menggunakan konstanta `#define` (`JUDUL1..5`, `HARGA1..5`, `STOK1..5`) |
| Nama pelanggan yang mengandung spasi terpotong saat dibaca `scanf` | Menggunakan format `scanf(" %[^\n]", nama)` agar membaca hingga akhir baris |

---

## BAB VII — KESIMPULAN

### 7.1 Kesimpulan
Tujuan pembuatan program Sistem Rental Film telah tercapai. Program berhasil mengimplementasikan validasi pilihan film menggunakan `do-while` dan `switch-case`, perhitungan biaya sewa, perpanjangan durasi, serta perhitungan denda keterlambatan dan status pengembalian menggunakan `if-else`, tanpa menggunakan array data, `struct`, maupun pointer.

### 7.2 Saran Pengembangan
Pada tahap selanjutnya, program dapat dikembangkan untuk menangani lebih banyak data film dan pelanggan menggunakan **array**. Selanjutnya data dapat dikelompokkan menggunakan **struct**, kemudian dilakukan manipulasi data menggunakan **pointer**.

---

## DAFTAR PUSTAKA
1. Buku Pemrograman C / C++.
2. Modul Pemrograman Dasar.
3. Dokumentasi C Standard Library (`<stdio.h>` dan `<string.h>`).
