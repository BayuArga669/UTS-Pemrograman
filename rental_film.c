/*
 * ============================================================
 *  MINI PROJECT PEMROGRAMAN DASAR (BAHASA C)
 *  KELOMPOK 3 - SISTEM RENTAL FILM
 * ============================================================
 *  Batasan Program:
 *  - Menggunakan bahasa C
 *  - Tidak menggunakan array data, struct (OOP), maupun pointer
 *  - Menggunakan struktur kontrol: if, if-else, while, do-while, for
 *
 *  Pembagian Tugas:
 *  - Mahasiswa 1 : Data Pelanggan & Film (Input, Validasi, do-while)
 *  - Mahasiswa 2 : Proses Sewa & Denda   (Biaya, Lama, Denda, if-else & loop)
 *  - Mahasiswa 3 : Transaksi & Pengujian (Bukti Rental, Status, Pengujian)
 * ============================================================
 */

#include <stdio.h>

/* Konstanta aturan rental */
#define JUMLAH_FILM         5
#define MAKS_DURASI_SEWA    7
#define DENDA_NORMAL        5000    /* Denda keterlambatan hari ke-1 s/d ke-3 */
#define DENDA_BERAT         10000   /* Denda keterlambatan hari ke-4 dst      */
#define BATAS_DENDA_NORMAL  3

/* Variabel global status ketersediaan film (1 = Tersedia, 0 = Dipinjam) */
int film1_tersedia = 1;
int film2_tersedia = 1;
int film3_tersedia = 1;
int film4_tersedia = 1;
int film5_tersedia = 1;

/* Variabel global data pelanggan & transaksi berjalan */
char idPelanggan[20];
char namaPelanggan[50];
int  pilihanFilm;
int  durasiSewa;
int  lamaPinjam;
int  hariTerlambat;
long hargaPerHari;
long biayaSewa;
long denda;
long totalBayar;
long uangBayar;
long kembalian;
int  statusTerlambat; /* 0 = TEPAT WAKTU, 1 = TERLAMBAT */

/* ======================== FUNGSI BANTU ========================== */

/* Mencetak garis pembatas menggunakan perulangan for */
void cetakGaris(char simbol, int panjang)
{
    int i;
    for (i = 0; i < panjang; i++) {
        printf("%c", simbol);
    }
    printf("\n");
}

/* Membersihkan sisa karakter di buffer input menggunakan while */
void bersihkanInput(void)
{
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {
        /* kosong - hanya membuang sisa karakter */
    }
}

/* Menampilkan nama & kode film berdasarkan nomor urut (tanpa array/struct) */
void cetakNamaFilm(int no)
{
    if (no == 1) {
        printf("Avengers: Endgame (F001)");
    } else if (no == 2) {
        printf("Laskar Pelangi (F002)");
    } else if (no == 3) {
        printf("Toy Story 4 (F003)");
    } else if (no == 4) {
        printf("Pengabdi Setan 2 (F004)");
    } else if (no == 5) {
        printf("Interstellar (F005)");
    } else {
        printf("Tidak diketahui");
    }
}

/* Mengambil harga sewa film per hari */
long ambilHargaFilm(int no)
{
    if (no == 1) return 8000;
    else if (no == 2) return 6000;
    else if (no == 3) return 7000;
    else if (no == 4) return 7500;
    else if (no == 5) return 9000;
    else return 0;
}

/* Mengecek status ketersediaan film (1 = Tersedia, 0 = Dipinjam) */
int cekFilmTersedia(int no)
{
    if (no == 1) return film1_tersedia;
    else if (no == 2) return film2_tersedia;
    else if (no == 3) return film3_tersedia;
    else if (no == 4) return film4_tersedia;
    else if (no == 5) return film5_tersedia;
    else return 0;
}

/* Mengubah status ketersediaan film */
void ubahStatusFilm(int no, int status)
{
    if (no == 1) film1_tersedia = status;
    else if (no == 2) film2_tersedia = status;
    else if (no == 3) film3_tersedia = status;
    else if (no == 4) film4_tersedia = status;
    else if (no == 5) film5_tersedia = status;
}

/* =================================================================
 *  MAHASISWA 1 - DATA PELANGGAN & FILM
 *  - Input ID dan nama pelanggan
 *  - Menampilkan pilihan film
 *  - Input & validasi pilihan film menggunakan do-while
 * ================================================================= */

