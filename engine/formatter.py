"""
Document formatter for deep transcripts.
Includes chapter listings, executive summary, glossary, and full dialogue.
"""

def format_transcript_document(metadata, summary_markdown="", glossary_markdown="", dialogue_markdown=""):
    """
    Assembles a professional Markdown document from metadata, official chapters,
    executive summary, glossary, and speaker dialogue.
    """
    title = metadata.get("title", "Transkrip Video")
    channel = metadata.get("channel", "YouTube")
    duration = metadata.get("duration_string", "")
    url = metadata.get("url", "")
    chapters = metadata.get("chapters", [])

    doc = [
        f"# Transkrip Dialog: {title}\n",
        f"- **Channel (Saluran)**: {channel}",
        f"- **Durasi**: {duration}",
        f"- **URL Video**: {url}",
        "\n---",
    ]

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
