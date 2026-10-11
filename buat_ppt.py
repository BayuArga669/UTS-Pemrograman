# -*- coding: utf-8 -*-
"""
Generator PowerPoint (.pptx) Murni menggunakan Python Standard Library (zipfile + XML).
Menghasilkan file Presentasi_Rental_Film_Kelompok_3.pptx (16:9 Widescreen)
yang disesuaikan 100% dengan kode rental_film.c milik Kelompok 3.
"""

import zipfile
from xml.sax.saxutils import escape

OUTPUT_FILE = "Presentasi_Rental_Film_Kelompok_3.pptx"

# Ukuran slide 16:9 dalam EMU (13.333 x 7.5 inch)
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
        self.add_rect(0, 0, SLIDE_W, emu_in(1.15), "0F172A")
        self.add_rect(0, emu_in(1.15), SLIDE_W, emu_in(0.06), "38BDF8")
        self.add_textbox(
            emu_in(0.55), emu_in(0.18), emu_in(2.4), emu_in(0.32),
            [{"text": bab_label, "size": 11, "bold": True, "color": "0F172A", "align": "ctr"}],
            fill_hex="38BDF8", roundness=25000, anchor="ctr", pad=(30000, 10000, 30000, 10000)
        )
        self.add_textbox(
            emu_in(0.55), emu_in(0.52), emu_in(10.5), emu_in(0.55),
            [{"text": title, "size": 22, "bold": True, "color": "FFFFFF"}],
            pad=(0, 0, 0, 0)
        )
        self.add_textbox(
            emu_in(8.2), emu_in(0.18), emu_in(4.55), emu_in(0.35),
            [{"text": subtitle, "size": 11, "color": "94A3B8", "align": "r"}],
            pad=(0, 0, 0, 0)
        )
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
        self.add_rect(x, y, w, h, bg_hex, line_hex="CBD5E1", roundness=4000)
        self.add_rect(x, y, w, emu_in(0.42), accent_hex, roundness=4000)
        self.add_textbox(
            x + emu_in(0.18), y + emu_in(0.05), w - emu_in(0.36), emu_in(0.34),
            [{"text": title, "size": 13, "bold": True, "color": "FFFFFF"}],
            pad=(0, 0, 0, 0), anchor="ctr"
        )
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
            {"text": "Implementasi Bahasa C Menggunakan do-while, switch-case, dan if-else (Tanpa Array Data, Struct, & Pointer)", "size": 15, "color": "94A3B8"}
        ],
        pad=(0, 0, 0, 0)
    )

    s1.add_rect(emu_in(1.0), emu_in(2.9), emu_in(6.8), emu_in(3.6), "1E293B", line_hex="334155", roundness=4000)
    s1.add_textbox(
        emu_in(1.25), emu_in(3.1), emu_in(6.3), emu_in(3.3),
        [
            {"text": "KELOMPOK 3 — PEMBAGIAN ANGGOTA", "size": 15, "bold": True, "color": "38BDF8", "space_after": 10},
            {"text": "1. Mahasiswa 1 (NRP: ....................) — Data Pelanggan & Film", "size": 13, "bold": True, "color": "FFFFFF", "space_after": 2},
            {"text": "    Input ID & nama pelanggan, daftar 5 film, validasi pilihan film (do-while & switch)", "size": 11, "color": "CBD5E1", "space_after": 8},
            {"text": "2. Mahasiswa 2 (NRP: ....................) — Proses Sewa & Denda", "size": 13, "bold": True, "color": "FFFFFF", "space_after": 2},
            {"text": "    Input lama pinjam, opsi perpanjangan (y/n), hitung biaya sewa, denda & status (if-else)", "size": 11, "color": "CBD5E1", "space_after": 8},
            {"text": "3. Mahasiswa 3 (NRP: ....................) — Transaksi & Pengujian", "size": 13, "bold": True, "color": "FFFFFF", "space_after": 2},
            {"text": "    Menampilkan bukti rental, biaya, denda, total bayar, status, & pengujian program", "size": 11, "color": "CBD5E1", "space_after": 4},
        ],
        pad=(0, 0, 0, 0)
    )

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
            "Proses penyewaan film secara manual membutuhkan pencatatan data pelanggan, pemilihan film yang tersedia, serta perhitungan biaya sewa dan denda keterlambatan secara terstruktur.",
            "Selain itu, pelanggan terkadang membutuhkan perpanjangan masa sewa sebelum mengembalikan film.",
            "Oleh karena itu, dibuat program sederhana menggunakan bahasa C untuk membantu proses transaksi rental film mulai dari validasi ketersediaan film hingga pencetakan bukti rental."
        ],
        accent_hex="0284C7", font_size=13
    )

    s2.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "1.2 Rumusan Masalah",
        [
            "1. Bagaimana membuat program Sistem Rental Film menggunakan bahasa C?",
            "2. Bagaimana melakukan input data pelanggan serta validasi pilihan dan ketersediaan stok film menggunakan do-while?",
            "3. Bagaimana menentukan biaya sewa, perpanjangan lama peminjaman, denda keterlambatan (Rp2.000/hari), dan status pengembalian menggunakan if-else?",
            "4. Bagaimana menampilkan bukti rental lengkap serta menguji skenario peminjaman tepat waktu dan terlambat?"
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
            "1. Membuat program Sistem Rental Film menggunakan bahasa C.",
            "2. Menerapkan struktur percabangan if, if-else, dan switch-case.",
            "3. Menerapkan struktur perulangan do-while untuk validasi input pilihan film.",
            "4. Menghitung biaya sewa, perpanjangan durasi, dan denda keterlambatan secara tepat.",
            "5. Mengembangkan kemampuan bekerja sama dan integrasi kode dalam kelompok."
        ],
        accent_hex="059669", font_size=13
    )

    s3.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "1.4 Batasan Masalah",
        [
            "Program dibuat menggunakan bahasa C (<stdio.h> dan <string.h>).",
            "Program TIDAK menggunakan array untuk menyimpan daftar film (menggunakan #define konstanta).",
            "Program TIDAK menggunakan struct maupun konsep OOP.",
            "Program TIDAK menggunakan pointer.",
            "Struktur kontrol yang digunakan adalah do-while, switch-case, if, dan if-else.",
            "Denda keterlambatan ditetapkan sebesar Rp2.000 per hari keterlambatan."
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
            "Program dimulai dengan menerima input ID dan nama pelanggan, lalu menampilkan daftar 5 film beserta biaya/hari dan status ketersediaannya (Tersedia/Dipinjam). Pelanggan memilih nomor film (1-5) dan program memvalidasi pilihan menggunakan do-while & switch-case (jika stok = 0 seperti Interstellar, pelanggan diminta memilih ulang). Selanjutnya pelanggan memasukkan lama peminjaman, opsi perpanjangan (y/n), dan hari pengembalian. Program menghitung biaya sewa, mengecek keterlambatan (if-else) dengan denda Rp2.000/hari, lalu mencetak Bukti Rental."
        ],
        accent_hex="0F172A", font_size=12
    )

    s4.add_card(
        emu_in(0.55), emu_in(3.25), emu_in(3.85), emu_in(3.65),
        "INPUT (Masukan)",
        [
            "ID Pelanggan (id)",
            "Nama Pelanggan (nama)",
            "Pilihan Nomor Film 1-5 (pilih)",
            "Lama Peminjaman Awal (lama)",
            "Opsi Perpanjang y/n (jawab & tambah)",
            "Hari Pengembalian Film (hariKembali)"
        ],
        accent_hex="0284C7", font_size=12
    )
    s4.add_card(
        emu_in(4.68), emu_in(3.25), emu_in(3.85), emu_in(3.65),
        "PROSES (Pengolahan)",
        [
            "Validasi nomor film & cek STOK (do-while & switch)",
            "Menentukan judul & harga film terpilih",
            "Menambah lama pinjam jika diperpanjang (if)",
            "Menghitung biaya = harga * lama",
            "Cek hariKembali > lama (if-else)",
            "Hitung denda = (hariKembali - lama) * 2000"
        ],
        accent_hex="7C3AED", font_size=12
    )
    s4.add_card(
        emu_in(8.80), emu_in(3.25), emu_in(3.85), emu_in(3.65),
        "OUTPUT (Keluaran)",
        [
            "Tabel Daftar Film (No, Nama, Biaya/Hari, Status)",
            "Konfirmasi Film Terpilih & Harga/Hari",
            "Bukti Rental: ID / Nama Pelanggan, Judul Film",
            "Lama Pinjam & Hari Dikembalikan",
            "Biaya Sewa, Denda, & Total Bayar (biaya + denda)",
            "Status Pengembalian (Tepat waktu / Terlambat)"
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
        "Algoritma Bagian 1: Data Pelanggan & Validasi Film",
        [
            {"text": "Mulai", "size": 11, "bold": True, "font": "Consolas", "color": "0284C7"},
            {"text": "  Input id pelanggan dan nama pelanggan", "size": 11, "font": "Consolas"},
            {"text": "  Tampilkan tabel 5 film (JUDUL1..5, HARGA1..5, STOK1..5)", "size": 11, "font": "Consolas"},
            {"text": "  Ulangi (do-while !valid):", "size": 11, "font": "Consolas"},
            {"text": "    valid = 0", "size": 11, "font": "Consolas"},
            {"text": "    Input pilih (nomor film 1-5)", "size": 11, "font": "Consolas"},
            {"text": "    Pilih kasus (switch pilih):", "size": 11, "font": "Consolas"},
            {"text": "      Kasus 1..5:", "size": 11, "font": "Consolas"},
            {"text": "        Jika STOK tersedia Maka:", "size": 11, "font": "Consolas"},
            {"text": "          Salin judul film & simpan harga; valid = 1", "size": 11, "font": "Consolas"},
            {"text": "        Jika tidak:", "size": 11, "font": "Consolas"},
            {"text": "          Tampilkan 'Film sedang dipinjam, pilih yang lain!'", "size": 11, "font": "Consolas"},
            {"text": "      Default: Tampilkan 'Nomor tidak valid, ulangi!'", "size": 11, "font": "Consolas"},
            {"text": "  Selama valid == 0", "size": 11, "font": "Consolas"},
        ],
        accent_hex="0F172A", bg_hex="F1F5F9"
    )

    s5.add_card(
        emu_in(6.75), emu_in(1.42), emu_in(5.9), emu_in(5.45),
        "Algoritma Bagian 2: Proses Sewa, Denda, & Bukti Rental",
        [
            {"text": "  Tampilkan judul film dan harga terpilih", "size": 11, "font": "Consolas"},
            {"text": "  Input lama peminjaman (hari)", "size": 11, "font": "Consolas"},
            {"text": "  Input jawab ('Perpanjang peminjaman? y/n')", "size": 11, "font": "Consolas"},
            {"text": "  Jika jawab == 'y' atau 'Y' Maka:", "size": 11, "font": "Consolas"},
            {"text": "    Input tambah hari; lama = lama + tambah", "size": 11, "font": "Consolas"},
            {"text": "  Input hariKembali ('Film dikembalikan pada hari ke-')", "size": 11, "font": "Consolas"},
            {"text": "  biaya = harga * lama", "size": 11, "font": "Consolas"},
            {"text": "  Jika hariKembali > lama Maka:", "size": 11, "font": "Consolas"},
            {"text": "    denda = (hariKembali - lama) * 2000", "size": 11, "font": "Consolas"},
            {"text": "    status = 'Terlambat'", "size": 11, "font": "Consolas"},
            {"text": "  Selain itu:", "size": 11, "font": "Consolas"},
            {"text": "    denda = 0; status = 'Tepat waktu'", "size": 11, "font": "Consolas"},
            {"text": "  Tampilkan Bukti Rental (biaya, denda, total, status)", "size": 11, "font": "Consolas"},
            {"text": "Selesai", "size": 11, "bold": True, "font": "Consolas", "color": "0284C7"},
        ],
        accent_hex="0284C7", bg_hex="F1F5F9"
    )
    slides.append(s5)

    # =========================================================================
    # SLIDE 6: BAB II — FLOWCHART PROGRAM (2.4)
    # =========================================================================
    s6 = SlideBuilder()
    s6.add_header("BAB II", "ANALISIS & PERANCANGAN: FLOWCHART PROGRAM", "2.4 Alur: Mulai -> Input -> Validasi (do-while) -> Perpanjangan -> Perhitungan -> Output -> Selesai", 6)

    flow_steps = [
        ("1. MULAI & INPUT", "Input ID (id) &\nNama Pelanggan (nama);\nTampilkan Daftar 5 Film", "0F172A"),
        ("2. PILIH FILM", "Masukkan Nomor Film\n(pilih 1-5) di dalam\nperulangan do-while", "0284C7"),
        ("3. VALIDASI STOK", "Cek switch(pilih) & STOK:\nJika valid & tersedia -> Lanjut\nJika tidak -> Ulangi input", "D97706"),
        ("4. LAMA PINJAM", "Input lama peminjaman;\nTanya Perpanjang? (y/n)\nJika 'y': lama += tambah", "7C3AED"),
        ("5. HARI KEMBALI", "Input hariKembali;\nHitung biaya = harga * lama", "0284C7"),
        ("6. CEK TERLAMBAT", "Apakah hariKembali > lama?\nYa: denda=(hariKembali-lama)*2000\nTidak: denda = 0", "DC2626"),
        ("7. STATUS KEMBALI", "Ya -> status = 'Terlambat'\nTidak -> status = 'Tepat waktu'\nHitung Total = biaya + denda", "059669"),
        ("8. BUKTI & SELESAI", "Cetak BUKTI RENTAL\nlengkap ke layar\n-> SELESAI", "0F172A"),
    ]

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

    s6.add_textbox(emu_in(10.7), emu_in(3.8), emu_in(1.2), emu_in(0.45),
                   [{"text": "⬇ Lanjut", "size": 13, "bold": True, "color": "0284C7", "align": "ctr"}],
                   pad=(0, 0, 0, 0))

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
            "Bahasa Pemrograman : Bahasa C",
            "Compiler / IDE     : GCC (MinGW) / Visual Studio Code",
            "Sistem Operasi     : Microsoft Windows 10 / 11",
            "Header Library     : <stdio.h> dan <string.h>",
            "Konstanta Makro    : #define JUDUL1..5, HARGA1..5, STOK1..5, DENDA_PER_HARI 2000"
        ],
        accent_hex="0F172A", font_size=13
    )

    s7.add_card(
        emu_in(6.25), emu_in(1.45), emu_in(6.4), emu_in(5.4),
        "3.2 Struktur Bagian Utama Program",
        [
            "1. Definisi Data Film (#define): Menyimpan judul, harga sewa, dan status stok 5 film serta tarif denda Rp2.000/hari.",
            "2. Bagian Input Pelanggan (Mahasiswa 1): Menerima input ID pelanggan (int) dan Nama pelanggan (char[]).",
            "3. Bagian Daftar & Validasi Film (Mahasiswa 1): Menampilkan tabel 5 film dan memvalidasi pilihan dengan do-while & switch-case.",
            "4. Bagian Lama Sewa & Perpanjangan (Mahasiswa 2): Menerima lama pinjam dan opsi perpanjangan durasi (if jawab == 'y').",
            "5. Bagian Perhitungan Biaya & Denda (Mahasiswa 2): Menghitung biaya sewa dan mengecek keterlambatan (if-else hariKembali > lama).",
            "6. Bagian Output Bukti Rental (Mahasiswa 3): Menampilkan struk bukti rental lengkap beserta total bayar dan status."
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
            {"text": "/* Validasi pilihan film (do-while & switch) */", "size": 10, "font": "Consolas", "color": "059669"},
            {"text": "do {", "size": 10, "font": "Consolas"},
            {"text": "    valid = 0;", "size": 10, "font": "Consolas"},
            {"text": "    printf(\"\\nPilih nomor film (1-5): \");", "size": 10, "font": "Consolas"},
            {"text": "    scanf(\"%d\", &pilih);", "size": 10, "font": "Consolas"},
            {"text": "    switch (pilih) {", "size": 10, "font": "Consolas"},
            {"text": "        case 1: if (STOK1) { strcpy(judul, JUDUL1);", "size": 10, "font": "Consolas"},
            {"text": "                harga = HARGA1; valid = 1; }", "size": 10, "font": "Consolas"},
            {"text": "                else printf(\"Film sedang dipinjam!\\n\"); break;", "size": 10, "font": "Consolas"},
            {"text": "        /* ... case 2 s/d 5 ... */", "size": 10, "font": "Consolas"},
            {"text": "    }", "size": 10, "font": "Consolas"},
            {"text": "} while (!valid);", "size": 10, "font": "Consolas", "space_after": 6},
            {"text": "/* Perhitungan biaya & denda (if-else) */", "size": 10, "font": "Consolas", "color": "059669"},
            {"text": "biaya = harga * lama;", "size": 10, "font": "Consolas"},
            {"text": "if (hariKembali > lama) {", "size": 10, "font": "Consolas"},
            {"text": "    denda = (hariKembali - lama) * DENDA_PER_HARI;", "size": 10, "font": "Consolas"},
            {"text": "    strcpy(status, \"Terlambat\");", "size": 10, "font": "Consolas"},
            {"text": "} else { denda = 0; strcpy(status, \"Tepat waktu\"); }", "size": 10, "font": "Consolas"},
        ],
        accent_hex="0F172A", bg_hex="F1F5F9"
    )

    s8.add_card(
        emu_in(6.85), emu_in(1.42), emu_in(5.8), emu_in(5.45),
        "3.4 Penjelasan Komponen Kode Program",
        [
            "if : Mengecek apakah pelanggan ingin memperpanjang lama peminjaman (jawab == 'y' || jawab == 'Y').",
            "if-else : Mengecek ketersediaan stok film (STOK1..5) serta menentukan apakah pengembalian Terlambat (hariKembali > lama) atau Tepat waktu.",
            "switch-case : Memilih data film ke-1 sampai ke-5 berdasarkan nomor yang diinput pelanggan.",
            "do-while : Mengulang input pemilihan film selama pilihan tidak valid atau film sedang dipinjam (!valid).",
            "Variabel & Operator : Menggunakan tipe int dan char[]; operator aritmatika (*, +, -, +=), relasional (>), logika (||, !), dan ternary (?:).",
            "Input / Output : Menggunakan printf(), scanf(), dan strcpy()."
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
            "Tugas:",
            "• Input ID dan nama pelanggan",
            "• Menampilkan daftar 5 pilihan film",
            "• Input & validasi pilihan film",
            "• Menggunakan perulangan do-while",
            "Bagian Kode:",
            "• Konstanta #define JUDUL1..5, HARGA1..5, STOK1..5",
            "• Input id & nama pelanggan",
            "• Tabel daftar film & blok do-while + switch(pilih)",
            "Integrasi: Menyediakan variabel judul & harga film terpilih untuk Mahasiswa 2."
        ],
        accent_hex="0284C7", font_size=11
    )

    s9.add_card(
        emu_in(4.68), emu_in(1.45), emu_in(3.85), emu_in(5.4),
        "4.2 Mahasiswa 2 — Sewa & Denda",
        [
            "Nama / NRP : ................................",
            "Tugas:",
            "• Menentukan biaya sewa",
            "• Menghitung lama peminjaman & perpanjangan",
            "• Menghitung denda keterlambatan",
            "• Menentukan status pengembalian",
            "Bagian Kode:",
            "• Input lama & perpanjangan (if jawab == 'y')",
            "• Input hariKembali & hitung biaya = harga * lama",
            "• Blok if-else (hariKembali > lama) untuk denda & status",
            "Integrasi: Menghasilkan nilai biaya, denda, & status untuk Mahasiswa 3."
        ],
        accent_hex="7C3AED", font_size=11
    )

    s9.add_card(
        emu_in(8.80), emu_in(1.45), emu_in(3.85), emu_in(5.4),
        "4.3 Mahasiswa 3 — Transaksi & Uji",
        [
            "Nama / NRP : ................................",
            "Tugas:",
            "• Menampilkan bukti rental",
            "• Menampilkan biaya, denda, & total bayar",
            "• Menampilkan status film / pengembalian",
            "• Menguji tepat waktu & terlambat",
            "Bagian Kode:",
            "• Blok pencetakan BUKTI RENTAL lengkap",
            "• Integrasi variabel dari Mahasiswa 1 & 2 di main()",
            "• Pengujian 5 skenario input & batas",
            "Integrasi: Menyatukan seluruh bagian kode menjadi satu program utuh."
        ],
        accent_hex="059669", font_size=11
    )
    slides.append(s9)

    # =========================================================================
    # SLIDE 10: BAB V — PENGUJIAN PROGRAM (5.1 SKENARIO PENGUJIAN)
    # =========================================================================
    s10 = SlideBuilder()
    s10.add_header("BAB V", "PENGUJIAN PROGRAM: 5 SKENARIO PENGUJIAN", "5.1 Tabel Skenario Pengujian Program Rental Film", 10)

    scenarios = [
        ("1. Peminjaman Tepat Waktu",
         "Pilih Film = 1 (Avengers Rp5000), Lama = 3 hari, Perpanjang = n, Kembali = hari ke-3",
         "Diharapkan: Biaya Rp15000, Denda Rp0, Total Rp15000, Status: Tepat waktu",
         "Aktual: Biaya Rp15000, Denda Rp0, Total Rp15000, Status: Tepat waktu  [BERHASIL]",
         "059669"),
        ("2. Pilihan Nomor Tidak Valid",
         "Pilih Nomor Film = 9 (di luar rentang 1-5)",
         "Diharapkan: Muncul pesan 'Nomor tidak valid, ulangi!' dan meminta input ulang",
         "Aktual: Muncul 'Nomor tidak valid, ulangi!' dan do-while mengulang input  [BERHASIL]",
         "0284C7"),
        ("3. Pilih Film Sedang Dipinjam",
         "Pilih Nomor Film = 3 (Interstellar, STOK3 = 0 / Dipinjam)",
         "Diharapkan: Ditolak dengan pesan 'Film sedang dipinjam, pilih yang lain!'",
         "Aktual: Pesan tampil dan pengguna diminta memilih film lain  [BERHASIL]",
         "D97706"),
        ("4. Perpanjangan Masa Sewa",
         "Pilih Film = 2 (Rp6000), Lama awal = 2 hari, Perpanjang = y (+2 hari), Kembali = hari ke-4",
         "Diharapkan: Lama pinjam jadi 4 hari, Biaya Rp24000, Denda Rp0, Status: Tepat waktu",
         "Aktual: Lama pinjam 4 hari, Biaya Rp24000, Denda Rp0, Tepat waktu  [BERHASIL]",
         "7C3AED"),
        ("5. Pengembalian Terlambat",
         "Pilih Film = 5 (Inception Rp6500), Lama = 2 hari, Perpanjang = n, Kembali = hari ke-5",
         "Diharapkan: Terlambat 3 hari -> Denda Rp6000, Biaya Rp13000, Total Rp19000, Terlambat",
         "Aktual: Biaya Rp13000, Denda Rp6000, Total Rp19000, Status: Terlambat  [BERHASIL]",
         "DC2626"),
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
    s11.add_header("BAB V", "BUKTI PENGUJIAN: OUTPUT TEPAT WAKTU & TERLAMBAT", "5.2 Hasil Running Program rental_film.c", 11)

    s11.add_card(
        emu_in(0.55), emu_in(1.42), emu_in(5.9), emu_in(5.45),
        "Pengujian 1 — Peminjaman Tepat Waktu",
        [
            {"text": "Masukkan ID pelanggan   : 101", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Masukkan nama pelanggan : Budi Santoso", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Pilih nomor film (1-5)  : 1", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Anda memilih: Avengers: Endgame (Rp5000/hari)", "size": 10, "font": "Consolas", "color": "38BDF8"},
            {"text": "Lama peminjaman (hari)  : 3", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Perpanjang peminjaman? (y/n): n", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Film dikembalikan pada hari ke-: 3", "size": 10, "font": "Consolas", "color": "CBD5E1", "space_after": 6},
            {"text": "========== BUKTI RENTAL ==========", "size": 10, "bold": True, "font": "Consolas", "color": "4ADE80"},
            {"text": "ID / Nama    : 101 / Budi Santoso", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Film         : Avengers: Endgame", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Biaya/hari   : Rp5000", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Lama pinjam  : 3 hari", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Dikembalikan : hari ke-3", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Biaya sewa   : Rp15000", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Denda        : Rp0", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Total bayar  : Rp15000", "size": 10, "bold": True, "font": "Consolas", "color": "4ADE80"},
            {"text": "Status       : Tepat waktu", "size": 10, "bold": True, "font": "Consolas", "color": "4ADE80"},
            {"text": "==================================", "size": 10, "font": "Consolas", "color": "4ADE80"},
        ],
        accent_hex="059669", bg_hex="0F172A"
    )

    s11.add_card(
        emu_in(6.75), emu_in(1.42), emu_in(5.9), emu_in(5.45),
        "Pengujian 2 — Validasi Stok & Pengembalian Terlambat",
        [
            {"text": "Masukkan ID pelanggan   : 102", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Masukkan nama pelanggan : Siti Aminah", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Pilih nomor film (1-5)  : 3", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Film sedang dipinjam, pilih yang lain!", "size": 10, "font": "Consolas", "color": "F87171"},
            {"text": "Pilih nomor film (1-5)  : 5", "size": 10, "font": "Consolas", "color": "CBD5E1"},
            {"text": "Lama peminjaman: 2 | Perpanjang: n | Kembali: hari ke-5", "size": 10, "font": "Consolas", "color": "CBD5E1", "space_after": 6},
            {"text": "========== BUKTI RENTAL ==========", "size": 10, "bold": True, "font": "Consolas", "color": "F87171"},
            {"text": "ID / Nama    : 102 / Siti Aminah", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Film         : Inception", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Biaya/hari   : Rp6500", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Lama pinjam  : 2 hari", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Dikembalikan : hari ke-5", "size": 10, "font": "Consolas", "color": "FCA5A5"},
            {"text": "Biaya sewa   : Rp13000", "size": 10, "font": "Consolas", "color": "FFFFFF"},
            {"text": "Denda        : Rp6000", "size": 10, "font": "Consolas", "color": "FCA5A5"},
            {"text": "Total bayar  : Rp19000", "size": 10, "bold": True, "font": "Consolas", "color": "FBBF24"},
            {"text": "Status       : Terlambat", "size": 10, "bold": True, "font": "Consolas", "color": "F87171"},
            {"text": "==================================", "size": 10, "font": "Consolas", "color": "F87171"},
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
            "Hasil Program: Program berhasil memvalidasi pilihan film, menghitung perpanjangan sewa, menghitung denda keterlambatan, dan menampilkan bukti rental.",
            "if : Mengecek apakah pengguna memilih perpanjangan sewa (jawab == 'y' || jawab == 'Y').",
            "if-else : Mengecek stok film (STOK1..5) serta menentukan denda dan status ('Terlambat' vs 'Tepat waktu').",
            "switch-case : Memilih film ke-1 s/d ke-5 berdasarkan input pengguna.",
            "do-while : Mengulang input pilihan film selama nomor tidak valid atau film sedang dipinjam (!valid)."
        ],
        accent_hex="0284C7", font_size=12
    )

    s12.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(5.4),
        "6.3 Kendala dan Solusi Selama Pengerjaan",
        [
            "Kendala 1: Pengguna memilih nomor film di luar 1-5 atau film yang sedang dipinjam (STOK = 0).",
            "Solusi 1 : Menggunakan perulangan do-while dengan variabel penanda valid dan percabangan switch-case.",
            "Kendala 2: Menyimpan data 5 film tanpa menggunakan array maupun struct.",
            "Solusi 2 : Mendefinisikan konstanta makro #define JUDUL1..5, HARGA1..5, dan STOK1..5 di bagian atas program.",
            "Kendala 3: Membaca nama pelanggan yang mengandung spasi menggunakan scanf.",
            "Solusi 3 : Menggunakan format spesifikasi scanf(\" %[^\\n]\", nama) agar spasi ikut terbaca."
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
            "Seluruh tujuan mini project telah tercapai.",
            "Program Sistem Rental Film berhasil dibangun menggunakan bahasa C dengan menerapkan do-while, switch-case, if, dan if-else tanpa menggunakan array data, struct, maupun pointer.",
            "Program berhasil memvalidasi pilihan film, menghitung biaya sewa dan denda keterlambatan, serta menampilkan bukti rental dengan tepat."
        ],
        accent_hex="059669", font_size=12
    )

    s13.add_card(
        emu_in(6.75), emu_in(1.45), emu_in(5.9), emu_in(3.3),
        "7.2 Saran Pengembangan (Tahap Berikutnya)",
        [
            "Pada tahap selanjutnya, program dapat dikembangkan untuk menyimpan banyak data film dan pelanggan menggunakan ARRAY.",
            "Data pelanggan, film, dan transaksi dapat dikelompokkan menggunakan STRUCT.",
            "Manipulasi dan pengelolaan data selanjutnya dapat dioptimalkan menggunakan POINTER."
        ],
        accent_hex="0284C7", font_size=12
    )

    s13.add_card(
        emu_in(0.55), emu_in(4.95), emu_in(12.1), emu_in(1.9),
        "Daftar Pustaka",
        [
            "1. Kernighan, B. W., & Ritchie, D. M. (1988). The C Programming Language (2nd ed.). Prentice Hall.",
            "2. Modul Praktikum & Materi Kuliah Pemrograman Dasar Tahun 2026.",
            "3. Dokumentasi C Standard Library (<stdio.h> & <string.h>) — https://en.cppreference.com/w/c"
        ],
        accent_hex="0F172A", font_size=12
    )
    slides.append(s13)

    return slides


def create_pptx(filename, slides):
    num_slides = len(slides)

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

    root_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

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

    print(f"Berhasil memperbarui {filename} ({num_slides} slide)!")


if __name__ == "__main__":
    all_slides = build_slides()
    create_pptx(OUTPUT_FILE, all_slides)