void inputDataPelanggan(void)
{
    printf("\n=== INPUT DATA PELANGGAN ===\n");
    printf("Masukkan ID Pelanggan   : ");
    scanf("%19s", idPelanggan);
    bersihkanInput();

    printf("Masukkan Nama Pelanggan : ");
    scanf(" %49[^\n]", namaPelanggan);
    bersihkanInput();
}

void tampilkanDaftarFilm(void)
{
    printf("\n=== DAFTAR PILIHAN FILM ===\n");
    cetakGaris('-', 66);
    printf("No  Kode   Judul Film           Genre     Harga/Hari   Status\n");
    cetakGaris('-', 66);
    printf("1   F001   Avengers: Endgame    Action    Rp 8000      %s\n",
           film1_tersedia ? "Tersedia" : "Dipinjam");
    printf("2   F002   Laskar Pelangi       Drama     Rp 6000      %s\n",
           film2_tersedia ? "Tersedia" : "Dipinjam");
    printf("3   F003   Toy Story 4          Animasi   Rp 7000      %s\n",
           film3_tersedia ? "Tersedia" : "Dipinjam");
    printf("4   F004   Pengabdi Setan 2     Horor     Rp 7500      %s\n",
           film4_tersedia ? "Tersedia" : "Dipinjam");
    printf("5   F005   Interstellar         Sci-Fi    Rp 9000      %s\n",
           film5_tersedia ? "Tersedia" : "Dipinjam");
    cetakGaris('-', 66);
}

void inputDanValidasiFilm(void)
{
    int valid = 0;
    int hasilBaca;

    /* Validasi pilihan film menggunakan do-while */
    do {
        printf("Pilih nomor film (1-%d)  : ", JUMLAH_FILM);
        hasilBaca = scanf("%d", &pilihanFilm);
        bersihkanInput();

        if (hasilBaca != 1) {
            printf("  [!] Error: Input harus berupa angka!\n");
            valid = 0;
        } else if (pilihanFilm < 1 || pilihanFilm > JUMLAH_FILM) {
            printf("  [!] Error: Pilihan film tidak valid! Pilih nomor 1 s/d %d.\n", JUMLAH_FILM);
            valid = 0;
        } else if (cekFilmTersedia(pilihanFilm) == 0) {
            printf("  [!] Error: Film sedang dipinjam! Silakan pilih film lain.\n");
            valid = 0;
        } else {
            valid = 1;
        }
    } while (valid == 0);

    printf("  >> Film dipilih: ");
    cetakNamaFilm(pilihanFilm);
    printf("\n");
}

/* =================================================================
 *  MAHASISWA 2 - PROSES SEWA & DENDA
 *  - Menentukan biaya sewa
 *  - Menghitung lama peminjaman
 *  - Menghitung denda keterlambatan (menggunakan for & if-else)
 *  - Menentukan status pengembalian (menggunakan if-else)
 * ================================================================= */

void inputDurasiDanLamaPinjam(void)
{
    int valid;
    int hasilBaca;

    /* Validasi durasi sewa yang disepakati (1-7 hari) */
    do {
        printf("Durasi sewa (1-%d hari)  : ", MAKS_DURASI_SEWA);
        hasilBaca = scanf("%d", &durasiSewa);
        bersihkanInput();

        if (hasilBaca != 1 || durasiSewa < 1 || durasiSewa > MAKS_DURASI_SEWA) {
            printf("  [!] Error: Durasi sewa harus antara 1 sampai %d hari.\n", MAKS_DURASI_SEWA);
            valid = 0;
        } else {
            valid = 1;
        }
    } while (valid == 0);

    /* Ubah status film menjadi Dipinjam saat disewa */
    ubahStatusFilm(pilihanFilm, 0);

    /* Input lama peminjaman aktual saat pengembalian */
    do {
        printf("Lama peminjaman aktual (hari): ");
        hasilBaca = scanf("%d", &lamaPinjam);
        bersihkanInput();

        if (hasilBaca != 1 || lamaPinjam < 1) {
            printf("  [!] Error: Lama peminjaman minimal 1 hari.\n");
            valid = 0;
        } else {
            valid = 1;
        }
    } while (valid == 0);
}

