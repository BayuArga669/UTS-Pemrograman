/*
 * ============================================================
 *  KELOMPOK 3 - SISTEM RENTAL FILM
 * ============================================================
 *  Mahasiswa 1 : Data Pelanggan & Film   (do-while, validasi)
 *  Mahasiswa 2 : Proses Sewa & Denda     (if-else, perulangan)
 *  Mahasiswa 3 : Transaksi & Pengujian   (bukti, status, uji)
 * ============================================================
 *  Tidak menggunakan array dan tidak menggunakan konsep OOP.
 *  Data film disimpan dalam switch-case.
 *  Status ketersediaan film disimpan di variabel global.
 * ============================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define JUMLAH_FILM         5
#define MAKS_DURASI_SEWA    7       /* maksimal sewa 7 hari            */
#define DENDA_NORMAL        5000    /* denda hari ke-1 s/d ke-3        */
#define DENDA_BERAT         10000   /* denda mulai hari ke-4 dst       */
#define BATAS_DENDA_NORMAL  3

/* Status ketersediaan tiap film (1 = Tersedia, 0 = Dipinjam) */
int film1_tersedia = 1;
int film2_tersedia = 1;
int film3_tersedia = 1;
int film4_tersedia = 1;
int film5_tersedia = 1;

/* ======================== FUNGSI BANTU ========================== */

