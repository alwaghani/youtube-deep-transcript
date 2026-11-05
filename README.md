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

## 🚀 Cara Penggunaan (AI-Powered)

Cukup buka repositori ini dengan **Claude Code**, lalu berikan tautan (*link*) video YouTube yang ingin dibedah:

```text
Bro, tolong bedah dan transkrip video ini: https://youtu.be/LINK_VIDEO
```

### Apa yang Otomatis Dikerjakan AI?
1. ⚡ **Mengekstrak Takarir:** Menyedot takarir resmi atau otomatis tanpa perlu mengunduh file video.
2. 👥 **Pemisahan Pembicara (*Speaker Diarization*):** Mengenali dan membedakan giliran bicara antar-tokoh secara utuh (*verbatim*).
3. 🧭 **Ringkasan Eksekutif (*Timeline Breakdown*):** Memetakan topik obrolan per babak waktu agar alur video 1–2 jam bisa dipahami dalam hitungan menit.
4. 📚 **Kamus Istilah Awam (*Layman Glossary*):** Menerjemahkan istilah teknis, singkatan asing, dan teori rumit ke analogi sehari-hari yang mudah dicerna.

File hasil akhir akan otomatis tersimpan rapi di dalam folder `outputs/` dalam format Markdown.
