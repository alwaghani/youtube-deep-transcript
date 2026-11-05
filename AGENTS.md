# AGENTS.md

Panduan ini ditujukan untuk **semua AI Coding Assistant & Agent** (Claude Code, Cursor, Windsurf, Codex, Roo Code, Aider, Copilot, dsb.) saat bekerja di repositori ini.

---

## 📌 Ringkasan Repositori (*Repository Overview*)

Repositori ini adalah mesin ekstraksi dan analisis mendalam transkrip video YouTube (podcast, wawancara, debat, materi edukasi). 
Tujuan utamanya adalah mengubah video YouTube berbobot tinggi menjadi dokumen transkrip terstruktur yang **ramah orang awam** dengan memadukan:
1. **Ekstraksi Takarir (*Captions Extraction*):** Cepat dan ringan via `yt-dlp` tanpa perlu unduh file video.
2. **Pemisahan Pembicara (*Speaker Diarization*):** Mengenali siapa yang berbicara secara utuh (*verbatim*).
3. **Ringkasan Kronologis (*Timeline Executive Summary*):** Pemetaan topik per babak waktu.
4. **Kamus Istilah Awam (*Layman Glossary*):** Penjelasan istilah sulit/jargon dengan analogi sehari-hari.

---

## 🛠️ Perintah CLI Inti (*Core CLI Commands*)

Jalankan perintah ini di terminal untuk mengekstrak takarir secara otomatis:

```bash
# 1. Ekstraksi standar langsung ke format Markdown
python3 run.py "<YOUTUBE_URL>"

# 2. Ekstraksi ke format mentah JSON (disarankan untuk AI Agent memproses chunk data)
python3 run.py "<YOUTUBE_URL>" --json-only

# 3. Menentukan preferensi bahasa takarir (default: id-orig,id,en)
python3 run.py "<YOUTUBE_URL>" --lang "id,en" --out "outputs/custom.md"
```

---

## 🤖 Alur Kerja AI Agent (*Step-by-Step Workflow*)

Saat pengguna meminta kamu untuk membedah, menganalisis, atau mentranskrip video YouTube:

### Langkah 1: Ekstraksi Data Mentah
Jalankan perintah CLI untuk mendapatkan potongan dialog mentah:
```bash
python3 run.py "<YOUTUBE_URL>" --json-only
```
File JSON akan tersimpan di folder `outputs/` yang memuat metadata video serta daftar segmen teks (*chunks*) berurutan waktu.

### Langkah 2: Pemisahan Pembicara (*Speaker Diarization*)
- Identifikasi pembicara dari judul, deskripsi video, atau menit pembuka (siapa pemandu acara / *host*, siapa bintang tamu / *guest*).
- Format dialog wajib: `**[timestamp] Nama Pembicara:** Kalimat...`
- **Aturan Ketat:** Jaga keaslian kalimat 100% (*verbatim*). Jangan meringkas, memotong, atau mengubah kata-kata yang diucapkan narasumber di bagian transkrip ini.

### Langkah 3: Susun Intisari Kronologis (*Executive Summary*)
Petakan alur pembicaraan menjadi babak-babak waktu kronologis (misal 5–8 segmen):
- Tuliskan rentang menitnya (`Menit XX:XX – YY:YY: [Topik Bahasan]`).
- Jelaskan poin perdebatan, argumen utama, dan kesimpulan penting.

### Langkah 4: Susun Kamus Istilah Awam (*Layman Glossary*)
Kumpulkan seluruh istilah teknis, singkatan asing, istilah ekonomi/teknologi/filsafat, atau referensi rumit yang disebut narasumber.
Untuk setiap istilah, sediakan:
1. **Definisi Singkat:** Penjelasan lugas tanpa jargon berbelit.
2. **💡 Analogi Sehari-hari:** Perumpamaan konkret dari kehidupan sehari-hari agar orang awam langsung paham.

### Langkah 5: Susun & Simpan Dokumen Akhir
Gabungkan dokumen dengan struktur berikut dan simpan ke dalam `outputs/transkrip-[nama-video].md`:

```markdown
# Transkrip Dialog: [Judul Video]

- **Channel (Saluran)**: [Nama Saluran]
- **Host (Pemandu Acara)**: [Nama Host]
- **Guest (Bintang Tamu)**: [Nama Bintang Tamu]
- **Durasi**: [HH:MM:SS]
- **URL Video**: [Tautan YouTube]

---

## 🧭 Panduan Membaca & Intisari Pembahasan (Executive Summary)
[Babak waktu dan poin penting...]

---

## 📚 Kamus Istilah & Konsep Penting (Glossary for Beginners)
- **Istilah A**: Definisi singkat.
  - *💡 Analogi:* Perumpamaan sederhana...

---

## 💬 Dialog Lengkap
**[00:00:15] Pembicara A:** ...
**[00:00:28] Pembicara B:** ...
```