void hitungSewaDanDenda(void)
{
    int hariKe;

    /* 1. Menentukan harga per hari dan menghitung biaya sewa */
    hargaPerHari = ambilHargaFilm(pilihanFilm);
    biayaSewa    = hargaPerHari * durasiSewa;

    /* 2. Menentukan status pengembalian & jumlah hari terlambat (if-else) */
    if (lamaPinjam > durasiSewa) {
        hariTerlambat   = lamaPinjam - durasiSewa;
        statusTerlambat = 1; /* TERLAMBAT */
    } else {
        hariTerlambat   = 0;
        statusTerlambat = 0; /* TEPAT WAKTU */
    }

    /* 3. Menghitung denda keterlambatan dengan perulangan for dan if-else
     *    Hari ke-1 s/d ke-3 : Rp 5.000 / hari
     *    Hari ke-4 dst      : Rp 10.000 / hari
     */
    denda = 0;
    for (hariKe = 1; hariKe <= hariTerlambat; hariKe++) {
        if (hariKe <= BATAS_DENDA_NORMAL) {
            denda = denda + DENDA_NORMAL;
        } else {
            denda = denda + DENDA_BERAT;
        }
    }

    /* 4. Menghitung total biaya yang harus dibayar */
    totalBayar = biayaSewa + denda;
}

void prosesPembayaran(void)
{
    int valid;
    int hasilBaca;

    printf("Total yang harus dibayar: Rp %ld\n", totalBayar);
    do {
        printf("Masukkan jumlah uang bayar: Rp ");
        hasilBaca = scanf("%ld", &uangBayar);
        bersihkanInput();

        if (hasilBaca != 1 || uangBayar < totalBayar) {
            printf("  [!] Error: Uang pembayaran kurang! Minimal Rp %ld.\n", totalBayar);
            valid = 0;
        } else {
            kembalian = uangBayar - totalBayar;
            valid = 1;
        }
    } while (valid == 0);

    /* Setelah pembayaran selesai, film dikembalikan (status = Tersedia) */
    ubahStatusFilm(pilihanFilm, 1);
}

/* =================================================================
 *  MAHASISWA 3 - TRANSAKSI & PENGUJIAN
 *  - Menampilkan bukti rental
 *  - Menampilkan biaya dan denda
 *  - Menampilkan status film
 *  - Menguji peminjaman tepat waktu dan terlambat
 *  - Mengintegrasikan program
 * ================================================================= */

void tampilkanStatusSemuaFilm(void)
{
    int i;
    printf("\n=== STATUS KETERSEDIAAN FILM ===\n");
    for (i = 1; i <= JUMLAH_FILM; i++) {
        printf("  %d. ", i);
        cetakNamaFilm(i);
        printf(" -> %s\n", cekFilmTersedia(i) ? "Tersedia" : "Dipinjam");
    }
}

void tampilkanBuktiRental(void)
{
    printf("\n");
    cetakGaris('=', 48);
    printf("               BUKTI RENTAL FILM\n");
    cetakGaris('=', 48);
    printf("ID Pelanggan      : %s\n", idPelanggan);
    printf("Nama Pelanggan    : %s\n", namaPelanggan);
    cetakGaris('-', 48);
    printf("Film Disewa       : ");
    cetakNamaFilm(pilihanFilm);
    printf("\n");
    printf("Harga Sewa / Hari : Rp %ld\n", hargaPerHari);
    printf("Durasi Sewa       : %d hari\n", durasiSewa);
    printf("Lama Peminjaman   : %d hari\n", lamaPinjam);
    printf("Keterlambatan     : %d hari\n", hariTerlambat);
    cetakGaris('-', 48);
    printf("Biaya Sewa        : Rp %ld\n", biayaSewa);
    printf("Denda Terlambat   : Rp %ld\n", denda);
    cetakGaris('-', 48);
    printf("TOTAL BAYAR       : Rp %ld\n", totalBayar);
    printf("Uang Pembayaran   : Rp %ld\n", uangBayar);
    printf("Kembalian         : Rp %ld\n", kembalian);
    cetakGaris('-', 48);
    printf("Status Kembali    : %s\n",
           statusTerlambat ? "TERLAMBAT" : "TEPAT WAKTU");
    printf("Status Film       : %s\n",
           cekFilmTersedia(pilihanFilm) ? "Tersedia (Sudah Dikembalikan)" : "Sedang Dipinjam");
    cetakGaris('=', 48);
    printf("       Terima kasih telah menyewa film!\n");
    cetakGaris('=', 48);
}

/* Menjalankan 1 transaksi penuh (integrasi Mahasiswa 1, 2, dan 3) */
void jalankanTransaksi(void)
{
    /* Bagian Mahasiswa 1 */
    inputDataPelanggan();
    tampilkanDaftarFilm();
    inputDanValidasiFilm();

    /* Bagian Mahasiswa 2 */
    inputDurasiDanLamaPinjam();
    tampilkanStatusSemuaFilm(); /* menampilkan status saat film sedang dipinjam */
    hitungSewaDanDenda();
    prosesPembayaran();

    /* Bagian Mahasiswa 3 */
    tampilkanBuktiRental();
    tampilkanStatusSemuaFilm(); /* menampilkan status setelah film dikembalikan */
}

