#!/usr/bin/env python3
"""
Skill helper script to fetch, clean, and chunk YouTube subtitles.
"""

import sys
import os

# Add repo root to sys.path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from engine.extractor import extract_subtitles

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_youtube_subs.py <YOUTUBE_URL> [output_json_path] [sub_langs]")
        sys.exit(1)

    url = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    langs = sys.argv[3] if len(sys.argv) > 3 else "id-orig,id,en"

    res = extract_subtitles(url, sub_langs=langs, output_json=out_path)
    if res:
        print(f"Extracted {res['total_chunks']} chunks from '{res['metadata']['title']}' ({res['metadata']['duration_string']})")
    else:
        sys.exit(1)
