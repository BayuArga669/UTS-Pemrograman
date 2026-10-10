# -*- coding: utf-8 -*-
"""
Generator PowerPoint (.pptx) Murni menggunakan Python Standard Library (zipfile + XML).
Menghasilkan file Presentasi_Rental_Film_Kelompok_3.pptx (16:9 Widescreen)
sesuai dengan Format Laporan Mini Project Pemrograman Dasar & Tugas Kelompok 3.
"""

import zipfile
from xml.sax.saxutils import escape

OUTPUT_FILE = "Presentasi_Rental_Film_Kelompok_3.pptx"

# Ukuran slide 16:9 dalam EMU (1 inch = 914400 EMU -> 13.333 x 7.5 inch)
SLIDE_W = 12192000
SLIDE_H = 6858000


def emu_in(inches):
    return int(inches * 914400)


class SlideBuilder:
    def __init__(self, bg_hex="F8FAFC"):
        self.bg_hex = bg_hex
        self.shapes = []
        self.next_id = 2

    def _id(self):
        i = self.next_id
        self.next_id += 1
        return i

    def add_rect(self, x, y, w, h, fill_hex, line_hex=None, line_w=12700, roundness=None):
        sid = self._id()
        geom = "roundRect" if roundness is not None else "rect"
        av = f'<a:avLst><a:gd name="adj" fmla="val {roundness}"/></a:avLst>' if roundness is not None else "<a:avLst/>"
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill_hex}"/></a:solidFill>' if fill_hex else "<a:noFill/>"
        if line_hex:
            line_xml = f'<a:ln w="{line_w}"><a:solidFill><a:srgbClr val="{line_hex}"/></a:solidFill></a:ln>'
        else:
            line_xml = "<a:ln><a:noFill/></a:ln>"

        self.shapes.append(f"""
        <p:sp>
          <p:nvSpPr>
            <p:cNvPr id="{sid}" name="Rect{sid}"/>
            <p:cNvSpPr/>
            <p:nvPr/>
          </p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
            <a:prstGeom prst="{geom}">{av}</a:prstGeom>
            {fill_xml}
            {line_xml}
          </p:spPr>
        </p:sp>""")

    def add_textbox(self, x, y, w, h, paragraphs, fill_hex=None, line_hex=None,
                    roundness=None, anchor="t", pad=(91440, 68580, 91440, 68580)):
        """
        paragraphs: list of dicts or tuples:
          dict keys: text, size (pt), bold (bool), color (hex), align ('l','ctr','r'),
                     bullet (bool), font ('Calibri' or 'Consolas'), space_after (pt)
        """
        sid = self._id()
        geom = "roundRect" if roundness is not None else "rect"
        av = f'<a:avLst><a:gd name="adj" fmla="val {roundness}"/></a:avLst>' if roundness is not None else "<a:avLst/>"
        fill_xml = f'<a:solidFill><a:srgbClr val="{fill_hex}"/></a:solidFill>' if fill_hex else "<a:noFill/>"
        if line_hex:
            line_xml = f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{line_hex}"/></a:solidFill></a:ln>'
        else:
            line_xml = "<a:ln><a:noFill/></a:ln>"

        lIns, tIns, rIns, bIns = pad
        p_xml_list = []
        for p in paragraphs:
            if isinstance(p, str):
                p = {"text": p}
            text = escape(p.get("text", ""))
            size = int(p.get("size", 14) * 100)
            bold = "1" if p.get("bold", False) else "0"
            italic = "1" if p.get("italic", False) else "0"
            color = p.get("color", "1E293B")
            align = p.get("align", "l")
            bullet = p.get("bullet", False)
            font = p.get("font", "Calibri")
            spc_after = int(p.get("space_after", 4) * 100)

            if bullet:
                ppr = f'<a:pPr algn="{align}" marL="228600" indent="-228600"><a:spcAft><a:spcPts val="{spc_after}"/></a:spcAft><a:buChar char="•"/></a:pPr>'
            else:
                ppr = f'<a:pPr algn="{align}"><a:spcAft><a:spcPts val="{spc_after}"/></a:spcAft><a:buNone/></a:pPr>'

            p_xml_list.append(f"""
            <a:p>
              {ppr}
              <a:r>
                <a:rPr lang="id-ID" sz="{size}" b="{bold}" i="{italic}" dirty="0">
                  <a:solidFill><a:srgbClr val="{color}"/></a:solidFill>
                  <a:latin typeface="{font}"/>
                  <a:cs typeface="{font}"/>
                </a:rPr>
                <a:t>{text}</a:t>
              </a:r>
            </a:p>""")

        p_joined = "".join(p_xml_list)
        self.shapes.append(f"""
        <p:sp>
          <p:nvSpPr>
            <p:cNvPr id="{sid}" name="TextBox{sid}"/>
            <p:cNvSpPr txBox="1"/>
            <p:nvPr/>
          </p:nvSpPr>
          <p:spPr>
            <a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>
            <a:prstGeom prst="{geom}">{av}</a:prstGeom>
            {fill_xml}
            {line_xml}
          </p:spPr>
          <p:txBody>
            <a:bodyPr wrap="square" lIns="{lIns}" tIns="{tIns}" rIns="{rIns}" bIns="{bIns}" anchor="{anchor}"/>
            <a:lstStyle/>
            {p_joined}
          </p:txBody>
        </p:sp>""")

    def add_header(self, bab_label, title, subtitle, slide_no):
        # Top navy header bar
        self.add_rect(0, 0, SLIDE_W, emu_in(1.15), "0F172A")
        self.add_rect(0, emu_in(1.15), SLIDE_W, emu_in(0.06), "38BDF8")
        # Bab badge
        self.add_textbox(
            emu_in(0.55), emu_in(0.18), emu_in(2.4), emu_in(0.32),
            [{"text": bab_label, "size": 11, "bold": True, "color": "0F172A", "align": "ctr"}],
            fill_hex="38BDF8", roundness=25000, anchor="ctr", pad=(30000, 10000, 30000, 10000)
        )
        # Main slide title
        self.add_textbox(
            emu_in(0.55), emu_in(0.52), emu_in(10.5), emu_in(0.55),
            [{"text": title, "size": 22, "bold": True, "color": "FFFFFF"}],
            pad=(0, 0, 0, 0)
        )
        # Subtitle on right
        self.add_textbox(
            emu_in(8.5), emu_in(0.18), emu_in(4.25), emu_in(0.35),
            [{"text": subtitle, "size": 11, "color": "94A3B8", "align": "r"}],
            pad=(0, 0, 0, 0)
        )
        # Footer bar
        self.add_rect(0, emu_in(7.15), SLIDE_W, emu_in(0.35), "E2E8F0")
        self.add_textbox(
            emu_in(0.55), emu_in(7.17), emu_in(8.0), emu_in(0.3),
            [{"text": "Kelompok 3 — Sistem Rental Film (Bahasa C) | Mini Project Pemrograman Dasar", "size": 10, "color": "475569"}],
            pad=(0, 0, 0, 0)
        )
        self.add_textbox(
            emu_in(11.0), emu_in(7.17), emu_in(1.75), emu_in(0.3),
            [{"text": f"Slide {slide_no} / 13", "size": 10, "bold": True, "color": "0F172A", "align": "r"}],
            pad=(0, 0, 0, 0)
        )

    def add_card(self, x, y, w, h, title, items, accent_hex="0284C7", bg_hex="FFFFFF", font="Calibri", font_size=13):
        # Card background
        self.add_rect(x, y, w, h, bg_hex, line_hex="CBD5E1", roundness=4000)
        # Top accent stripe
        self.add_rect(x, y, w, emu_in(0.42), accent_hex, roundness=4000)
        self.add_textbox(
            x + emu_in(0.18), y + emu_in(0.05), w - emu_in(0.36), emu_in(0.34),
            [{"text": title, "size": 13, "bold": True, "color": "FFFFFF"}],
            pad=(0, 0, 0, 0), anchor="ctr"
        )
        # Body text
        paras = []
        for it in items:
            if isinstance(it, dict):
                paras.append(it)
            else:
                paras.append({"text": it, "size": font_size, "color": "1E293B", "bullet": True, "font": font, "space_after": 5})
        self.add_textbox(
            x + emu_in(0.15), y + emu_in(0.48), w - emu_in(0.3), h - emu_in(0.55),
            paras
        )

    def to_xml(self):
        shapes_xml = "\n".join(self.shapes)
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgPr>
        <a:solidFill><a:srgbClr val="{self.bg_hex}"/></a:solidFill>
        <a:effectLst/>
      </p:bgPr>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {shapes_xml}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def build_slides():
    slides = []

    # =========================================================================
    # SLIDE 1: HALAMAN SAMPUL (COVER)
    # =========================================================================
    s1 = SlideBuilder(bg_hex="0F172A")
    s1.add_rect(0, 0, emu_in(0.35), SLIDE_H, "38BDF8")
    s1.add_rect(emu_in(0.35), 0, emu_in(0.12), SLIDE_H, "0284C7")

    s1.add_textbox(
        emu_in(1.0), emu_in(0.75), emu_in(4.5), emu_in(0.42),
        [{"text": "LAPORAN MINI PROJECT PEMROGRAMAN DASAR", "size": 12, "bold": True, "color": "0F172A", "align": "ctr"}],
        fill_hex="38BDF8", roundness=20000, anchor="ctr"
    )
    s1.add_textbox(
        emu_in(1.0), emu_in(1.35), emu_in(11.2), emu_in(1.4),
        [
            {"text": "SISTEM RENTAL FILM", "size": 40, "bold": True, "color": "FFFFFF", "space_after": 6},
            {"text": "Implementasi Bahasa C Menggunakan Struktur Kontrol Dasar (Tanpa Array, Struct, & Pointer)", "size": 16, "color": "94A3B8"}
        ],
        pad=(0, 0, 0, 0)
    )

    # Box Kelompok & Anggota
    s1.add_rect(emu_in(1.0), emu_in(2.9), emu_in(6.8), emu_in(3.6), "1E293B", line_hex="334155", roundness=4000)
    s1.add_textbox(
        emu_in(1.25), emu_in(3.1), emu_in(6.3), emu_in(3.3),
        [
            {"text": "KELOMPOK 3 — PEMBAGIAN ANGGOTA", "size": 15, "bold": True, "color": "38BDF8", "space_after": 10},
            {"text": "1. Mahasiswa 1 (NRP: ....................) — Data Pelanggan & Film", "size": 13, "bold": True, "color": "FFFFFF", "space_after": 2},
            {"text": "    Input ID & nama pelanggan, daftar film, validasi pilihan film (do-while)", "size": 11, "color": "CBD5E1", "space_after": 8},
            {"text": "2. Mahasiswa 2 (NRP: ....................) — Proses Sewa & Denda", "size": 13, "bold": True, "color": "FFFFFF", "space_after": 2},
            {"text": "    Biaya sewa, lama pinjam, denda keterlambatan & status (if-else & for)", "size": 11, "color": "CBD5E1", "space_after": 8},
            {"text": "3. Mahasiswa 3 (NRP: ....................) — Transaksi & Pengujian", "size": 13, "bold": True, "color": "FFFFFF", "space_after": 2},
            {"text": "    Bukti rental, status film, uji tepat waktu & terlambat, integrasi program", "size": 11, "color": "CBD5E1", "space_after": 4},
        ],
        pad=(0, 0, 0, 0)
    )

    # Box Identitas Mata Kuliah
    s1.add_rect(emu_in(8.1), emu_in(2.9), emu_in(4.5), emu_in(3.6), "1E293B", line_hex="38BDF8", roundness=4000)
    s1.add_textbox(
        emu_in(8.35), emu_in(3.1), emu_in(4.0), emu_in(3.3),
        [
            {"text": "INFORMASI AKADEMIK", "size": 15, "bold": True, "color": "38BDF8", "space_after": 12},
            {"text": "Mata Kuliah :", "size": 11, "color": "94A3B8", "space_after": 1},
            {"text": "Pemrograman Dasar", "size": 14, "bold": True, "color": "FFFFFF", "space_after": 8},
            {"text": "Dosen Pengampu :", "size": 11, "color": "94A3B8", "space_after": 1},
            {"text": "................................................", "size": 13, "color": "FFFFFF", "space_after": 8},
            {"text": "Program Studi / Institusi :", "size": 11, "color": "94A3B8", "space_after": 1},
            {"text": "................................................", "size": 13, "color": "FFFFFF", "space_after": 8},
            {"text": "Tahun Akademik : 2026", "size": 13, "bold": True, "color": "38BDF8"},
        ],
        pad=(0, 0, 0, 0)
    )
    slides.append(s1)

    # =========================================================================
    # SLIDE 2: BAB I — PENDAHULUAN (LATAR BELAKANG & RUMUSAN MASALAH)
    # =========================================================================
    s2 = SlideBuilder()
    s2.add_header("BAB I", "PENDAHULUAN: LATAR BELAKANG & RUMUSAN MASALAH", "1.1 Latar Belakang & 1.2 Rumusan Masalah", 2)

    s2.add_card(
        emu_in(0.55), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "1.1 Latar Belakang Permasalahan",
        [
            "Proses penyewaan (rental) film secara manual membutuhkan pencatatan identitas pelanggan, pengecekan ketersediaan judul film, serta perhitungan biaya dan denda yang rentan mengalami kesalahan hitung.",
            "Sering terjadi kekeliruan saat menentukan apakah pengembalian film berstatus TEPAT WAKTU atau TERLAMBAT beserta akumulasi denda hariannya.",
            "Oleh karena itu, dibangun program Sistem Rental Film berbasis bahasa C yang terstruktur untuk mengotomatisasi proses pencatatan, validasi input, perhitungan biaya sewa dan denda, hingga pencetakan bukti transaksi."
        ],
        accent_hex="0284C7", font_size=13
    )

    s2.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "1.2 Rumusan Masalah",
        [
            "1. Bagaimana merancang dan membangun program Sistem Rental Film menggunakan bahasa C?",
            "2. Bagaimana melakukan input data pelanggan serta validasi pilihan film menggunakan perulangan do-while?",
            "3. Bagaimana menentukan biaya sewa, menghitung lama peminjaman, menghitung denda keterlambatan, dan menentukan status pengembalian menggunakan if-else dan perulangan?",
            "4. Bagaimana menampilkan bukti rental, memperbarui status film, serta menguji skenario peminjaman tepat waktu dan terlambat?"
        ],
        accent_hex="0F172A", font_size=13
    )
    slides.append(s2)

    # =========================================================================
    # SLIDE 3: BAB I — TUJUAN & BATASAN MASALAH
    # =========================================================================
    s3 = SlideBuilder()
    s3.add_header("BAB I", "PENDAHULUAN: TUJUAN & BATASAN MASALAH", "1.3 Tujuan & 1.4 Batasan Masalah", 3)

    s3.add_card(
        emu_in(0.55), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "1.3 Tujuan Pembuatan Program",
        [
            "1. Membuat program Sistem Rental Film yang fungsional menggunakan bahasa pemrograman C.",
            "2. Menerapkan struktur percabangan if dan if-else untuk penentuan tarif film, status pengembalian, dan denda.",
            "3. Menerapkan struktur perulangan while, do-while, dan for sesuai fungsinya masing-masing.",
            "4. Menerapkan validasi input agar program tahan terhadap masukan yang tidak valid.",
            "5. Mengembangkan kemampuan pembagian tugas dan integrasi kode dalam kerja kelompok."
        ],
        accent_hex="059669", font_size=13
    )

    s3.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "1.4 Batasan Masalah",
        [
            "Program dibuat menggunakan bahasa pemrograman C (Standard Library stdio.h).",
            "Program TIDAK menggunakan array data untuk menyimpan daftar film maupun transaksi.",
            "Program TIDAK menggunakan struct ataupun konsep Object-Oriented Programming (OOP).",
            "Program TIDAK menggunakan pointer (*).",
            "Struktur kontrol yang digunakan dibatasi pada: if, if-else, while, do-while, dan for.",
            "Data ketersediaan film dan transaksi hanya disimpan selama program berjalan (in-memory)."
        ],
        accent_hex="DC2626", font_size=13
    )
    slides.append(s3)

    # =========================================================================
    # SLIDE 4: BAB II — ANALISIS & PERANCANGAN (DESKRIPSI & TABEL IPO)
    # =========================================================================
    s4 = SlideBuilder()
    s4.add_header("BAB II", "ANALISIS & PERANCANGAN: DESKRIPSI SISTEM & IPO", "2.1 Deskripsi Sistem & 2.2 Input - Proses - Output", 4)

    s4.add_card(
        emu_in(0.55), emu_in(1.42), emu_in(12.1), emu_in(1.65),
        "2.1 Deskripsi Singkat Sistem",
        [
            "Program dimulai dengan menampilkan menu utama, lalu menerima input ID dan Nama Pelanggan. Selanjutnya program menampilkan 5 pilihan film beserta harga sewa per hari dan statusnya (Tersedia/Dipinjam), lalu memvalidasi pilihan pelanggan menggunakan do-while. Pelanggan memasukkan durasi sewa (1-7 hari) dan lama peminjaman aktual. Program menghitung biaya sewa, menentukan status pengembalian (TEPAT WAKTU / TERLAMBAT) dengan if-else, menghitung denda keterlambatan bertingkat dengan perulangan for, memvalidasi uang pembayaran, dan mencetak Bukti Rental Film."
        ],
        accent_hex="0F172A", font_size=12
    )

    # Tiga kolom Tabel IPO (2.2)
    s4.add_card(
        emu_in(0.55), emu_in(3.25), emu_in(3.85), emu_in(3.65),
        "INPUT (Masukan)",
        [
            "ID Pelanggan",
            "Nama Pelanggan",
            "Pilihan Nomor Film (1-5)",
            "Durasi Sewa (1-7 hari)",
            "Lama Peminjaman Aktual (hari)",
            "Jumlah Uang Pembayaran (Rp)"
        ],
        accent_hex="0284C7", font_size=12
    )
    s4.add_card(
        emu_in(4.68), emu_in(3.25), emu_in(3.85), emu_in(3.65),
        "PROSES (Pengolahan)",
        [
            "Validasi pilihan film & ketersediaan (do-while)",
            "Menentukan harga sewa film (if-else)",
            "Menghitung biaya sewa = harga x durasi",
            "Menentukan status kembali & hari telat (if-else)",
            "Menghitung denda bertingkat per hari (for)",
            "Menghitung total bayar & kembalian"
        ],
        accent_hex="7C3AED", font_size=12
    )
    s4.add_card(
        emu_in(8.80), emu_in(3.25), emu_in(3.85), emu_in(3.65),
        "OUTPUT (Keluaran)",
        [
            "Tabel Daftar & Status Ketersediaan Film",
            "Bukti Rental Film (ID, Nama, Judul Film)",
            "Rincian Biaya Sewa & Denda Keterlambatan",
            "Total Pembayaran & Uang Kembalian",
            "Status Pengembalian (TEPAT WAKTU / TERLAMBAT)",
            "Status Film Terbaru (Dipinjam / Tersedia)"
        ],
        accent_hex="059669", font_size=12
    )
    slides.append(s4)

    # =========================================================================
    # SLIDE 5: BAB II — ALGORITMA / PSEUDOCODE (2.3)
    # =========================================================================
    s5 = SlideBuilder()
    s5.add_header("BAB II", "ANALISIS & PERANCANGAN: ALGORITMA / PSEUDOCODE", "2.3 Algoritma Program Sistem Rental Film", 5)

    s5.add_card(
        emu_in(0.55), emu_in(1.42), emu_in(5.9), emu_in(5.45),
        "Algoritma Bagian 1: Input & Validasi (Mahasiswa 1 & 2)",
        [
            {"text": "Mulai", "size": 11, "bold": True, "font": "Consolas", "color": "0284C7"},
            {"text": "  Ulangi (do-while transaksi):", "size": 11, "font": "Consolas"},
            {"text": "    Input idPelanggan dan namaPelanggan", "size": 11, "font": "Consolas"},
            {"text": "    Tampilkan daftar 5 film beserta harga & status", "size": 11, "font": "Consolas"},
            {"text": "    Ulangi (do-while validasi film):", "size": 11, "font": "Consolas"},
            {"text": "      Input pilihanFilm (1..5)", "size": 11, "font": "Consolas"},
            {"text": "      Jika pilihanFilm < 1 atau > 5 atau status == Dipinjam:", "size": 11, "font": "Consolas"},
            {"text": "        Tampilkan pesan kesalahan", "size": 11, "font": "Consolas"},
            {"text": "    Selama pilihanFilm tidak valid", "size": 11, "font": "Consolas"},
            {"text": "    Input durasiSewa (validasi 1..7 hari dengan do-while)", "size": 11, "font": "Consolas"},
            {"text": "    Ubah status film terpilih menjadi Dipinjam (0)", "size": 11, "font": "Consolas"},
            {"text": "    Input lamaPinjam aktual (minimal 1 hari)", "size": 11, "font": "Consolas"},
        ],
        accent_hex="0F172A", bg_hex="F1F5F9"
    )

    s5.add_card(
        emu_in(6.75), emu_in(1.42), emu_in(5.9), emu_in(5.45),
        "Algoritma Bagian 2: Perhitungan & Output (Mahasiswa 2 & 3)",
        [
            {"text": "    Tentukan hargaPerHari berdasarkan pilihanFilm (if-else)", "size": 11, "font": "Consolas"},
            {"text": "    biayaSewa = hargaPerHari * durasiSewa", "size": 11, "font": "Consolas"},
            {"text": "    Jika lamaPinjam > durasiSewa Maka:", "size": 11, "font": "Consolas"},
            {"text": "      hariTerlambat = lamaPinjam - durasiSewa", "size": 11, "font": "Consolas"},
            {"text": "      status = TERLAMBAT", "size": 11, "font": "Consolas"},
            {"text": "      Untuk hariKe = 1 sampai hariTerlambat (for):", "size": 11, "font": "Consolas"},
            {"text": "        Jika hariKe <= 3: denda += 5000", "size": 11, "font": "Consolas"},
            {"text": "        Selain itu      : denda += 10000", "size": 11, "font": "Consolas"},
            {"text": "    Selain itu: hariTerlambat = 0, denda = 0, status = TEPAT WAKTU", "size": 11, "font": "Consolas"},
            {"text": "    totalBayar = biayaSewa + denda", "size": 11, "font": "Consolas"},
            {"text": "    Input uangBayar (do-while uangBayar >= totalBayar)", "size": 11, "font": "Consolas"},
            {"text": "    kembalian = uangBayar - totalBayar; Status Film = Tersedia", "size": 11, "font": "Consolas"},
            {"text": "    Tampilkan Bukti Rental & Status Film; Tanya transaksi lagi", "size": 11, "font": "Consolas"},
            {"text": "Selesai", "size": 11, "bold": True, "font": "Consolas", "color": "0284C7"},
        ],
        accent_hex="0284C7", bg_hex="F1F5F9"
    )
    slides.append(s5)

    # =========================================================================
    # SLIDE 6: BAB II — FLOWCHART PROGRAM (2.4)
    # =========================================================================
    s6 = SlideBuilder()
    s6.add_header("BAB II", "ANALISIS & PERANCANGAN: FLOWCHART PROGRAM", "2.4 Alur Eksekusi: Mulai -> Input -> Validasi -> Proses -> Perhitungan -> Output -> Pengulangan -> Selesai", 6)

    flow_steps = [
        ("1. MULAI", "Tampilkan Menu Utama\n(1. Transaksi, 2. Daftar Film,\n3. Pengujian, 0. Keluar)", "0F172A"),
        ("2. INPUT DATA", "Masukkan ID Pelanggan &\nNama Pelanggan;\nTampilkan 5 Pilihan Film", "0284C7"),
        ("3. VALIDASI (do-while)", "Input Pilihan Film (1-5)\n& Durasi Sewa (1-7 hari).\nValid & Tersedia?", "D97706"),
        ("4. PROSES PINJAM", "Set Status Film = Dipinjam;\nInput Lama Peminjaman\nAktual (hari)", "7C3AED"),
        ("5. PERHITUNGAN", "Hitung Biaya Sewa;\nCek Lama > Durasi (if-else);\nHitung Denda Bertingkat (for)", "DC2626"),
        ("6. PEMBAYARAN", "Hitung Total = Biaya + Denda;\nValidasi Uang Bayar >= Total;\nHitung Kembalian", "059669"),
        ("7. OUTPUT BUKTI", "Cetak Bukti Rental Lengkap;\nKembalikan Status Film\nmenjadi Tersedia", "0284C7"),
        ("8. PENGULANGAN / SELESAI", "Transaksi Lagi? (y/t)\nJika 'y' kembali ke Input;\nJika 't' -> SELESAI", "0F172A"),
    ]

    # Baris 1 (Langkah 1 - 4)
    for idx in range(4):
        title, desc, color = flow_steps[idx]
        x = emu_in(0.55 + idx * 3.1)
        y = emu_in(1.65)
        s6.add_card(x, y, emu_in(2.8), emu_in(2.1), title,
                    [{"text": desc, "size": 12, "align": "ctr", "color": "1E293B"}],
                    accent_hex=color)
        if idx < 3:
            s6.add_textbox(x + emu_in(2.8), y + emu_in(0.75), emu_in(0.3), emu_in(0.5),
                           [{"text": "➔", "size": 20, "bold": True, "color": "0284C7", "align": "ctr"}],
                           pad=(0, 0, 0, 0))

    # Panah turun dari langkah 4 ke langkah 5
    s6.add_textbox(emu_in(10.7), emu_in(3.8), emu_in(1.2), emu_in(0.45),
                   [{"text": "⬇ Lanjut", "size": 13, "bold": True, "color": "0284C7", "align": "ctr"}],
                   pad=(0, 0, 0, 0))

    # Baris 2 (Langkah 5 - 8)
    for idx in range(4, 8):
        title, desc, color = flow_steps[idx]
        col = idx - 4
        x = emu_in(0.55 + col * 3.1)
        y = emu_in(4.35)
        s6.add_card(x, y, emu_in(2.8), emu_in(2.1), title,
                    [{"text": desc, "size": 12, "align": "ctr", "color": "1E293B"}],
                    accent_hex=color)
        if col < 3:
            s6.add_textbox(x + emu_in(2.8), y + emu_in(0.75), emu_in(0.3), emu_in(0.5),
                           [{"text": "➔", "size": 20, "bold": True, "color": "0284C7", "align": "ctr"}],
                           pad=(0, 0, 0, 0))
    slides.append(s6)

    # =========================================================================
    # SLIDE 7: BAB III — IMPLEMENTASI PROGRAM (3.1 & 3.2)
    # =========================================================================
    s7 = SlideBuilder()
    s7.add_header("BAB III", "IMPLEMENTASI: LINGKUNGAN & STRUKTUR PROGRAM", "3.1 Lingkungan Pengembangan & 3.2 Struktur Program", 7)

    s7.add_card(
        emu_in(0.55), emu_in(1.45), emu_in(5.4), emu_in(5.4),
        "3.1 Lingkungan Pengembangan",
        [
            "Bahasa Pemrograman : Bahasa C (Standard C99 / C11)",
            "Compiler           : GCC (MinGW-w64) via Terminal",
            "Perintah Kompilasi : gcc -Wall -Wextra -o rental_film.exe rental_film.c",
            "Sistem Operasi     : Microsoft Windows 10 / 11",
            "Text Editor / IDE  : Visual Studio Code",
            "pustaka (Header)   : #include <stdio.h>"
        ],
        accent_hex="0F172A", font_size=13
    )

    s7.add_card(
        emu_in(6.25), emu_in(1.45), emu_in(6.4), emu_in(5.4),
        "3.2 Bagian-Bagian Utama Struktur Program",
        [
            "1. Bagian Input Pelanggan (inputDataPelanggan): Menerima ID dan Nama pelanggan.",
            "2. Bagian Pemilihan & Validasi Film (tampilkanDaftarFilm, inputDanValidasiFilm): Menampilkan 5 film dan memvalidasi pilihan dengan do-while.",
            "3. Bagian Input Durasi & Lama Pinjam (inputDurasiDanLamaPinjam): Menerima durasi sewa (1-7 hari) dan lama pinjam aktual.",
            "4. Bagian Perhitungan Biaya & Denda (hitungSewaDanDenda): Menghitung biaya sewa, mengecek keterlambatan (if-else), dan menghitung denda (for).",
            "5. Bagian Pembayaran (prosesPembayaran): Memvalidasi uang bayar dan menghitung kembalian.",
            "6. Bagian Output (tampilkanBuktiRental, tampilkanStatusSemuaFilm): Mencetak struk bukti rental dan status ketersediaan film.",
            "7. Bagian Pengujian & Pengulangan (pengujianOtomatis, main): Menguji kasus tepat waktu/terlambat dan mengulang transaksi."
        ],
        accent_hex="0284C7", font_size=12
    )
    slides.append(s7)

    # =========================================================================
    # SLIDE 8: BAB III — SOURCE CODE & PENJELASAN KODE (3.3 & 3.4)
    # =========================================================================
    s8 = SlideBuilder()
    s8.add_header("BAB III", "IMPLEMENTASI: CUPLIKAN & PENJELASAN SOURCE CODE", "3.3 Source Code Inti & 3.4 Penjelasan Struktur Kontrol", 8)

    s8.add_card(
        emu_in(0.55), emu_in(1.42), emu_in(6.1), emu_in(5.45),
        "3.3 Cuplikan Kode Inti (rental_film.c)",
        [
            {"text": "/* Validasi pilihan film dengan do-while (Mhs 1) */", "size": 10, "font": "Consolas", "color": "059669"},
            {"text": "do {", "size": 10, "font": "Consolas"},
            {"text": "    printf(\"Pilih nomor film (1-5): \");", "size": 10, "font": "Consolas"},
            {"text": "    hasilBaca = scanf(\"%d\", &pilihanFilm);", "size": 10, "font": "Consolas"},
            {"text": "    if (pilihanFilm < 1 || pilihanFilm > 5)", "size": 10, "font": "Consolas"},
            {"text": "        valid = 0;", "size": 10, "font": "Consolas"},
            {"text": "    else if (cekFilmTersedia(pilihanFilm) == 0)", "size": 10, "font": "Consolas"},
            {"text": "        valid = 0;", "size": 10, "font": "Consolas"},
            {"text": "    else valid = 1;", "size": 10, "font": "Consolas"},
            {"text": "} while (valid == 0);", "size": 10, "font": "Consolas", "space_after": 6},
            {"text": "/* Perhitungan denda dengan for & if-else (Mhs 2) */", "size": 10, "font": "Consolas", "color": "059669"},
            {"text": "denda = 0;", "size": 10, "font": "Consolas"},
            {"text": "for (hariKe = 1; hariKe <= hariTerlambat; hariKe++) {", "size": 10, "font": "Consolas"},
            {"text": "    if (hariKe <= 3) denda = denda + 5000;", "size": 10, "font": "Consolas"},
            {"text": "    else             denda = denda + 10000;", "size": 10, "font": "Consolas"},
            {"text": "}", "size": 10, "font": "Consolas"},
        ],
        accent_hex="0F172A", bg_hex="F1F5F9"
    )

    s8.add_card(
        emu_in(6.85), emu_in(1.42), emu_in(5.8), emu_in(5.45),
        "3.4 Penjelasan Komponen Kode Program",
        [
            "if & if-else : Memilih judul/harga film (1-5), menentukan status TEPAT WAKTU vs TERLAMBAT, serta membedakan tarif denda hari ke-1..3 (Rp 5.000) dan hari ke-4 dst (Rp 10.000).",
            "while : Digunakan pada fungsi bersihkanInput() untuk membuang sisa karakter newline di buffer stdin.",
            "do-while : Mengulang menu utama, perulangan transaksi, serta validasi input nomor film, durasi sewa, dan uang pembayaran.",
            "for : Mengakumulasi denda per hari keterlambatan dan menampilkan daftar status kelima film.",
            "Variabel & Operator : Menggunakan tipe int, long, char; operator aritmatika (*, +, -), relasional (<, >, <=, ==), dan logika (||, &&).",
            "Input / Output : Menggunakan printf() dan scanf() dari <stdio.h>."
        ],
        accent_hex="0284C7", font_size=12
    )
    slides.append(s8)

    # =========================================================================
    # SLIDE 9: BAB IV — PEMBAGIAN KONTRIBUSI ANGGOTA (4.1, 4.2, 4.3)
    # =========================================================================
    s9 = SlideBuilder()
    s9.add_header("BAB IV", "PEMBAGIAN KONTRIBUSI ANGGOTA KELOMPOK 3", "4.1 Mahasiswa 1, 4.2 Mahasiswa 2, dan 4.3 Mahasiswa 3", 9)

    s9.add_card(
        emu_in(0.55), emu_in(1.45), emu_in(3.85), emu_in(5.4),
        "4.1 Mahasiswa 1 — Data & Film",
        [
            "Nama / NRP : ................................",
            "Tugas Utama:",
            "• Input ID dan nama pelanggan",
            "• Menampilkan daftar pilihan film",
            "• Input & validasi pilihan film",
            "• Menerapkan perulangan do-while",
            "Fungsi yang Dikerjakan:",
            "• inputDataPelanggan()",
            "• tampilkanDaftarFilm()",
            "• inputDanValidasiFilm()",
            "Integrasi: Menyediakan data pelanggan & film valid untuk diproses Mahasiswa 2."
        ],
        accent_hex="0284C7", font_size=11
    )

    s9.add_card(
        emu_in(4.68), emu_in(1.45), emu_in(3.85), emu_in(5.4),
        "4.2 Mahasiswa 2 — Sewa & Denda",
        [
            "Nama / NRP : ................................",
            "Tugas Utama:",
            "• Menentukan biaya sewa film",
            "• Menghitung lama peminjaman",
            "• Menghitung denda keterlambatan",
            "• Menentukan status pengembalian",
            "• Menerapkan if-else & perulangan for",
            "Fungsi yang Dikerjakan:",
            "• inputDurasiDanLamaPinjam()",
            "• hitungSewaDanDenda()",
            "• prosesPembayaran()",
            "Integrasi: Mengolah biaya, denda, & status untuk dicetak Mahasiswa 3."
        ],
        accent_hex="7C3AED", font_size=11
    )

    s9.add_card(
        emu_in(8.80), emu_in(1.45), emu_in(3.85), emu_in(5.4),
        "4.3 Mahasiswa 3 — Output & Uji",
        [
            "Nama / NRP : ................................",
            "Tugas Utama:",
            "• Menampilkan bukti rental lengkap",
            "• Menampilkan rincian biaya & denda",
            "• Menampilkan status ketersediaan film",
            "• Menguji tepat waktu & terlambat",
            "• Mengintegrasikan seluruh program",
            "Fungsi yang Dikerjakan:",
            "• tampilkanBuktiRental()",
            "• tampilkanStatusSemuaFilm()",
            "• pengujianOtomatis() & main()",
            "Integrasi: Menyatukan modul Mhs 1 & 2 dalam menu utama interaktif."
        ],
        accent_hex="059669", font_size=11
    )
    slides.append(s9)

    # =========================================================================
    # SLIDE 10: BAB V — PENGUJIAN PROGRAM (5.1 SKENARIO PENGUJIAN)
    # =========================================================================
    s10 = SlideBuilder()
    s10.add_header("BAB V", "PENGUJIAN PROGRAM: 5 SKENARIO PENGUJIAN", "5.1 Tabel Skenario Pengujian (Valid, Tidak Valid, Nilai Batas, Pembayaran)", 10)

    scenarios = [
        ("1. Input Valid (Tepat Waktu)",
         "Film = 1 (Rp 8.000), Durasi = 3 hari, Lama Pinjam = 3 hari",
         "Diharapkan: Biaya Rp 24.000, Denda Rp 0, Status TEPAT WAKTU",
         "Aktual: Biaya Rp 24.000, Denda Rp 0, Status TEPAT WAKTU  [BERHASIL]",
         "059669"),
        ("2. Pilihan Film Tidak Valid",
         "Input pilihanFilm = 9 (di luar rentang 1 s/d 5)",
         "Diharapkan: Muncul pesan '[!] Error: Pilihan film tidak valid!' & minta ulang",
         "Aktual: Pesan error tampil dan do-while meminta input ulang  [BERHASIL]",
         "0284C7"),
        ("3. Nilai Batas & Terlambat",
         "Film = 5 (Rp 9.000), Durasi = 2 hari, Lama = 7 hari (Telat 5 hari)",
         "Diharapkan: Biaya Rp 18.000, Denda Rp 35.000 (3x5rb + 2x10rb), Total Rp 53.000",
         "Aktual: Biaya Rp 18.000, Denda Rp 35.000, Total Rp 53.000, TERLAMBAT  [BERHASIL]",
         "7C3AED"),
        ("4. Pembayaran Kurang",
         "Total Tagihan = Rp 24.000, Input uangBayar = Rp 10.000",
         "Diharapkan: Pembayaran ditolak & diminta memasukkan nominal yang cukup",
         "Aktual: Muncul '[!] Error: Uang pembayaran kurang!' & diulang  [BERHASIL]",
         "D97706"),
        ("5. Pembayaran Lebih (Kembalian)",
         "Total Tagihan = Rp 24.000, Input uangBayar = Rp 30.000",
         "Diharapkan: Pembayaran diterima & Kembalian dihitung Rp 6.000",
         "Aktual: Kembalian tercetak Rp 6.000 pada Bukti Rental  [BERHASIL]",
         "0F172A"),
    ]

    for idx, (sc_title, sc_in, sc_exp, sc_act, color) in enumerate(scenarios):
        y = emu_in(1.40 + idx * 1.10)
        s10.add_rect(emu_in(0.55), y, emu_in(12.1), emu_in(1.0), "FFFFFF", line_hex="CBD5E1", roundness=3000)
        s10.add_rect(emu_in(0.55), y, emu_in(2.85), emu_in(1.0), color, roundness=3000)
        s10.add_textbox(emu_in(0.65), y + emu_in(0.1), emu_in(2.65), emu_in(0.8),
                        [{"text": sc_title, "size": 12, "bold": True, "color": "FFFFFF", "align": "ctr"}],
                        anchor="ctr", pad=(0, 0, 0, 0))
        s10.add_textbox(emu_in(3.55), y + emu_in(0.08), emu_in(9.0), emu_in(0.85),
                        [
                            {"text": f"Input      : {sc_in}", "size": 11, "bold": True, "color": "0F172A", "space_after": 2},
                            {"text": f"{sc_exp}", "size": 11, "color": "475569", "space_after": 2},
                            {"text": f"{sc_act}", "size": 11, "bold": True, "color": "059669", "space_after": 0},
                        ],
                        pad=(0, 0, 0, 0))
    slides.append(s10)

    # =========================================================================
    # SLIDE 11: BAB V — BUKTI PENGUJIAN PROGRAM (5.2 OUTPUT TERMINAL)
    # =========================================================================
    s11 = SlideBuilder()
    s11.add_header("BAB V", "BUKTI PENGUJIAN: OUTPUT TEPAT WAKTU & TERLAMBAT", "5.2 Bukti Running Program pada Menu Pengujian Otomatis", 11)

    s11.add_card(
        emu_in(0.55), emu_in(1.42), emu_in(5.9), emu_in(5.45),
        "Pengujian 1 — Peminjaman Tepat Waktu",
        [
            {"text": "================================================", "size": 10, "font": "Consolas", "color": "38BDF8"},
            {"text": "               BUKTI RENTAL FILM", "size": 10, "bold": True, "font": "Consolas", "color": "FFFFFF"},
            {"text": "================================================", "size": 10, "font": "Consolas", "color": "38BDF8"},
            {"text": "ID Pelanggan      : P001", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Nama Pelanggan    : Budi Santoso", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Film Disewa       : Avengers: Endgame (F001)", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Harga Sewa / Hari : Rp 8000", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Durasi Sewa       : 3 hari", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Lama Peminjaman   : 3 hari (Terlambat: 0 hari)", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "------------------------------------------------", "size": 10, "font": "Consolas", "color": "64748B"},
            {"text": "Biaya Sewa        : Rp 24000", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Denda Terlambat   : Rp 0", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "TOTAL BAYAR       : Rp 24000 (Bayar: Rp 30000)", "size": 10, "bold": True, "font": "Consolas", "color": "4ADE80"},
            {"text": "Kembalian         : Rp 6000", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Status Kembali    : TEPAT WAKTU", "size": 10, "bold": True, "font": "Consolas", "color": "4ADE80"},
            {"text": "Status Film       : Tersedia (Sudah Dikembalikan)", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": ">> HASIL UJI 1 (TEPAT WAKTU): BERHASIL / LULUS", "size": 10, "bold": True, "font": "Consolas", "color": "38BDF8"},
        ],
        accent_hex="059669", bg_hex="0F172A"
    )

    s11.add_card(
        emu_in(6.75), emu_in(1.42), emu_in(5.9), emu_in(5.45),
        "Pengujian 2 — Peminjaman Terlambat",
        [
            {"text": "================================================", "size": 10, "font": "Consolas", "color": "F87171"},
            {"text": "               BUKTI RENTAL FILM", "size": 10, "bold": True, "font": "Consolas", "color": "FFFFFF"},
            {"text": "================================================", "size": 10, "font": "Consolas", "color": "F87171"},
            {"text": "ID Pelanggan      : P002", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Nama Pelanggan    : Siti Aminah", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Film Disewa       : Interstellar (F005)", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Harga Sewa / Hari : Rp 9000", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Durasi Sewa       : 2 hari", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Lama Peminjaman   : 7 hari (Terlambat: 5 hari)", "size": 10, "font": "Consolas", "color": "FCA5A5"},
            {"text": "------------------------------------------------", "size": 10, "font": "Consolas", "color": "64748B"},
            {"text": "Biaya Sewa        : Rp 18000", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Denda Terlambat   : Rp 35000 (3x5rb + 2x10rb)", "size": 10, "font": "Consolas", "color": "FCA5A5"},
            {"text": "TOTAL BAYAR       : Rp 53000 (Bayar: Rp 60000)", "size": 10, "bold": True, "font": "Consolas", "color": "FBBF24"},
            {"text": "Kembalian         : Rp 7000", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": "Status Kembali    : TERLAMBAT", "size": 10, "bold": True, "font": "Consolas", "color": "F87171"},
            {"text": "Status Film       : Tersedia (Sudah Dikembalikan)", "size": 10, "font": "Consolas", "color": "E2E8F0"},
            {"text": ">> HASIL UJI 2 (TERLAMBAT)  : BERHASIL / LULUS", "size": 10, "bold": True, "font": "Consolas", "color": "38BDF8"},
        ],
        accent_hex="DC2626", bg_hex="0F172A"
    )
    slides.append(s11)

    # =========================================================================
    # SLIDE 12: BAB VI — HASIL, PEMBAHASAN, KENDALA & SOLUSI
    # =========================================================================
    s12 = SlideBuilder()
    s12.add_header("BAB VI", "HASIL DAN PEMBAHASAN: STRUKTUR KONTROL & SOLUSI", "6.1 Hasil Program, 6.2 Penerapan Struktur Kontrol, & 6.3 Kendala dan Solusi", 12)

    s12.add_card(
        emu_in(0.55), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "6.1 Hasil & 6.2 Penerapan Struktur Kontrol",
        [
            "Hasil Program: Program berhasil berjalan secara interaktif, memvalidasi input, menghitung sewa & denda, dan menampilkan bukti rental dengan tepat.",
            "if : Mengecek validitas input dan kecukupan pembayaran.",
            "if-else : Menentukan harga film (1-5), menentukan status TEPAT WAKTU vs TERLAMBAT, dan memilih tarif denda harian.",
            "while : Membersihkan sisa karakter input pada buffer stdin.",
            "do-while : Mengulang input saat tidak valid & mengulang transaksi.",
            "for : Mengakumulasi denda per hari keterlambatan & mencetak daftar film."
        ],
        accent_hex="0284C7", font_size=12
    )

    s12.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "6.3 Kendala dan Solusi Selama Pengerjaan",
        [
            "Kendala 1: Input pilihan film di luar nomor 1-5 atau film sedang dipinjam.",
            "Solusi 1 : Menambahkan validasi bertingkat di dalam perulangan do-while.",
            "Kendala 2: Menyimpan status 5 film tanpa menggunakan array maupun struct.",
            "Solusi 2 : Menggunakan 5 variabel global (film1_tersedia s/d film5_tersedia) dan fungsi pemilihan if-else.",
            "Kendala 3: Uang pembayaran kurang dari total biaya sewa + denda.",
            "Solusi 3 : Menambahkan pengecekan if (uangBayar < totalBayar) di dalam do-while agar pengguna mengulang pembayaran.",
            "Kendala 4: Program langsung tertutup setelah 1 transaksi selesai.",
            "Solusi 4 : Membungkus menu utama dan transaksi dengan perulangan do-while."
        ],
        accent_hex="7C3AED", font_size=12
    )
    slides.append(s12)

    # =========================================================================
    # SLIDE 13: BAB VII — KESIMPULAN, SARAN & DAFTAR PUSTAKA
    # =========================================================================
    s13 = SlideBuilder()
    s13.add_header("BAB VII", "KESIMPULAN, SARAN PENGEMBANGAN & REFERENSI", "7.1 Kesimpulan, 7.2 Saran Pengembangan, & Daftar Pustaka", 13)

    s13.add_card(
        emu_in(0.55), emu_in(1.45), emu_in(5.9), emu_in(3.3),
        "7.1 Kesimpulan",
        [
            "Seluruh tujuan mini project telah tercapai dengan baik.",
            "Program Sistem Rental Film dalam bahasa C berhasil menerapkan struktur kontrol if, if-else, while, do-while, dan for tanpa menggunakan array data, struct, maupun pointer.",
            "Kolaborasi Mahasiswa 1, 2, dan 3 terintegrasi dengan baik dan seluruh skenario pengujian (Tepat Waktu & Terlambat) dinyatakan LULUS."
        ],
        accent_hex="059669", font_size=12
    )

    s13.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(3.3),
        "7.2 Saran Pengembangan (Tahap Berikutnya)",
        [
            "Menggunakan ARRAY untuk menampung lebih banyak katalog film dan riwayat transaksi pelanggan secara dinamis.",
            "Menggunakan STRUCT untuk mengelompokkan data Pelanggan, Film, dan Transaksi agar kode lebih rapi dan modular.",
            "Menggunakan POINTER untuk manipulasi data antar-fungsi secara efisien serta penyimpanan ke file eksternal."
        ],
        accent_hex="0284C7", font_size=12
    )

    s13.add_card(
        emu_in(0.55), emu_in(4.95), emu_in(12.1), emu_in(1.9),
        "Daftar Pustaka",
        [
            "1. Kernighan, B. W., & Ritchie, D. M. (1988). The C Programming Language (2nd ed.). Prentice Hall.",
            "2. Modul Praktikum & Materi Kuliah Pemrograman Dasar Tahun 2026.",
            "3. Dokumentasi C Standard Library (<stdio.h>) — https://en.cppreference.com/w/c"
        ],
        accent_hex="0F172A", font_size=12
    )
    slides.append(s13)

    return slides


def create_pptx(filename, slides):
    num_slides = len(slides)

    # 1. [Content_Types].xml
    slide_overrides = "\n".join(
        f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, num_slides + 1)
    )
    content_types_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>
  <Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>
  <Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>
{slide_overrides}
</Types>"""

    # 2. _rels/.rels
    root_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

    # 3. ppt/presentation.xml
    sld_id_entries = "\n".join(
        f'    <p:sldId id="{255 + i}" r:id="rId{i + 1}"/>'
        for i in range(1, num_slides + 1)
    )
    presentation_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
                saveSubsetFonts="1">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
{sld_id_entries}
  </p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="custom"/>
  <p:notesSz cx="{SLIDE_H}" cy="{SLIDE_W}"/>
</p:presentation>"""

    # 4. ppt/_rels/presentation.xml.rels
    slide_rels = "\n".join(
        f'  <Relationship Id="rId{i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, num_slides + 1)
    )
    p_top = num_slides + 2
    pres_rels_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
{slide_rels}
  <Relationship Id="rId{p_top}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>
  <Relationship Id="rId{p_top + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps" Target="viewProps.xml"/>
  <Relationship Id="rId{p_top + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
  <Relationship Id="rId{p_top + 3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles" Target="tableStyles.xml"/>
</Relationships>"""

    # 5. Slide Master & Layout
    slide_master_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg>
      <p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef>
    </p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
  </p:sldLayoutIdLst>
</p:sldMaster>"""

    slide_master_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""

    slide_layout_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             type="blank" preserve="1">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""

    slide_layout_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""

    slide_rel_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>"""

    theme_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme">
  <a:themeElements>
    <a:clrScheme name="Office">
      <a:dk1><a:srgbClr val="0F172A"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1E293B"/></a:dk2>
      <a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>
      <a:accent1><a:srgbClr val="0284C7"/></a:accent1>
      <a:accent2><a:srgbClr val="059669"/></a:accent2>
      <a:accent3><a:srgbClr val="7C3AED"/></a:accent3>
      <a:accent4><a:srgbClr val="D97706"/></a:accent4>
      <a:accent5><a:srgbClr val="DC2626"/></a:accent5>
      <a:accent6><a:srgbClr val="38BDF8"/></a:accent6>
      <a:hlink><a:srgbClr val="0284C7"/></a:hlink>
      <a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Office">
      <a:majorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="25400"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="38100"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>"""

    pres_props_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presProps xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>"""

    view_props_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:viewProps xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>"""

    table_styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>"""

    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", root_rels_xml)
        zf.writestr("ppt/presentation.xml", presentation_xml)
        zf.writestr("ppt/_rels/presentation.xml.rels", pres_rels_xml)
        zf.writestr("ppt/presProps.xml", pres_props_xml)
        zf.writestr("ppt/viewProps.xml", view_props_xml)
        zf.writestr("ppt/tableStyles.xml", table_styles_xml)
        zf.writestr("ppt/theme/theme1.xml", theme_xml)
        zf.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml)
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels_xml)
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml)
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels_xml)

        for idx, slide in enumerate(slides, start=1):
            zf.writestr(f"ppt/slides/slide{idx}.xml", slide.to_xml())
            zf.writestr(f"ppt/slides/_rels/slide{idx}.xml.rels", slide_rel_xml)

    print(f"Berhasil membuat {filename} ({num_slides} slide)!")


if __name__ == "__main__":
    all_slides = build_slides()
    create_pptx(OUTPUT_FILE, all_slides)