void bersihkanBuffer(void)
{
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int bacaInt(const char *prompt)
{
    int nilai, ok;
    do {
        printf("%s", prompt);
        ok = scanf("%d", &nilai);
        if (ok == EOF) {
            printf("\nInput berakhir. Program dihentikan.\n");
            exit(0);
        }
        bersihkanBuffer();
        if (ok != 1)
            printf("  [!] Input harus berupa angka.\n");
    } while (ok != 1);
    return nilai;
}

void bacaString(const char *prompt, char *buf, int ukuran)
{
    char *nl;
    do {
        printf("%s", prompt);
        if (fgets(buf, ukuran, stdin) == NULL) {
            printf("\nInput berakhir. Program dihentikan.\n");
            exit(0);
        }
        nl = strchr(buf, '\n');
        if (nl != NULL) *nl = '\0';
        else bersihkanBuffer();
        if (strlen(buf) == 0)
            printf("  [!] Input tidak boleh kosong.\n");
    } while (strlen(buf) == 0);
}

void garis(char c, int n)
{
    int i;
    for (i = 0; i < n; i++) putchar(c);
    putchar('\n');
}

/* Mengambil judul film berdasarkan nomor (1-5) */
void ambilJudul(int no, char *hasil)
{
    switch (no) {
        case 1: strcpy(hasil, "Avengers: Endgame"); break;
        case 2: strcpy(hasil, "Laskar Pelangi");    break;
        case 3: strcpy(hasil, "Toy Story 4");       break;
        case 4: strcpy(hasil, "Pengabdi Setan 2");  break;
        case 5: strcpy(hasil, "Interstellar");      break;
        default: strcpy(hasil, "-");
    }
}

/* Mengambil kode film */
void ambilKode(int no, char *hasil)
{
    switch (no) {
        case 1: strcpy(hasil, "F001"); break;
        case 2: strcpy(hasil, "F002"); break;
        case 3: strcpy(hasil, "F003"); break;
        case 4: strcpy(hasil, "F004"); break;
        case 5: strcpy(hasil, "F005"); break;
        default: strcpy(hasil, "-");
    }
}

/* Mengambil genre film */
void ambilGenre(int no, char *hasil)
{
    switch (no) {
        case 1: strcpy(hasil, "Action");  break;
        case 2: strcpy(hasil, "Drama");   break;
        case 3: strcpy(hasil, "Animasi"); break;
        case 4: strcpy(hasil, "Horor");   break;
        case 5: strcpy(hasil, "Sci-Fi");  break;
        default: strcpy(hasil, "-");
    }
}

/* Mengambil harga per hari */
long ambilHarga(int no)
{
    switch (no) {
        case 1: return 8000;
        case 2: return 6000;
        case 3: return 7000;
        case 4: return 7500;
        case 5: return 9000;
        default: return 0;
    }
}

/* Mengecek apakah film tersedia */
int cekTersedia(int no)
{
    switch (no) {
        case 1: return film1_tersedia;
        case 2: return film2_tersedia;
        case 3: return film3_tersedia;
        case 4: return film4_tersedia;
        case 5: return film5_tersedia;
        default: return 0;
    }
}

/* Mengubah status ketersediaan film */
void setTersedia(int no, int status)
{
    switch (no) {
        case 1: film1_tersedia = status; break;
        case 2: film2_tersedia = status; break;
        case 3: film3_tersedia = status; break;
        case 4: film4_tersedia = status; break;
        case 5: film5_tersedia = status; break;
    }
}

/* Mengubah angka menjadi format rupiah, contoh: 24000 -> "Rp 24.000" */
void formatRupiah(long nilai, char *hasil)
{
    char tmp[32];
    int i, j, sisa, len;

    sprintf(tmp, "%ld", nilai);
    len = (int)strlen(tmp);
    strcpy(hasil, "Rp ");
    j = 3;
    for (i = 0; i < len; i++) {
        hasil[j++] = tmp[i];
        sisa = len - i - 1;
        if (sisa > 0 && sisa % 3 == 0)
            hasil[j++] = '.';
    }
    hasil[j] = '\0';
}

/* =================================================================
 *  MAHASISWA 1 - DATA PELANGGAN & FILM
 * ================================================================= */

void inputPelanggan(char *id, char *nama)
{
    printf("\n=== DATA PELANGGAN ===\n");
    bacaString("ID Pelanggan   : ", id, 15);
    bacaString("Nama Pelanggan : ", nama, 50);
}

void tampilkanFilm(void)
{
    int i;
    char kode[6], judul[40], genre[15], harga[20];

    printf("\n=== DAFTAR FILM ===\n");
    garis('-', 70);
    printf("%-3s %-6s %-20s %-9s %-12s %-10s\n",
           "No", "Kode", "Judul", "Genre", "Harga/Hari", "Status");
    garis('-', 70);
    for (i = 1; i <= JUMLAH_FILM; i++) {
        ambilKode(i, kode);
        ambilJudul(i, judul);
        ambilGenre(i, genre);
        formatRupiah(ambilHarga(i), harga);
        printf("%-3d %-6s %-20s %-9s %-12s %-10s\n",
               i, kode, judul, genre, harga,
               cekTersedia(i) ? "Tersedia" : "Dipinjam");
    }
    garis('-', 70);
}

/* Input + validasi pilihan film menggunakan do-while.
 * Mengembalikan nomor film (1-5), atau -1 jika semua dipinjam. */
int pilihFilm(void)
{
    int pilihan, valid, adaTersedia = 0;
    int i;
    char judul[40];

    for (i = 1; i <= JUMLAH_FILM; i++)
        if (cekTersedia(i)) adaTersedia = 1;
    if (!adaTersedia) {
        printf("  [!] Semua film sedang dipinjam.\n");
        return -1;
    }

    do {
        pilihan = bacaInt("Pilih nomor film (1-5): ");
        valid = 0;
        if (pilihan < 1 || pilihan > JUMLAH_FILM) {
            printf("  [!] Pilihan tidak valid. Masukkan angka 1-%d.\n", JUMLAH_FILM);
        } else if (!cekTersedia(pilihan)) {
            ambilJudul(pilihan, judul);
            printf("  [!] Film \"%s\" sedang dipinjam. Pilih film lain.\n", judul);
        } else {
            valid = 1;
        }
    } while (!valid);

    ambilJudul(pilihan, judul);
    printf("  Film dipilih: %s\n", judul);
    return pilihan;
}

/* =================================================================
 *  MAHASISWA 2 - PROSES SEWA & DENDA
 * ================================================================= */

int tahunKabisat(int tahun)
{
    if ((tahun % 4 == 0 && tahun % 100 != 0) || tahun % 400 == 0)
        return 1;
    else
        return 0;
}

int jumlahHariBulan(int bulan, int tahun)
{
    if (bulan == 2)
        return tahunKabisat(tahun) ? 29 : 28;
    else if (bulan == 4 || bulan == 6 || bulan == 9 || bulan == 11)
        return 30;
    else
        return 31;
}

int tanggalValid(int hari, int bulan, int tahun)
{
    if (tahun < 2000 || tahun > 2100) return 0;
    if (bulan < 1 || bulan > 12)      return 0;
    if (hari < 1 || hari > jumlahHariBulan(bulan, tahun)) return 0;
    return 1;
}

void inputTanggal(const char *judul, int *hari, int *bulan, int *tahun)
{
    printf("%s\n", judul);
    do {
        *hari  = bacaInt("  Tanggal (1-31) : ");
        *bulan = bacaInt("  Bulan   (1-12) : ");
        *tahun = bacaInt("  Tahun          : ");
        if (!tanggalValid(*hari, *bulan, *tahun))
            printf("  [!] Tanggal tidak valid, ulangi.\n");
    } while (!tanggalValid(*hari, *bulan, *tahun));
}

/* Mengubah tanggal menjadi jumlah hari sejak 1 Jan 2000 (pakai perulangan) */
long tanggalKeHari(int hari, int bulan, int tahun)
{
    long total = 0;
    int th, bl;

    for (th = 2000; th < tahun; th++)
        total += tahunKabisat(th) ? 366 : 365;
    for (bl = 1; bl < bulan; bl++)
        total += jumlahHariBulan(bl, tahun);
    total += hari;
    return total;
}

long hitungBiayaSewa(long hargaPerHari, int durasi)
{
    return hargaPerHari * durasi;
}

int hitungLamaPinjam(int hPinjam, int bPinjam, int tPinjam,
                     int hKembali, int bKembali, int tKembali)
{
    int lama = (int)(tanggalKeHari(hKembali, bKembali, tKembali)
                   - tanggalKeHari(hPinjam, bPinjam, tPinjam));
    if (lama < 1) lama = 1;    /* dikembalikan di hari yang sama = 1 hari */
    return lama;
}

/* Denda dihitung per hari dengan perulangan:
 * hari ke-1 s/d ke-3 : Rp 5.000/hari, hari ke-4 dst : Rp 10.000/hari */
long hitungDenda(int hariTerlambat)
{
    long denda = 0;
    int i;
    for (i = 1; i <= hariTerlambat; i++) {
        if (i <= BATAS_DENDA_NORMAL)
            denda += DENDA_NORMAL;
        else
            denda += DENDA_BERAT;
    }
    return denda;
}

/* Menghitung seluruh komponen transaksi */
void prosesTransaksi(int noFilm, int durasiSewa,
                     int hPinjam, int bPinjam, int tPinjam,
                     int hKembali, int bKembali, int tKembali,
                     int *lamaPinjam, int *hariTerlambat,
                     long *biayaSewa, long *denda, long *total,
                     char *status)
{
    *biayaSewa  = hitungBiayaSewa(ambilHarga(noFilm), durasiSewa);
    *lamaPinjam = hitungLamaPinjam(hPinjam, bPinjam, tPinjam,
                                   hKembali, bKembali, tKembali);

    if (*lamaPinjam > durasiSewa) {
        *hariTerlambat = *lamaPinjam - durasiSewa;
        strcpy(status, "TERLAMBAT");
    } else {
        *hariTerlambat = 0;
        strcpy(status, "TEPAT WAKTU");
    }

    *denda = hitungDenda(*hariTerlambat);
    *total = *biayaSewa + *denda;
}

/* =================================================================
 *  MAHASISWA 3 - TRANSAKSI & PENGUJIAN
 * ================================================================= */

void tampilkanStatusFilm(void)
{
    int i;
    char kode[6], judul[40];

    printf("\n=== STATUS FILM ===\n");
    for (i = 1; i <= JUMLAH_FILM; i++) {
        ambilKode(i, kode);
        ambilJudul(i, judul);
        printf("  %-5s %-20s : %s\n", kode, judul,
               cekTersedia(i) ? "Tersedia" : "Dipinjam");
    }
}

void cetakBukti(const char *id, const char *nama, int noFilm,
                int durasiSewa,
                int hPinjam, int bPinjam, int tPinjam,
                int hKembali, int bKembali, int tKembali,
                int lamaPinjam, int hariTerlambat,
                long biayaSewa, long dendaVal, long total,
                const char *status)
{
    char judul[40], kode[6], genre[15];
    char harga[20], sBiaya[20], sDenda[20], sTotal[20];

    ambilJudul(noFilm, judul);
    ambilKode(noFilm, kode);
    ambilGenre(noFilm, genre);
    formatRupiah(ambilHarga(noFilm), harga);
    formatRupiah(biayaSewa, sBiaya);
    formatRupiah(dendaVal, sDenda);
    formatRupiah(total, sTotal);

    printf("\n");
    garis('=', 46);
    printf("            BUKTI RENTAL FILM\n");
    garis('=', 46);
    printf("ID Pelanggan    : %s\n", id);
    printf("Nama Pelanggan  : %s\n", nama);
    garis('-', 46);
    printf("Film            : %s (%s)\n", judul, kode);
    printf("Genre           : %s\n", genre);
    printf("Harga / Hari    : %s\n", harga);
    printf("Tanggal Pinjam  : %02d-%02d-%04d\n", hPinjam, bPinjam, tPinjam);
    printf("Tanggal Kembali : %02d-%02d-%04d\n", hKembali, bKembali, tKembali);
    printf("Durasi Sewa     : %d hari\n", durasiSewa);
    printf("Lama Pinjam     : %d hari\n", lamaPinjam);
    printf("Hari Terlambat  : %d hari\n", hariTerlambat);
    garis('-', 46);
    printf("Biaya Sewa      : %15s\n", sBiaya);
    printf("Denda           : %15s\n", sDenda);
    garis('-', 46);
    printf("TOTAL BAYAR     : %15s\n", sTotal);
    garis('-', 46);
    printf("Status Kembali  : %s\n", status);
    printf("Status Film     : %s\n",
           cekTersedia(noFilm) ? "Tersedia (sudah dikembalikan)" : "Dipinjam");
    garis('=', 46);
    printf("     Terima kasih telah menyewa film!\n");
    garis('=', 46);
}

/* Transaksi lengkap: data pelanggan -> pinjam -> kembali -> bukti */
void transaksiBaru(void)
{
    char id[15], nama[50];
    int noFilm, durasiSewa;
    int hPinjam, bPinjam, tPinjam;
    int hKembali, bKembali, tKembali;
    int lamaPinjam, hariTerlambat;
    long biayaSewa, denda, total;
    char status[20];
    int valid;
    char judul[40];

    /* Mahasiswa 1 */
    inputPelanggan(id, nama);
    tampilkanFilm();
    noFilm = pilihFilm();
    if (noFilm < 0) return;

    /* Mahasiswa 2 */
    do {
        durasiSewa = bacaInt("Durasi sewa (1-7 hari): ");
        if (durasiSewa < 1 || durasiSewa > MAKS_DURASI_SEWA)
            printf("  [!] Durasi sewa harus 1-%d hari.\n", MAKS_DURASI_SEWA);
    } while (durasiSewa < 1 || durasiSewa > MAKS_DURASI_SEWA);

    inputTanggal("\nMasukkan tanggal pinjam:", &hPinjam, &bPinjam, &tPinjam);
    setTersedia(noFilm, 0);
    ambilJudul(noFilm, judul);
    printf("\n>> Film \"%s\" berhasil dipinjam.\n", judul);
    tampilkanStatusFilm();

    printf("\n=== PENGEMBALIAN FILM ===\n");
    do {
        inputTanggal("Masukkan tanggal kembali:", &hKembali, &bKembali, &tKembali);
        valid = tanggalKeHari(hKembali, bKembali, tKembali)
              >= tanggalKeHari(hPinjam, bPinjam, tPinjam);
        if (!valid)
            printf("  [!] Tanggal kembali tidak boleh sebelum tanggal pinjam.\n");
    } while (!valid);

    prosesTransaksi(noFilm, durasiSewa,
                    hPinjam, bPinjam, tPinjam,
                    hKembali, bKembali, tKembali,
                    &lamaPinjam, &hariTerlambat,
                    &biayaSewa, &denda, &total, status);
    setTersedia(noFilm, 1);     /* film dikembalikan */

    /* Mahasiswa 3 */
    cetakBukti(id, nama, noFilm, durasiSewa,
               hPinjam, bPinjam, tPinjam,
               hKembali, bKembali, tKembali,
               lamaPinjam, hariTerlambat,
               biayaSewa, denda, total, status);
    tampilkanStatusFilm();
}

/* Pengujian otomatis: kasus tepat waktu & terlambat */
int ujiKasus(const char *namaKasus,
             const char *id, const char *nama, int noFilm, int durasiSewa,
             int hPinjam, int bPinjam, int tPinjam,
             int hKembali, int bKembali, int tKembali,
             int expLama, int expTerlambat,
             long expBiaya, long expDenda, long expTotal,
             const char *expStatus)
{
    int lamaPinjam, hariTerlambat, lulus;
    long biayaSewa, denda, total;
    char status[20];

    prosesTransaksi(noFilm, durasiSewa,
                    hPinjam, bPinjam, tPinjam,
                    hKembali, bKembali, tKembali,
                    &lamaPinjam, &hariTerlambat,
                    &biayaSewa, &denda, &total, status);

    printf("\n>>> %s\n", namaKasus);
    cetakBukti(id, nama, noFilm, durasiSewa,
               hPinjam, bPinjam, tPinjam,
               hKembali, bKembali, tKembali,
               lamaPinjam, hariTerlambat,
               biayaSewa, denda, total, status);

    lulus = lamaPinjam == expLama && hariTerlambat == expTerlambat &&
            biayaSewa == expBiaya && denda == expDenda &&
            total == expTotal && strcmp(status, expStatus) == 0;

    printf("Diharapkan : lama=%d, telat=%d, biaya=%ld, denda=%ld, total=%ld, %s\n",
           expLama, expTerlambat, expBiaya, expDenda, expTotal, expStatus);
    printf("Hasil      : lama=%d, telat=%d, biaya=%ld, denda=%ld, total=%ld, %s\n",
           lamaPinjam, hariTerlambat, biayaSewa, denda, total, status);
    printf("Kesimpulan : %s\n", lulus ? "LULUS" : "GAGAL");
    return lulus;
}

void pengujian(void)
{
    int lulus = 0;

    printf("\n========== MODE PENGUJIAN ==========\n");

    /* Kasus 1: Tepat waktu.
     * Sewa 3 hari, pinjam 01-10-2026, kembali 04-10-2026 */
    lulus += ujiKasus("KASUS 1 - PENGEMBALIAN TEPAT WAKTU",
                      "P001", "Budi Santoso", 1, 3,
                      1, 10, 2026,
                      4, 10, 2026,
                      3, 0, 24000, 0, 24000, "TEPAT WAKTU");

    /* Kasus 2: Terlambat.
     * Sewa 2 hari, pinjam 28-09-2026, kembali 05-10-2026
     * Lama 7 hari -> telat 5 hari -> denda 3x5.000 + 2x10.000 = 35.000 */
    lulus += ujiKasus("KASUS 2 - PENGEMBALIAN TERLAMBAT",
                      "P002", "Siti Aminah", 5, 2,
                      28, 9, 2026,
                      5, 10, 2026,
                      7, 5, 18000, 35000, 53000, "TERLAMBAT");

    printf("\n========== HASIL PENGUJIAN: %d/2 LULUS ==========\n", lulus);
}

/* =================================================================
 *  PROGRAM UTAMA (INTEGRASI)
 * ================================================================= */
int main(void)
{
    int menu;

    do {
        printf("\n");
        garis('=', 40);
        printf("       SISTEM RENTAL FILM - KELOMPOK 3\n");
        garis('=', 40);
        printf("1. Transaksi Rental Baru\n");
        printf("2. Lihat Daftar & Status Film\n");
        printf("3. Pengujian (Tepat Waktu & Terlambat)\n");
        printf("0. Keluar\n");
        garis('-', 40);
        menu = bacaInt("Pilih menu: ");

        if (menu == 1)
            transaksiBaru();
        else if (menu == 2)
            tampilkanFilm();
        else if (menu == 3)
            pengujian();
        else if (menu == 0)
            printf("Terima kasih. Program selesai.\n");
        else
            printf("  [!] Menu tidak tersedia.\n");
    } while (menu != 0);

    return 0;
}
