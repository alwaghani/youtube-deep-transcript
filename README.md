# 🎙️ YouTube Deep Transcript & Layman Explainer

Repositori (*repository*) ini adalah mesin otomatis untuk mengekstrak, membersihkan, dan menganalisis video YouTube (terutama podcast, wawancara mendalam, dan materi berbobot tinggi) menjadi dokumen transkrip terstruktur yang ramah orang awam.

---

## 🌟 Keunggulan Utama
1. **Ekstraksi Cepat & Ringan:** Mengambil takarir (*captions/subtitles*) dalam hitungan detik tanpa perlu mengunduh file video utuh.
2. **Pembersihan Teks Otomatis:** Membuang tag HTML dan menduplikasi teks berulang khas takarir bergulir (*rolling captions*) YouTube.
3. **Pemisahan Pembicara (*Speaker Diarization*):** Mengelompokkan setiap kalimat ke nama narasumber aslinya secara utuh (*verbatim*).
4. **Ringkasan Eksekutif (*Timeline Summary*):** Menyajikan peta pembahasan berbabak waktu sehingga alur percakapan 1–2 jam bisa dipahami dalam beberapa menit.
5. **Kamus Istilah Awam (*Layman Glossary*):** Menerjemahkan istilah teknis, singkatan asing, dan teori rumit ke analogi sehari-hari yang mudah dicerna.

---

## 📁 Struktur Repositori

```text
transcript/
├── engine/                      # Modul inti mesin pemroses
│   ├── __init__.py
│   ├── extractor.py             # Ekstraksi takarir via yt-dlp & pembersih VTT
│   └── formatter.py             # Penyusun format dokumen Markdown
├── outputs/                     # Arsip hasil transkrip (.md & .json)
│   └── transkrip-timothy-ronald-inner-circle.md
├── .claude/
│   └── skills/
│       └── youtube-deep-transcript/  # Skill Claude Code terintegrasi
├── run.py                       # CLI Runner utama
├── requirements.txt             # Dependensi Python
├── .gitignore                   # Aturan pengabaian file Git
└── README.md                    # Dokumentasi repositori
```

---

## ⚙️ Persyaratan Sistem (*Prerequisites*)

- **Python**: 3.10+
- **Node.js**: v22+ (untuk *JavaScript runtime* pemecah proteksi YouTube)
- **yt-dlp**: Versi terbaru (`2026.10.26`+)
- **ffmpeg**: Tersedia di sistem untuk manipulasi media

---

## 🚀 Cara Penggunaan

### 1. Menggunakan CLI Langsung (*Command Line Interface*)
Ekstrak takarir video YouTube langsung ke format Markdown:
```bash
python3 run.py "https://youtu.be/nz665d6jcAQ"
```

Ekstrak langsung ke format data mentah JSON:
```bash
python3 run.py "https://youtu.be/nz665d6jcAQ" --json-only
```

Menentukan bahasa takarir (*subtitles*) pilihan:
```bash
python3 run.py "https://youtu.be/nz665d6jcAQ" --lang "id,en" --out "outputs/podcast-baru.md"
```

---

### 2. Menggunakan Asisten Claude Code (Direkomendasikan)
Kamu cukup memberikan tautan video YouTube di dalam Claude Code:
> *"Bro, tolong bedah dan transkrip video ini: [LINK_YOUTUBE]"*

Claude Code akan otomatis memanggil skill `youtube-deep-transcript`, menjalankan pemisahan pembicara (*speaker diarization*), serta menyusun ringkasan eksekutif dan kamus istilah awam secara otomatis.
