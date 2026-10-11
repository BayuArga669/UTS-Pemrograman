#include <stdio.h>
#include <string.h>

#define DENDA_PER_HARI 2000

/* ====== Data film: ubah di sini saja ====== */
/* STOK: 1 = tersedia, 0 = sedang dipinjam */
#define JUDUL1 "Avengers: Endgame"
#define HARGA1 5000
#define STOK1  1

#define JUDUL2 "Spider-Man: No Way Home"
#define HARGA2 6000
#define STOK2  1

#define JUDUL3 "Interstellar"
#define HARGA3 7000
#define STOK3  0

#define JUDUL4 "Your Name"
#define HARGA4 5000
#define STOK4  1

#define JUDUL5 "Inception"
#define HARGA5 6500
#define STOK5  1

int main() {
    /* Data pelanggan */
    int id;
    char nama[50];

    /* Data film terpilih */
    char judul[50];
    int harga = 0;

    /* Data transaksi */
    int pilih, valid;
    int lama, hariKembali, tambah;
    char jawab;
    int biaya, denda;
    char status[20];

    /* ===== MAHASISWA 1: Data Pelanggan & Film ===== */
    printf("Masukkan ID pelanggan   : ");
    scanf("%d", &id);
    printf("Masukkan nama pelanggan : ");
    scanf(" %[^\n]", nama);

    printf("\n=============== DAFTAR FILM ===============\n");
    printf("%-4s %-26s %-12s %-10s\n", "No", "Nama Film", "Biaya/Hari", "Status");
    printf("--------------------------------------------------------\n");
    printf("%-4d %-26s Rp%-10d %-10s\n", 1, JUDUL1, HARGA1, STOK1 ? "Tersedia" : "Dipinjam");
    printf("%-4d %-26s Rp%-10d %-10s\n", 2, JUDUL2, HARGA2, STOK2 ? "Tersedia" : "Dipinjam");
    printf("%-4d %-26s Rp%-10d %-10s\n", 3, JUDUL3, HARGA3, STOK3 ? "Tersedia" : "Dipinjam");
    printf("%-4d %-26s Rp%-10d %-10s\n", 4, JUDUL4, HARGA4, STOK4 ? "Tersedia" : "Dipinjam");
    printf("%-4d %-26s Rp%-10d %-10s\n", 5, JUDUL5, HARGA5, STOK5 ? "Tersedia" : "Dipinjam");

    /* Input + validasi pilihan film (do-while) */
    do {
        valid = 0;
        printf("\nPilih nomor film (1-5): ");
        scanf("%d", &pilih);

        switch (pilih) {
            case 1:
                if (STOK1) { strcpy(judul, JUDUL1); harga = HARGA1; valid = 1; }
                else printf("Film sedang dipinjam, pilih yang lain!\n");
                break;
            case 2:
                if (STOK2) { strcpy(judul, JUDUL2); harga = HARGA2; valid = 1; }
                else printf("Film sedang dipinjam, pilih yang lain!\n");
                break;
            case 3:
                if (STOK3) { strcpy(judul, JUDUL3); harga = HARGA3; valid = 1; }
                else printf("Film sedang dipinjam, pilih yang lain!\n");
                break;
            case 4:
                if (STOK4) { strcpy(judul, JUDUL4); harga = HARGA4; valid = 1; }
                else printf("Film sedang dipinjam, pilih yang lain!\n");
                break;
            case 5:
                if (STOK5) { strcpy(judul, JUDUL5); harga = HARGA5; valid = 1; }
                else printf("Film sedang dipinjam, pilih yang lain!\n");
                break;
            default:
                printf("Nomor tidak valid, ulangi!\n");
        }
    } while (!valid);

    printf("\nAnda memilih: %s (Rp%d/hari)\n", judul, harga);

    /* ===== MAHASISWA 2: Proses Sewa & Denda ===== */
    printf("Lama peminjaman (hari): ");
    scanf("%d", &lama);

    printf("Perpanjang peminjaman? (y/n): ");
    scanf(" %c", &jawab);
    if (jawab == 'y' || jawab == 'Y') {
        printf("Tambah berapa hari? ");
        scanf("%d", &tambah);
        lama += tambah;
        printf("Lama peminjaman sekarang: %d hari\n", lama);
    }

    printf("Film dikembalikan pada hari ke-: ");
    scanf("%d", &hariKembali);

    biaya = harga * lama;

    if (hariKembali > lama) {
        denda = (hariKembali - lama) * DENDA_PER_HARI;
        strcpy(status, "Terlambat");
    } else {
        denda = 0;
        strcpy(status, "Tepat waktu");
    }

    /* ===== MAHASISWA 3: Transaksi & Pengujian ===== */
    printf("\n========== BUKTI RENTAL ==========\n");
    printf("ID / Nama    : %d / %s\n", id, nama);
    printf("Film         : %s\n", judul);
    printf("Biaya/hari   : Rp%d\n", harga);
    printf("Lama pinjam  : %d hari\n", lama);
    printf("Dikembalikan : hari ke-%d\n", hariKembali);
    printf("Biaya sewa   : Rp%d\n", biaya);
    printf("Denda        : Rp%d\n", denda);
    printf("Total bayar  : Rp%d\n", biaya + denda);
    printf("Status       : %s\n", status);
    printf("==================================\n");

    return 0;
}
