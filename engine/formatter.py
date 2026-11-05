"""
Document formatter for deep transcripts.
Includes clickable thumbnail banner, rich metadata, chapter listings,
executive summary, glossary, and full dialogue.
"""

def format_upload_date(raw_date):
    """
    Formats YYYYMMDD into a localized readable date string (e.g., '4 November 2026').
    """
    if not raw_date or len(raw_date) != 8:
        return raw_date or ""
    months = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    try:
        year = raw_date[:4]
        month_idx = int(raw_date[4:6]) - 1
        day = str(int(raw_date[6:8]))
        if 0 <= month_idx < 12:
            return f"{day} {months[month_idx]} {year}"
        return f"{year}-{raw_date[4:6]}-{raw_date[6:8]}"
    except (ValueError, IndexError):
        return raw_date

def format_view_count(views):
    """
    Formats view count integer with dot thousands separator (e.g., '174.901 tayangan').
    """
    if not views:
        return ""
    try:
        return f"{int(views):,}".replace(",", ".") + " tayangan"
    except (ValueError, TypeError):
        return f"{views} tayangan"

def format_transcript_document(metadata, summary_markdown="", glossary_markdown="", dialogue_markdown=""):
    """
    Assembles a professional Markdown document from metadata, clickable thumbnail banner,
    official chapters, executive summary, glossary, and speaker dialogue.
    """
    title = metadata.get("title", "Transkrip Video")
    channel = metadata.get("channel", "YouTube")
    channel_url = metadata.get("channel_url", "")
    duration = metadata.get("duration_string", "")
    url = metadata.get("url", "")
    thumbnail = metadata.get("thumbnail", "")
    upload_date = format_upload_date(metadata.get("upload_date", ""))
    view_count = format_view_count(metadata.get("view_count"))
    chapters = metadata.get("chapters", [])

    doc = [
        f"# Transkrip Dialog: {title}\n"
    ]

    # Clickable thumbnail banner
    if thumbnail:
        doc.append(f"[![Thumbnail Banner]({thumbnail})]({url})\n")

    # Metadata list
    channel_display = f"[{channel}]({channel_url})" if channel_url else channel
    doc.append(f"- **Channel (Saluran)**: {channel_display}")
    if upload_date:
        doc.append(f"- **Tanggal Tayang**: {upload_date}")
    if duration:
        doc.append(f"- **Durasi**: {duration}")
    if view_count:
        doc.append(f"- **Total Penayangan**: {view_count}")
    doc.append(f"- **URL Video**: {url}")
    doc.append("\n---")

    # 1. Chapters Section (if available)
    if chapters:
        doc.append("\n## 📑 Daftar Bab Video (Chapters)\n")
        for ch in chapters:
            ts = ch.get("timestamp", "00:00")
            ch_title = ch.get("title", "")
            doc.append(f"- **[{ts}]** {ch_title}")
        doc.append("\n---")

    # 2. Executive Summary
    if summary_markdown.strip():
        doc.append("\n## 🧭 Panduan Membaca & Intisari Pembahasan (Executive Summary)\n")
        doc.append(summary_markdown.strip())
        doc.append("\n---")

    # 3. Layman Glossary
    if glossary_markdown.strip():
        doc.append("\n## 📚 Kamus Istilah & Konsep Penting (Glossary)\n")
        doc.append(glossary_markdown.strip())
        doc.append("\n---")

    # 4. Full Dialogue
    doc.append("\n## 💬 Dialog Lengkap\n")
    doc.append(dialogue_markdown.strip())
    doc.append("\n")

    return "\n".join(doc)
