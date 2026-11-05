---
name: youtube-deep-transcript
description: Ekstrak transkrip video YouTube ke dalam format dialog lengkap yang dilengkapi ringkasan eksekutif berbabak (timeline summary) dan kamus istilah awam (glossary with simple analogies). Wajib digunakan saat pengguna meminta transkripsi, rangkuman mendalam, atau bedah video YouTube/podcast agar mudah dipahami orang awam.
---

# YouTube Deep Transcript & Layman Explainer

Skill ini mengubah video YouTube (terutama podcast, wawancara mendalam, kuliah, atau diskusi berbobot) menjadi satu file dokumen Markdown lengkap. Hasilnya dirancang agar **siapa pun (bahkan orang awam)** bisa memahami isi obrolan berlevel tinggi seolah-olah mereka ikut menonton langsung.

---

## Struktur File Output yang Dihasilkan

Dokumen Markdown akhir WAJIB memuat 4 bagian utama berikut secara berurutan:

```markdown
# Transkrip Dialog: [Judul Video]

- **Channel (Saluran)**: [Nama Saluran]
- **Host (Pemandu Acara)**: [Nama Host jika ada]
- **Guest (Bintang Tamu)**: [Nama Tamu jika ada]
- **Durasi**: [HH:MM:SS / Durasi Video]
- **URL Video**: [Tautan YouTube]

---

## 🧭 Panduan Membaca & Intisari Pembahasan (Executive Summary)
[Rangkuman pokok bahasan yang dibagi per babak / topik utama secara terstruktur dengan penanda waktu]

---

## 📚 Kamus Istilah & Konsep Penting (Glossary for Beginners)
[Penjelasan semua istilah teknis, singkatan, konsep ekonomi/sains/sejarah, dan istilah asing menggunakan bahasa sederhana dan analogi sehari-hari]

---

## 💬 Dialog Lengkap
**[timestamp] Pembicara A:** [Kalimat...]
**[timestamp] Pembicara B:** [Kalimat...]
```

---

## Alur Kerja Langkah Demi Langkah

### Langkah 1: Ekstraksi Subtitle & Metadata Otomatis
Gunakan script pembantu yang sudah tersedia di direktori skill ini:
```bash
python3 .claude/skills/youtube-deep-transcript/scripts/extract_youtube_subs.py "<YOUTUBE_URL>" "/tmp/subs_extracted.json"
```

Script ini otomatis:
1. Menjalankan `yt-dlp` dengan runtime Node.js untuk membongkar proteksi YouTube.
2. Mengambil judul, nama channel, deskripsi, dan takarir (*captions*).
3. Membersihkan tag HTML dan menduplikasi teks berulang khas auto-generated caption YouTube.
4. Menghasilkan potongan teks per 30–60 detik dalam file JSON `/tmp/subs_extracted.json`.

---

### Langkah 2: Pemisahan Pembicara (Speaker Diarization)
Bila video berupa wawancara atau dialog multi-orang:
1. Identifikasi nama pembicara dari deskripsi video, judul, atau menit-menit pembuka (siapa host dan siapa bintang tamunya).
2. **Jika durasi video panjang (>25 menit atau >50 chunk):**
   - Bagi teks menjadi beberapa potongan (*slices*, misalnya per 20–30 menit).
   - Kerahkan agen AI paralel (`Agent` tool) untuk memproses masing-masing potongan secara serentak.
   - Instruksikan agen agar:
     - Memberi label penutur yang jelas: `**[timestamp] Nama:**`.
     - **TIDAK memotong atau meringkas kata** (*verbatim / kata demi kata dipertahankan 100%*).
3. Gabungkan hasil dialog dari seluruh potongan.

---

### Langkah 3: Susun Panduan Membaca (Executive Summary)
Bagi obrolan menjadi babak-babak kronologis (misal 5–8 babak waktu):
- Tuliskan rentang waktu menitnya (`Menit XX:XX – YY:YY`).
- Berikan poin-poin inti apa yang diperdebatkan atau disimpulkan.
- Tuliskan pesan moral atau sudut pandang utama dari pembicara.

---

### Langkah 4: Susun Kamus Istilah Awam (Layman Glossary)
Identifikasi seluruh kata sulit, singkatan, istilah bahasa Inggris, atau referensi sejarah/geopolitik yang muncul dalam dialog (contoh: *GDP, HFT, Moat, Sparta, ICBM, CRISPR, Debasement, Attention Span*).

Untuk setiap istilah:
1. **Definisi Sederhana:** Jelaskan maknanya tanpa jargon berbelit.
2. **💡 Analogi Sehari-hari:** Berikan perumpamaan konkret dari kehidupan sehari-hari yang mudah dibayangkan siapa saja (misal: "HFT itu seperti balapan lari antara manusia biasa melawan mobil F1").

---

### Langkah 5: Gabungkan & Simpan
1. Satukan Metadata, Panduan Membaca, Kamus Istilah, dan Dialog Lengkap.
2. Simpan ke file `.md` dengan nama yang deskriptif (misal: `transkrip-[topik/nama-tamu].md`).
3. Bersihkan file sementara di `/tmp/`.
4. Laporkan kepada pengguna bahwa file siap dibaca.