/* Fungsi pengujian otomatis: Tepat Waktu & Terlambat */
void pengujianOtomatis(void)
{
    printf("\n");
    cetakGaris('=', 52);
    printf("   PENGUJIAN OTOMATIS (TEPAT WAKTU & TERLAMBAT)\n");
    cetakGaris('=', 52);

    /* --- KASUS UJI 1: Peminjaman Tepat Waktu --- */
    printf("\n[KASUS UJI 1] Peminjaman Tepat Waktu\n");
    snprintf(idPelanggan, sizeof(idPelanggan), "P001");
    snprintf(namaPelanggan, sizeof(namaPelanggan), "Budi Santoso");
    pilihanFilm = 1; /* Avengers: Endgame - Rp 8000/hari */
    durasiSewa  = 3;
    lamaPinjam  = 3; /* Dikembalikan tepat 3 hari */

    ubahStatusFilm(pilihanFilm, 0);
    hitungSewaDanDenda();
    uangBayar = 30000;
    kembalian = uangBayar - totalBayar;
    ubahStatusFilm(pilihanFilm, 1);
    tampilkanBuktiRental();

    if (biayaSewa == 24000 && denda == 0 && totalBayar == 24000 && statusTerlambat == 0) {
        printf(">> HASIL UJI 1 (TEPAT WAKTU): BERHASIL / LULUS\n");
    } else {
        printf(">> HASIL UJI 1 (TEPAT WAKTU): GAGAL\n");
    }

    /* --- KASUS UJI 2: Peminjaman Terlambat --- */
    printf("\n[KASUS UJI 2] Peminjaman Terlambat\n");
    snprintf(idPelanggan, sizeof(idPelanggan), "P002");
    snprintf(namaPelanggan, sizeof(namaPelanggan), "Siti Aminah");
    pilihanFilm = 5; /* Interstellar - Rp 9000/hari */
    durasiSewa  = 2;
    lamaPinjam  = 7; /* Terlambat 5 hari: 3x5000 + 2x10000 = 35000 */

    ubahStatusFilm(pilihanFilm, 0);
    hitungSewaDanDenda();
    uangBayar = 60000;
    kembalian = uangBayar - totalBayar;
    ubahStatusFilm(pilihanFilm, 1);
    tampilkanBuktiRental();

    if (biayaSewa == 18000 && denda == 35000 && totalBayar == 53000 && statusTerlambat == 1) {
        printf(">> HASIL UJI 2 (TERLAMBAT)  : BERHASIL / LULUS\n");
    } else {
        printf(">> HASIL UJI 2 (TERLAMBAT)  : GAGAL\n");
    }
}

/* =================================================================
 *  PROGRAM UTAMA (INTEGRASI MENU)
 * ================================================================= */
int main(void)
{
    int menu;
    int hasilBaca;
    char ulangTransaksi;

    do {
        printf("\n");
        cetakGaris('=', 44);
        printf("      SISTEM RENTAL FILM - KELOMPOK 3\n");
        cetakGaris('=', 44);
        printf("1. Transaksi Rental Film Baru\n");
        printf("2. Lihat Daftar & Status Film\n");
        printf("3. Pengujian (Tepat Waktu & Terlambat)\n");
        printf("0. Keluar\n");
        cetakGaris('-', 44);
        printf("Pilih menu (0-3): ");

        hasilBaca = scanf("%d", &menu);
        bersihkanInput();

        if (hasilBaca != 1) {
            printf("  [!] Error: Masukkan angka menu 0-3!\n");
            menu = -1;
        } else if (menu == 1) {
            do {
                jalankanTransaksi();
                printf("\nIngin melakukan transaksi lagi? (y/t): ");
                scanf(" %c", &ulangTransaksi);
                bersihkanInput();
            } while (ulangTransaksi == 'y' || ulangTransaksi == 'Y');
        } else if (menu == 2) {
            tampilkanDaftarFilm();
        } else if (menu == 3) {
            pengujianOtomatis();
        } else if (menu == 0) {
            printf("\nTerima kasih telah menggunakan Sistem Rental Film!\n");
        } else {
            printf("  [!] Error: Pilihan menu tidak tersedia!\n");
        }
    } while (menu != 0);

    return 0;
}
