#!/usr/bin/env python3
"""
CLI Runner for YouTube Deep Transcript Engine.
"""

import sys
import os
import argparse
import json
import re

from engine.extractor import extract_subtitles
from engine.formatter import format_transcript_document

def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|]', "", name)
    clean = clean.replace(" ", "-").lower()
    return clean[:60]

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Deep Transcript & Subtitle Extraction Tool"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--lang",
        default="id-orig,id,en",
        help="Preferred subtitle language codes comma-separated (default: id-orig,id,en)"
    )
    parser.add_argument(
        "--out",
        help="Output markdown file path (defaults to outputs/<title>.md)"
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Export raw chunks directly to JSON instead of markdown"
    )

    args = parser.parse_args()

    os.makedirs("outputs", exist_ok=True)

    print(f"[*] Mengekstrak data dan takarir dari: {args.url} ...")
    data = extract_subtitles(args.url, sub_langs=args.lang)

    if not data:
        print("[!] Gagal mengekstrak takarir. Pastikan video memiliki subtitle atau CC otomatis.", file=sys.stderr)
        sys.exit(1)

    title = data["metadata"]["title"]
    duration = data["metadata"]["duration_string"]
    chunks = data["chunks"]
    print(f"[+] Berhasil! Judul: '{title}' ({duration}) | Total: {len(chunks)} segmen.")

    default_slug = sanitize_filename(title)

    if args.json_only:
        out_file = args.out or os.path.join("outputs", f"{default_slug}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[✓] Data JSON tersimpan di: {out_file}")
        return

    # Build initial clean markdown
    dialogue_lines = []
    for c in chunks:
        dialogue_lines.append(f"**[{c['timestamp']}]** {c['text']}\n")

    doc = format_transcript_document(
        metadata=data["metadata"],
        dialogue_markdown="\n".join(dialogue_lines)
    )

    out_file = args.out or os.path.join("outputs", f"{default_slug}.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(doc)

    print(f"[✓] Dokumen transkrip tersimpan di: {out_file}")
    print(f"[i] Untuk pemisahan nama penutur (speaker diarization) dan penjelasan awam, jalankan via Claude Code skill.")

if __name__ == "__main__":
    main()
