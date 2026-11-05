"""
Subtitle & Metadata Extractor using yt-dlp and Node.js runtime.
"""

import os
import sys
import json
import subprocess
import re
import glob

def run_cmd(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return p.returncode, p.stdout, p.stderr

def to_seconds(ts_str):
    parts = ts_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return 0.0

def fmt_ts(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"

def extract_subtitles(url, sub_langs="id-orig,id,en", output_json=None):
    """
    Downloads captions and metadata from YouTube via yt-dlp without downloading video,
    deduplicates rolling caption tags, and chunks conversation into natural dialogue blocks.
    """
    # 1. Fetch metadata
    meta_cmd = ["yt-dlp", "--js-runtimes", "node", "-j", url]
    code, stdout, stderr = run_cmd(meta_cmd)
    if code != 0 or not stdout.strip():
        print(f"Error fetching metadata: {stderr}", file=sys.stderr)
        return None

    meta = json.loads(stdout.strip())
    title = meta.get("title", "")
    channel = meta.get("channel", "")
    duration = meta.get("duration", 0)
    duration_str = meta.get("duration_string", "")
    description = meta.get("description", "")

    # 2. Download subtitles
    temp_prefix = f"/tmp/yt_sub_{os.getpid()}"
    dl_cmd = [
        "yt-dlp", "--js-runtimes", "node", "--skip-download",
        "--write-auto-subs", "--write-subs",
        "--sub-lang", sub_langs,
        "--sub-format", "vtt",
        "-o", f"{temp_prefix}.%(ext)s",
        url
    ]
    run_cmd(dl_cmd)

    # Find generated vtt files
    vtt_files = glob.glob(f"{temp_prefix}*.vtt")
    if not vtt_files:
        print("No subtitle files found for the requested languages.", file=sys.stderr)
        return None

    # Prioritize languages based on requested order
    chosen_file = None
    for lang in sub_langs.split(','):
        lang = lang.strip()
        for vf in vtt_files:
            if f".{lang}." in vf or vf.endswith(f".{lang}.vtt"):
                chosen_file = vf
                break
        if chosen_file:
            break
    if not chosen_file:
        chosen_file = vtt_files[0]

    with open(chosen_file, 'r', encoding='utf-8') as f:
        vtt_content = f.read()

    # Clean up temporary vtt files
    for vf in vtt_files:
        try:
            os.remove(vf)
        except OSError:
            pass

    # 3. Parse VTT and deduplicate rolling captions
    cues = re.findall(
        r'(\d{2}:\d{2}(?::\d{2})?\.\d{3}) --> (\d{2}:\d{2}(?::\d{2})?\.\d{3})[^\n]*\n([\s\S]*?)(?=\n\d{2}:\d{2}(?::\d{2})?\.\d{3} -->|\Z)',
        vtt_content
    )

    cleaned = []
    last_text = None
    for start_ts, end_ts, text in cues:
        clean_text = re.sub(r'<[^>]+>', '', text)
        lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
        if not lines:
            continue
        newest = lines[-1]
        if newest and newest != last_text:
            last_text = newest
            start_sec = to_seconds(start_ts)
            cleaned.append((start_sec, newest))

    # 4. Chunk into natural conversation blocks (~30-45s or 40-50 words)
    chunks = []
    curr_ts = None
    curr_words = []

    for sec, text in cleaned:
        if curr_ts is None:
            curr_ts = sec

        if (sec - curr_ts >= 30 and len(curr_words) >= 40) or (sec - curr_ts >= 60):
            chunks.append({
                "timestamp": fmt_ts(curr_ts),
                "seconds": curr_ts,
                "text": " ".join(curr_words)
            })
            curr_ts = sec
            curr_words = [text]
        else:
            curr_words.append(text)

    if curr_words:
        chunks.append({
            "timestamp": fmt_ts(curr_ts),
            "seconds": curr_ts,
            "text": " ".join(curr_words)
        })

    result = {
        "metadata": {
            "title": title,
            "channel": channel,
            "duration_seconds": duration,
            "duration_string": duration_str,
            "url": url,
            "description": description[:1000]
        },
        "total_chunks": len(chunks),
        "chunks": chunks
    }

    if output_json:
        with open(output_json, 'w', encoding='utf-8') as out:
            json.dump(result, out, ensure_ascii=False, indent=2)

    return result
