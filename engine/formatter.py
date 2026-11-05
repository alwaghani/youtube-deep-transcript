"""
Document formatter for deep transcripts.
"""

def format_transcript_document(metadata, summary_markdown="", glossary_markdown="", dialogue_markdown=""):
    """
    Assembles a professional Markdown document from metadata, executive summary,
    glossary, and speaker dialogue.
    """
    title = metadata.get("title", "Transkrip Video")
    channel = metadata.get("channel", "YouTube")
    duration = metadata.get("duration_string", "")
    url = metadata.get("url", "")

    doc = [
        f"# Transkrip Dialog: {title}\n",
        f"- **Channel (Saluran)**: {channel}",
        f"- **Durasi**: {duration}",
        f"- **URL Video**: {url}",
        "\n---",
    ]

    if summary_markdown.strip():
        doc.append("\n## 🧭 Panduan Membaca & Intisari Pembahasan (Executive Summary)\n")
        doc.append(summary_markdown.strip())
        doc.append("\n---")

    if glossary_markdown.strip():
        doc.append("\n## 📚 Kamus Istilah & Konsep Penting (Glossary)\n")
        doc.append(glossary_markdown.strip())
        doc.append("\n---")

    doc.append("\n## 💬 Dialog Lengkap\n")
    doc.append(dialogue_markdown.strip())
    doc.append("\n")

    return "\n".join(doc)
