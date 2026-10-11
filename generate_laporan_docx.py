# -*- coding: utf-8 -*-
"""
Script untuk membuat dokumen Word resmi (.docx) Laporan Mini Project
sesuai format 8 halaman PDF template laporan.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()

    # Set Margins 1 inch (standard)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Base styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Helper functions
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.name = 'Times New Roman'
        p.paragraph_format.space_after = Pt(12)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        run.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        return p

    def add_p(text, bold=False, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.size = Pt(12)
        run.font.name = 'Times New Roman'
        return p

    def add_code_block(code_text):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 120, 120, 180, 180)
        
        # Border tipis abu
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:left w:val="single" w:sz="12" w:space="0" w:color="0284C7"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/></w:tcBorders>')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # HALAMAN SAMPUL
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("FORMAT LAPORAN PENGERJAAN\nMINI PROJECT PEMROGRAMAN C++\n\n")
    r.bold = True
    r.font.size = Pt(14)
    r.font.name = 'Times New Roman'

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("HALAMAN SAMPUL\nLAPORAN MINI PROJECT PEMROGRAMAN C++\n\n")
    r2.bold = True
    r2.font.size = Pt(13)

    p_cover = doc.add_paragraph()
    p_cover.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cover.paragraph_format.line_spacing = 1.3
    
    runs_cover = [
        ("Judul Project:\n", True),
        ("Sistem Rental Film\n\n", False),
        ("Kelompok: ", True),
        ("3 (Tiga)\n\n", False),
        ("Anggota Kelompok:\n", True),
        ("1. NRP – Nama Mahasiswa 1 (Mahasiswa 1 — Data Pelanggan & Film)\n", False),
        ("2. NRP – Nama Mahasiswa 2 (Mahasiswa 2 — Proses Sewa & Denda)\n", False),
        ("3. NRP – Nama Mahasiswa 3 (Mahasiswa 3 — Transaksi & Pengujian)\n\n", False),
        ("Mata Kuliah: ", True),
        ("Pemrograman Dasar\n", False),
        ("Dosen Pengampu: ", True),
        ("................................................\n", False),
        ("Program Studi: ", True),
        ("................................................\n", False),
        ("Institusi: ", True),
        ("................................................\n", False),
        ("Tahun: ", True),
        ("2026\n", False),
    ]
    for text, bold in runs_cover:
        r = p_cover.add_run(text)
        r.bold = bold
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # BAB I — PENDAHULUAN
    # =========================================================================
    add_h1("BAB I — PENDAHULUAN")
    
    add_h2("1.1 Latar Belakang")
    add_p(
        "Proses penyewaan (rental) film yang dilakukan secara manual membutuhkan pencatatan data identitas "
        "pelanggan, pemilihan judul film yang masih tersedia, serta perhitungan biaya sewa dan denda keterlambatan "
        "secara terstruktur. Selain itu, pelanggan terkadang mengajukan perpanjangan masa peminjaman saat masa sewa "
        "sedang berlangsung. Pencatatan konvensional rentan menyebabkan kesalahan perhitungan biaya, kekeliruan "
        "pencatatan status ketersediaan film, serta keterlambatan dalam menghitung denda harian. Oleh karena itu, "
        "dibuat sebuah program sederhana menggunakan bahasa C untuk membantu proses transaksi rental film secara "
        "otomatis, akurat, dan terstruktur."
    )

    add_h2("1.2 Rumusan Masalah")
    add_p("Berdasarkan latar belakang di atas, rumusan masalah dalam pembuatan program ini adalah:")
    add_bullet("1. Bagaimana membuat program sistem rental film menggunakan bahasa C?")
    add_bullet("2. Bagaimana melakukan input data pelanggan serta validasi pilihan dan ketersediaan stok film menggunakan perulangan do-while dan switch-case?")
    add_bullet("3. Bagaimana menentukan biaya sewa, perpanjangan durasi pinjam, denda keterlambatan (Rp2.000/hari), dan status pengembalian menggunakan if-else?")
    add_bullet("4. Bagaimana menampilkan bukti rental transaksi lengkap dan memastikan program berjalan dengan tepat pada berbagai kondisi?")

    add_h2("1.3 Tujuan")
    add_p("Tujuan dari pengerjaan mini project ini adalah:")
    add_bullet("1. Membuat program sistem rental film yang fungsional dan terstruktur menggunakan bahasa C.")
    add_bullet("2. Menerapkan struktur percabangan if, if-else, dan switch-case.")
    add_bullet("3. Menerapkan struktur perulangan do-while untuk validasi input nomor film dan status stok.")
    add_bullet("4. Menerapkan validasi input dan logika perhitungan biaya sewa, perpanjangan masa pinjam, serta denda keterlambatan.")
    add_bullet("5. Mengembangkan kemampuan kolaborasi, pembagian tugas kerja, dan integrasi kode dalam kelompok.")

    add_h2("1.4 Batasan Masalah")
    add_p("Batasan masalah dalam pembuatan program rental film ini meliputi:")
    add_bullet("• Program dibuat menggunakan bahasa pemrograman C (menggunakan header <stdio.h> dan <string.h>).")
    add_bullet("• Program tidak menggunakan array pada tahap ini untuk daftar film (data film disimpan menggunakan konstanta makro #define).")
    add_bullet("• Program tidak menggunakan struct maupun konsep Object-Oriented Programming (OOP).")
    add_bullet("• Program tidak menggunakan pointer.")
    add_bullet("• Struktur kontrol yang digunakan adalah if, if-else, switch-case, dan do-while.")
    add_bullet("• Data transaksi hanya disimpan dalam memori variabel selama program berjalan.")
    add_bullet("• Tarif denda keterlambatan ditetapkan flat sebesar Rp2.000 per hari keterlambatan.")

    # =========================================================================
    # BAB II — ANALISIS DAN PERANCANGAN
    # =========================================================================
    add_h1("BAB II — ANALISIS DAN PERANCANGAN")

    add_h2("2.1 Deskripsi Sistem")
    add_p(
        "Program Sistem Rental Film bekerja secara interaktif melalui antarmuka konsol (terminal). "
        "Alur kerja program dimulai dengan meminta pengguna memasukkan data identitas pelanggan berupa ID pelanggan "
        "dan nama lengkap. Setelah data pelanggan diinput, program mencetak tabel berisi daftar 5 film beserta "
        "biaya sewa per hari dan status ketersediaannya (Tersedia atau Dipinjam). "
        "Pengguna kemudian diminta memilih nomor film (1–5). Program melakukan validasi menggunakan perulangan do-while "
        "dan percabangan switch-case: jika nomor di luar 1–5 atau stok film bernilai 0 (sedang dipinjam, contohnya film "
        "Interstellar), program menampilkan pesan peringatan dan meminta pengguna memilih ulang hingga pilihan valid. "
        "Setelah film terpilih, pengguna memasukkan lama peminjaman awal, memilih apakah ingin memperpanjang waktu pinjam "
        "(y/n), dan memasukkan hari ke-berapa film dikembalikan. Program menghitung biaya sewa (harga × lama), "
        "memeriksa apakah pengembalian terlambat (hariKembali > lama), menghitung denda ((hariKembali - lama) × 2000) "
        "dan menentukan status ('Terlambat' atau 'Tepat waktu'), lalu mencetak Bukti Rental lengkap."
    )

    add_h2("2.2 Input – Proses – Output")
    add_p("Hubungan antara data masukan, proses pengolahan, dan keluaran disajikan pada tabel berikut:")

    table_ipo = doc.add_table(rows=7, cols=3)
    table_ipo.alignment = WD_TABLE_ALIGNMENT.CENTER
    ipo_headers = ["Input", "Proses", "Output"]
    for i, h in enumerate(ipo_headers):
        cell = table_ipo.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0284C7")
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        set_cell_margins(cell, 80, 80, 100, 100)

    ipo_rows = [
        ("ID pelanggan (id)", "Membaca ID bertipe integer", "Identitas ID pelanggan"),
        ("Nama pelanggan (nama)", "Membaca teks nama lengkap berspasi", "Identitas Nama pelanggan"),
        ("Pilihan film (pilih)", "Validasi nomor (1-5) & status stok (do-while & switch)", "Nama film & harga terpilih"),
        ("Lama peminjaman (lama)", "Menghitung biaya sewa = harga * lama", "Lama sewa terkonfirmasi"),
        ("Perpanjangan (jawab, tambah)", "Menambah durasi pinjam jika jawab == 'y' (if)", "Total lama pinjam baru"),
        ("Hari dikembalikan (hariKembali)", "Mengecek hariKembali > lama, hitung denda & total bayar (if-else)", "Bukti Rental, Total Bayar & Status"),
    ]
    for r_idx, row in enumerate(ipo_rows, start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = table_ipo.cell(r_idx, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("2.3 Algoritma")
    add_p("Algoritma/pseudocode lengkap sistem rental film dituliskan sebagai berikut:")
    
    pseudo = (
        "Mulai\n"
        "  Input id pelanggan\n"
        "  Input nama pelanggan\n"
        "  Tampilkan DAFTAR FILM (1 s/d 5) beserta Biaya/Hari dan Status (Tersedia/Dipinjam)\n\n"
        "  Ulangi (do-while !valid):\n"
        "    valid = 0\n"
        "    Input pilih (nomor film 1-5)\n"
        "    Switch (pilih):\n"
        "      Case 1..5:\n"
        "        Jika STOK film ke-n tersedia (1) Maka:\n"
        "          Salin JUDUL ke variabel judul\n"
        "          Simpan HARGA ke variabel harga\n"
        "          valid = 1\n"
        "        Jika tidak (STOK == 0):\n"
        "          Tampilkan \"Film sedang dipinjam, pilih yang lain!\"\n"
        "      Default:\n"
        "        Tampilkan \"Nomor tidak valid, ulangi!\"\n"
        "  Selama valid == 0\n\n"
        "  Tampilkan judul film dan harga yang dipilih\n"
        "  Input lama peminjaman (hari)\n"
        "  Input jawab (\"Perpanjang peminjaman? (y/n)\")\n"
        "  Jika jawab == 'y' atau jawab == 'Y' Maka:\n"
        "    Input tambah (jumlah hari tambahan)\n"
        "    lama = lama + tambah\n"
        "    Tampilkan lama peminjaman sekarang\n\n"
        "  Input hariKembali (\"Film dikembalikan pada hari ke-\")\n"
        "  biaya = harga * lama\n\n"
        "  Jika hariKembali > lama Maka:\n"
        "    denda = (hariKembali - lama) * DENDA_PER_HARI\n"
        "    status = \"Terlambat\"\n"
        "  Jika tidak:\n"
        "    denda = 0\n"
        "    status = \"Tepat waktu\"\n\n"
        "  Tampilkan BUKTI RENTAL:\n"
        "    ID / Nama Pelanggan\n"
        "    Nama Film terpilih\n"
        "    Biaya sewa per hari\n"
        "    Lama pinjam\n"
        "    Hari dikembalikan\n"
        "    Biaya sewa\n"
        "    Denda keterlambatan\n"
        "    Total bayar (biaya + denda)\n"
        "    Status pengembalian (Tepat waktu / Terlambat)\n"
        "Selesai"
    )
    add_code_block(pseudo)

    add_h2("2.4 Flowchart")
    add_p("Alur eksekusi program mengikuti standar minimal: Mulai → Input → Validasi → Proses → Perhitungan → Output → Selesai:")
    add_bullet("1. Mulai: Inisialisasi program dan variabel.")
    add_bullet("2. Input: Menerima ID pelanggan dan nama pelanggan.")
    add_bullet("3. Tampilkan Daftar: Menampilkan tabel 5 film beserta status ketersediaannya.")
    add_bullet("4. Validasi (do-while & switch): Membaca pilihan nomor film (1–5) dan memeriksa ketersediaan stok. Jika tidak valid atau stok 0, alur berputar kembali meminta input ulang.")
    add_bullet("5. Proses Durasi: Membaca lama hari sewa, mengecek percabangan perpanjangan (y/n), dan membaca hari pengembalian aktual.")
    add_bullet("6. Perhitungan: Menghitung biaya = harga × lama, membandingkan hariKembali > lama untuk menghitung denda (Rp2.000 × hari telat) dan menentukan status.")
    add_bullet("7. Output: Mencetak struk Bukti Rental lengkap beserta total pembayaran.")
    add_bullet("8. Selesai: Program mengakhiri eksekusi dengan return 0.")
    add_p("Diagram visual lengkap flowchart juga telah disertakan pada file Flowchart_Rental_Film.drawio serta pada Lampiran C laporan ini.", italic=True)

    # =========================================================================
    # BAB III — IMPLEMENTASI PROGRAM
    # =========================================================================
    add_h1("BAB III — IMPLEMENTASI PROGRAM")

    add_h2("3.1 Lingkungan Pengembangan")
    add_p("Spesifikasi lingkungan yang digunakan selama tahap perancangan dan implementasi kode:")

    table_env = doc.add_table(rows=5, cols=2)
    table_env.alignment = WD_TABLE_ALIGNMENT.CENTER
    env_headers = ["Komponen", "Keterangan"]
    for i, h in enumerate(env_headers):
        cell = table_env.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0284C7")
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        set_cell_margins(cell, 80, 80, 100, 100)

    env_rows = [
        ("Bahasa Pemrograman", "Bahasa C (Standard C99 / C11)"),
        ("Compiler / IDE", "GCC (MinGW.org GCC-6.3.0) via Terminal"),
        ("Sistem Operasi", "Microsoft Windows 11"),
        ("Editor", "Visual Studio Code"),
    ]
    for r_idx, row in enumerate(env_rows, start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = table_env.cell(r_idx, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("3.2 Struktur Program")
    add_p("Program rental_film.c disusun ke dalam beberapa bagian utama:")
    add_bullet("1. Bagian Header & Konstanta Makro: Mengimpor <stdio.h> dan <string.h>, mendefinisikan DENDA_PER_HARI (2000), serta konstanta 5 data film (JUDUL1..5, HARGA1..5, STOK1..5).")
    add_bullet("2. Bagian Deklarasi Variabel: Mendeklarasikan variabel id, nama, judul, harga, pilih, valid, lama, hariKembali, tambah, jawab, biaya, denda, dan status.")
    add_bullet("3. Bagian Input Pelanggan (Mahasiswa 1): Membaca ID dan Nama Pelanggan menggunakan scanf.")
    add_bullet("4. Bagian Daftar & Validasi Film (Mahasiswa 1): Menampilkan tabel film berformat rapi dan memvalidasi pilihan film dengan do-while serta switch-case.")
    add_bullet("5. Bagian Lama Sewa & Perpanjangan (Mahasiswa 2): Membaca lama hari peminjaman dan memproses perpanjangan durasi jika pengguna menjawab 'y'.")
    add_bullet("6. Bagian Perhitungan Biaya & Denda (Mahasiswa 2): Menghitung biaya sewa serta percabangan if-else untuk menghitung denda keterlambatan dan status kembali.")
    add_bullet("7. Bagian Bukti Rental (Mahasiswa 3): Mencetak laporan struk Bukti Rental secara terperinci.")

    add_h2("3.3 Source Code")
    add_p("Source code lengkap program rental_film.c adalah sebagai berikut:")

    with open(r"c:\Users\Bayu Arga\Documents\Coding\Kuliah\Semester 1\Pemrograman\UTS\rental_film.c", "r", encoding="utf-8") as f:
        c_code = f.read()
    add_code_block(c_code)

    add_h2("3.4 Penjelasan Source Code")
    add_p("Penjelasan struktur kontrol dan elemen pemrograman penting yang diterapkan dalam kode program:")
    add_bullet("• if: Digunakan untuk memeriksa apakah pelanggan memilih perpanjangan peminjaman (if (jawab == 'y' || jawab == 'Y')).")
    add_bullet("• if-else: Diterapkan di dalam blok switch untuk memeriksa ketersediaan stok film (if (STOKn) ... else ...) serta untuk menentukan status pengembalian dan perhitungan denda (if (hariKembali > lama) ... else ...).")
    add_bullet("• switch-case: Diterapkan untuk mencocokkan nomor film yang diinput (case 1 sampai 5) dan menyalin judul serta harga film terpilih ke variabel transaksi. Bagian default menangani nomor yang tidak valid.")
    add_bullet("• do-while: Diterapkan pada proses pemilihan film (do { ... } while (!valid);), memastikan blok pemilihan minimal dijalankan 1 kali dan diulang selama input belum valid.")
    add_bullet("• Variabel: Menggunakan tipe integer (id, harga, pilih, valid, lama, hariKembali, tambah, biaya, denda) dan karakter (nama[50], judul[50], status[20], jawab).")
    add_bullet("• Operator: Menggunakan operator aritmatika (*, +, -, +=), operator relasional (>, ==), operator logika (||, !), dan operator ternary (STOK ? \"Tersedia\" : \"Dipinjam\").")
    add_bullet("• Input / Output: Menggunakan fungsi pustaka printf() untuk menampilkan teks terformat rapi dan scanf() untuk membaca nilai masukan dari pengguna.")

    # =========================================================================
    # BAB IV — PEMBAGIAN KONTRIBUSI
    # =========================================================================
    add_h1("BAB IV — PEMBAGIAN KONTRIBUSI")
    add_p("Bagian ini memaparkan kontribusi dan pembagian tanggung jawab masing-masing anggota kelompok:")

    add_h2("4.1 Mahasiswa 1 — Data Pelanggan & Film")
    add_bullet("NRP: ................................")
    add_bullet("Nama: ................................")
    add_bullet("Tugas:")
    add_bullet("  - Membuat input ID pelanggan dan nama pelanggan.")
    add_bullet("  - Menampilkan daftar 5 pilihan film beserta biaya sewa/hari dan status ketersediaan.")
    add_bullet("  - Membuat input pilihan nomor film.")
    add_bullet("  - Membuat validasi pilihan film menggunakan perulangan do-while dan switch-case.")
    add_bullet("Kode yang dikerjakan:")
    add_bullet("  - Pendefinisian konstanta #define JUDUL1..5, HARGA1..5, dan STOK1..5.")
    add_bullet("  - Blok input id, nama, tampilan tabel DAFTAR FILM, dan perulangan do-while pemilihan film.")
    add_bullet("Kontribusi pada integrasi program:")
    add_bullet("  - Menyediakan nilai variabel judul dan harga yang tervalidasi agar siap dihitung pada tahap berikutnya.")

    add_h2("4.2 Mahasiswa 2 — Proses Sewa & Denda")
    add_bullet("NRP: ................................")
    add_bullet("Nama: ................................")
    add_bullet("Tugas:")
    add_bullet("  - Menentukan dan menghitung biaya sewa berdasarkan harga film dan lama peminjaman.")
    add_bullet("  - Menghitung total lama peminjaman termasuk opsi perpanjangan waktu peminjaman.")
    add_bullet("  - Menghitung denda keterlambatan (Rp2.000/hari) jika hari pengembalian melebihi batas waktu.")
    add_bullet("  - Menentukan status pengembalian ('Tepat waktu' atau 'Terlambat') menggunakan if-else.")
    add_bullet("Kode yang dikerjakan:")
    add_bullet("  - Blok input lama, opsi perpanjangan jawab dan penambahan durasi tambah.")
    add_bullet("  - Blok input hariKembali, perhitungan biaya = harga * lama, serta percabangan if-else untuk menghitung denda dan mengisi variabel status.")
    add_bullet("Kontribusi pada integrasi program:")
    add_bullet("  - Menghubungkan pilihan film dari Mahasiswa 1 dengan perhitungan finansial dan status yang akan dicetak oleh Mahasiswa 3.")

    add_h2("4.3 Mahasiswa 3 — Transaksi & Pengujian")
    add_bullet("NRP: ................................")
    add_bullet("Nama: ................................")
    add_bullet("Tugas:")
    add_bullet("  - Menampilkan bukti rental transaksi secara lengkap dan rapi.")
    add_bullet("  - Menampilkan rincian biaya sewa, denda keterlambatan, dan total yang harus dibayarkan.")
    add_bullet("  - Menampilkan status film dan status pengembalian.")
    add_bullet("  - Menguji kasus peminjaman tepat waktu dan peminjaman terlambat.")
    add_bullet("  - Mengintegrasikan seluruh bagian kode menjadi satu program utuh.")
    add_bullet("Kode yang dikerjakan:")
    add_bullet("  - Blok pencetakan BUKTI RENTAL lengkap dengan format garis pembatas.")
    add_bullet("  - Penggabungan kode Mahasiswa 1 dan Mahasiswa 2 di dalam fungsi main().")
    add_bullet("  - Pengujian skenario normal, skenario salah input, dan skenario keterlambatan.")
    add_bullet("Kontribusi pada integrasi program:")
    add_bullet("  - Menyatukan seluruh alur sistem serta memastikan program bebas dari kesalahan kompilasi dan logika.")

    # =========================================================================
    # BAB V — PENGUJIAN PROGRAM
    # =========================================================================
    add_h1("BAB V — PENGUJIAN PROGRAM")

    add_h2("5.1 Skenario Pengujian")
    add_p("Pengujian dilakukan mencakup 5 skenario penting untuk memastikan keandalan program:")

    table_test = doc.add_table(rows=6, cols=6)
    table_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["No.", "Skenario", "Input", "Hasil yang Diharapkan", "Hasil Aktual", "Status"]
    for i, h in enumerate(test_headers):
        cell = table_test.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0284C7")
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(10.5)
        set_cell_margins(cell, 80, 80, 80, 80)

    test_rows = [
        ("1", "Input valid (Tepat waktu)", "pilih=1, lama=3, jawab=n, kembali=3", "Biaya Rp15.000, Denda Rp0, Total Rp15.000, Tepat waktu", "Biaya Rp15.000, Denda Rp0, Total Rp15.000, Tepat waktu", "Berhasil"),
        ("2", "Pilihan tidak valid", "pilih=9", "Muncul 'Nomor tidak valid, ulangi!' dan input diulang", "Pesan error tampil dan do-while mengulang input", "Berhasil"),
        ("3", "Kondisi batas (Film dipinjam)", "pilih=3 (Interstellar, STOK=0)", "Muncul 'Film sedang dipinjam, pilih yang lain!' dan input diulang", "Pesan tampil dan program meminta input ulang", "Berhasil"),
        ("4", "Perpanjangan masa sewa", "pilih=2, lama=2, jawab=y, tambah=2, kembali=4", "Lama jadi 4 hari, Biaya Rp24.000, Denda Rp0, Tepat waktu", "Lama 4 hari, Biaya Rp24.000, Denda Rp0, Tepat waktu", "Berhasil"),
        ("5", "Pengembalian terlambat", "pilih=5, lama=2, jawab=n, kembali=5", "Telat 3 hari, Biaya Rp13.000, Denda Rp6.000, Total Rp19.000, Terlambat", "Biaya Rp13.000, Denda Rp6.000, Total Rp19.000, Terlambat", "Berhasil"),
    ]
    for r_idx, row in enumerate(test_rows, start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = table_test.cell(r_idx, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            if c_idx == 5:
                cell.paragraphs[0].runs[0].bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x05, 0x96, 0x69)
            set_cell_margins(cell, 60, 60, 60, 60)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("5.2 Bukti Pengujian")
    add_p("Berikut adalah salinan hasil running program pada terminal untuk setiap skenario penting:")

    add_p("Pengujian 1 — Peminjaman Tepat Waktu (Input Normal):", bold=True)
    out1 = (
        "Masukkan ID pelanggan   : 101\n"
        "Masukkan nama pelanggan : Budi Santoso\n\n"
        "=============== DAFTAR FILM ===============\n"
        "No   Nama Film                  Biaya/Hari   Status    \n"
        "--------------------------------------------------------\n"
        "1    Avengers: Endgame          Rp5000       Tersedia  \n"
        "2    Spider-Man: No Way Home    Rp6000       Tersedia  \n"
        "3    Interstellar               Rp7000       Dipinjam  \n"
        "4    Your Name                  Rp5000       Tersedia  \n"
        "5    Inception                  Rp6500       Tersedia  \n\n"
        "Pilih nomor film (1-5): 1\n\n"
        "Anda memilih: Avengers: Endgame (Rp5000/hari)\n"
        "Lama peminjaman (hari): 3\n"
        "Perpanjang peminjaman? (y/n): n\n"
        "Film dikembalikan pada hari ke-: 3\n\n"
        "========== BUKTI RENTAL ==========\n"
        "ID / Nama    : 101 / Budi Santoso\n"
        "Film         : Avengers: Endgame\n"
        "Biaya/hari   : Rp5000\n"
        "Lama pinjam  : 3 hari\n"
        "Dikembalikan : hari ke-3\n"
        "Biaya sewa   : Rp15000\n"
        "Denda        : Rp0\n"
        "Total bayar  : Rp15000\n"
        "Status       : Tepat waktu\n"
        "=================================="
    )
    add_code_block(out1)

    add_p("Pengujian 2 & 3 — Input Tidak Valid & Kondisi Batas (Film Dipinjam):", bold=True)
    out2 = (
        "Pilih nomor film (1-5): 9\n"
        "Nomor tidak valid, ulangi!\n\n"
        "Pilih nomor film (1-5): 3\n"
        "Film sedang dipinjam, pilih yang lain!\n\n"
        "Pilih nomor film (1-5): 5\n"
        "Anda memilih: Inception (Rp6500/hari)"
    )
    add_code_block(out2)

    add_p("Pengujian 4 & 5 — Perpanjangan Sewa & Pengembalian Terlambat:", bold=True)
    out3 = (
        "Masukkan ID pelanggan   : 102\n"
        "Masukkan nama pelanggan : Siti Aminah\n"
        "Pilih nomor film (1-5): 5\n"
        "Anda memilih: Inception (Rp6500/hari)\n"
        "Lama peminjaman (hari): 2\n"
        "Perpanjang peminjaman? (y/n): n\n"
        "Film dikembalikan pada hari ke-: 5\n\n"
        "========== BUKTI RENTAL ==========\n"
        "ID / Nama    : 102 / Siti Aminah\n"
        "Film         : Inception\n"
        "Biaya/hari   : Rp6500\n"
        "Lama pinjam  : 2 hari\n"
        "Dikembalikan : hari ke-5\n"
        "Biaya sewa   : Rp13000\n"
        "Denda        : Rp6000\n"
        "Total bayar  : Rp19000\n"
        "Status       : Terlambat\n"
        "=================================="
    )
    add_code_block(out3)

    # =========================================================================
    # BAB VI — HASIL DAN PEMBAHASAN
    # =========================================================================
    add_h1("BAB VI — HASIL DAN PEMBAHASAN")

    add_h2("6.1 Hasil Program")
    add_p(
        "Setelah diimplementasikan dan diuji, program sistem rental film berhasil berjalan dengan lancar tanpa error "
        "maupun warning saat dikompilasi menggunakan GCC. Seluruh fitur utama berfungsi sesuai rancangan: program mampu "
        "menerima input nama berspasi, menampilkan katalog film secara rapi, menolak input film yang sedang dipinjam "
        "atau nomor di luar 1–5, menangani opsi perpanjangan sewa dengan menambahkan durasi secara dinamis, "
        "menghitung biaya sewa dan denda keterlambatan secara akurat, serta menyajikan bukti rental yang informatif."
    )

    add_h2("6.2 Penerapan Struktur Kontrol")
    add_p("Ringkasan peran dan penerapan setiap struktur kontrol di dalam program:")

    table_ctrl = doc.add_table(rows=5, cols=2)
    table_ctrl.alignment = WD_TABLE_ALIGNMENT.CENTER
    ctrl_headers = ["Struktur", "Penggunaan dalam Program"]
    for i, h in enumerate(ctrl_headers):
        cell = table_ctrl.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0284C7")
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        set_cell_margins(cell, 80, 80, 100, 100)

    ctrl_rows = [
        ("if", "Mengecek apakah pengguna memilih opsi perpanjangan waktu peminjaman (jawab == 'y' || jawab == 'Y')"),
        ("if-else", "Mengecek stok ketersediaan film (STOKn) serta menentukan denda keterlambatan dan status pengembalian (hariKembali > lama)"),
        ("switch-case", "Memetakan nomor film yang dipilih pengguna (1-5) ke judul dan harga film masing-masing, serta menangani nilai default"),
        ("do-while", "Mengulang proses input pemilihan nomor film selama nomor tidak valid atau film berstatus sedang dipinjam (!valid)"),
    ]
    for r_idx, row in enumerate(ctrl_rows, start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = table_ctrl.cell(r_idx, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("6.3 Kendala dan Solusi")
    add_p("Tabel kendala teknis yang dihadapi selama pengerjaan dan solusi yang diterapkan:")

    table_sol = doc.add_table(rows=4, cols=2)
    table_sol.alignment = WD_TABLE_ALIGNMENT.CENTER
    sol_headers = ["Kendala", "Solusi"]
    for i, h in enumerate(sol_headers):
        cell = table_sol.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0284C7")
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        set_cell_margins(cell, 80, 80, 100, 100)

    sol_rows = [
        ("Input pilihan film tidak valid atau film sedang dipinjam (STOK = 0)", "Menggunakan perulangan do-while dengan flag penanda valid serta switch-case yang memvalidasi STOK"),
        ("Menyimpan data 5 film tanpa array maupun struct", "Menggunakan konstanta makro #define untuk JUDUL1..5, HARGA1..5, dan STOK1..5 secara terstruktur"),
        ("Nama pelanggan yang mengandung spasi terpotong saat dibaca scanf", "Menggunakan format penentu scanf(\" %[^\n]\", nama) agar membaca karakter hingga baris baru"),
    ]
    for r_idx, row in enumerate(sol_rows, start=1):
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = table_sol.cell(r_idx, c_idx)
            cell.text = val
            set_cell_background(cell, bg)
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # BAB VII — KESIMPULAN
    # =========================================================================
    add_h1("BAB VII — KESIMPULAN")

    add_h2("7.1 Kesimpulan")
    add_p(
        "Berdasarkan hasil perancangan, implementasi, dan pengujian program Sistem Rental Film, dapat disimpulkan bahwa "
        "tujuan mini project telah tercapai dengan baik. Program berhasil dibangun menggunakan bahasa C dengan menerapkan "
        "struktur kontrol dasar meliputi if, if-else, switch-case, dan do-while tanpa menggunakan array data, struct, "
        "maupun pointer. Sistem mampu memvalidasi pilihan film, mengakomodasi perpanjangan durasi sewa, menghitung denda "
        "keterlambatan, serta mencetak bukti rental secara otomatis dan akurat pada seluruh skenario pengujian."
    )

    add_h2("7.2 Saran Pengembangan")
    add_p(
        "Bagian ini sangat penting karena project akan dikembangkan pada tugas atau mata kuliah berikutnya. "
        "Saran perbaikan dan peningkatan untuk pengembangan lebih lanjut meliputi:"
    )
    add_bullet("1. Penggunaan Array: Pada tahap selanjutnya, program dapat dikembangkan untuk menangani lebih banyak data film dan antrean riwayat transaksi pelanggan secara dinamis menggunakan struktur array satu dimensi maupun dua dimensi.")
    add_bullet("2. Pengelompokan Data dengan Struct: Data pelanggan (ID, nama), data film (kode, judul, harga, status), dan data transaksi dapat dikelompokkan ke dalam struct agar pengelolaan tipe data majemuk lebih terorganisir dan modular.")
    add_bullet("3. Manipulasi Menggunakan Pointer & File: Pada tahap lanjut, manipulasi memori dapat dilakukan menggunakan pointer untuk efisiensi fungsi, serta menambahkan fitur File I/O agar riwayat transaksi dan data stok film tersimpan permanen ke media penyimpanan eksternal (file .txt atau .dat).")

    # =========================================================================
    # DAFTAR PUSTAKA
    # =========================================================================
    add_h1("DAFTAR PUSTAKA")
    add_bullet("1. Kernighan, B. W., & Ritchie, D. M. (1988). The C Programming Language (2nd ed.). Englewood Cliffs, NJ: Prentice Hall.")
    add_bullet("2. Deitel, P. J., & Deitel, H. M. (2016). C How to Program (8th ed.). Boston: Pearson Education.")
    add_bullet("3. Modul Praktikum Pemrograman Dasar Tahun 2026.")
    add_bullet("4. Dokumentasi Standard C Library (<stdio.h> dan <string.h>) — https://en.cppreference.com/w/c")

    # =========================================================================
    # LAMPIRAN
    # =========================================================================
    add_h1("LAMPIRAN")

    add_h2("Lampiran A — Source Code Lengkap")
    add_p("File source code lengkap rental_film.c disertakan pada repository project dan tertera pada Subbab 3.3.")

    add_h2("Lampiran B — Screenshot Program")
    add_p("Hasil tangkapan layar (screenshot) terminal pengujian program rental_film.c disertakan pada Subbab 5.2.")

    add_h2("Lampiran C — Flowchart")
    add_p("File diagram flowchart lengkap tersimpan dalam format Flowchart_Rental_Film.drawio yang dapat dibuka dan diedit menggunakan aplikasi diagram draw.io.")

    add_h2("Lampiran D — Bukti Kontribusi Anggota")
    add_bullet("• Mahasiswa 1: Mengerjakan bagian input ID & nama pelanggan, definisi katalog film #define, tampilan DAFTAR FILM, dan perulangan do-while + switch untuk validasi pilihan film.")
    add_bullet("• Mahasiswa 2: Mengerjakan bagian input lama pinjam, percabangan perpanjangan sewa (jawab == 'y'), input hari pengembalian, perhitungan biaya = harga * lama, dan logika if-else denda serta penentuan status.")
    add_bullet("• Mahasiswa 3: Mengerjakan bagian pencetakan BUKTI RENTAL, penggabungan seluruh blok kode ke main(), kompilasi program, serta pengujian kelima skenario uji.")

    output_path = r"c:\Users\Bayu Arga\Documents\Coding\Kuliah\Semester 1\Pemrograman\UTS\Laporan_Mini_Project_Kelompok_3.docx"
    doc.save(output_path)
    print(f"Laporan berhasil dibuat di: {output_path}")

if __name__ == "__main__":
    create_document()
