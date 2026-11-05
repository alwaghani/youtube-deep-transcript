"""
Subtitle & Metadata Extractor using yt-dlp and Node.js runtime.
Includes YouTube chapter parsing and smart subtitle fallback.
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

def parse_chapters_from_description(desc):
    """
    Extract chapters if creator listed timestamps in the description.
    Example: 01:25 - Topik Pembahasan
    """
    pattern = r'(?:^|\n)\s*(\d{1,2}:\d{2}(?::\d{2})?)\s+[-–:]?\s*([^\n\r]+)'
    matches = re.findall(pattern, desc)
    chapters = []
    for ts_str, title in matches:
        title_clean = title.strip()
        if len(title_clean) >= 2 and not title_clean.isdigit():
            sec = to_seconds(ts_str)
            chapters.append({
                "title": title_clean,
                "start_time": sec,
                "timestamp": fmt_ts(sec)
            })
    return chapters if len(chapters) >= 2 else []

def get_best_available_subtitle_langs(meta):
    """
    Finds the most reliable subtitle codes available for this video,
    prioritizing human-written manual subs and original audio captions (*-orig)
    to avoid YouTube machine-translation rate limits (HTTP 429).
    """
    candidates = []
    manual_subs = list(meta.get("subtitles", {}).keys())
    if manual_subs:
        for pref in ["id", "en"]:
            for m in manual_subs:
                if m.startswith(pref) and m not in candidates:
                    candidates.append(m)
        candidates.extend([m for m in manual_subs if m not in candidates])
        return candidates

    auto_subs = meta.get("automatic_captions", {})
    orig_langs = [k for k in auto_subs.keys() if "-orig" in k]
    if orig_langs:
        candidates.extend(orig_langs)

    audio_lang = meta.get("language")
    if audio_lang and audio_lang in auto_subs and audio_lang not in candidates:
        candidates.append(audio_lang)

    for common in ["id", "en"]:
        if common in auto_subs and common not in candidates:
            candidates.append(common)

    return candidates

def extract_subtitles(url, sub_langs="id-orig,id,en", output_json=None):
    """
    Downloads captions and metadata from YouTube via yt-dlp without downloading video,
    deduplicates rolling caption tags, parses chapters, and chunks conversation.
    Includes smart fallback to any available subtitle language if requested language is missing.
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

    # 1.1 Process chapters (native YouTube chapters or from description)
    raw_chapters = meta.get("chapters")
    chapters = []
    if raw_chapters:
        for ch in raw_chapters:
            start = ch.get("start_time", 0)
            chapters.append({
                "title": ch.get("title", "").strip(),
                "start_time": start,
                "end_time": ch.get("end_time"),
                "timestamp": fmt_ts(start)
            })
    else:
        chapters = parse_chapters_from_description(description)

    # 2. Download subtitles with smart fallback
    temp_prefix = f"/tmp/yt_sub_{os.getpid()}"

    def try_download_subs(lang_query):
        dl_cmd = [
            "yt-dlp", "--js-runtimes", "node", "--skip-download",
            "--write-auto-subs", "--write-subs",
            "--sub-lang", lang_query,
            "--sub-format", "vtt",
            "-o", f"{temp_prefix}.%(ext)s",
            url
        ]
        run_cmd(dl_cmd)
        return glob.glob(f"{temp_prefix}*.vtt")

    # Initial attempt with requested languages
    vtt_files = try_download_subs(sub_langs)

    # Smart fallback attempt if requested languages not found
    if not vtt_files:
        best_fallbacks = get_best_available_subtitle_langs(meta)
        if best_fallbacks:
            fallback_query = ",".join(best_fallbacks[:3])
            print(f"[*] Subtitle bahasa '{sub_langs}' tidak ditemukan. Beralih ke cadangan: {fallback_query}...", file=sys.stderr)
            vtt_files = try_download_subs(fallback_query)

    if not vtt_files:
        print("No subtitle files found for this video.", file=sys.stderr)
        return None

    # Prioritize languages based on requested order, else pick first available
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
            "chapters": chapters,
            "description": description[:1000]
        },
        "total_chunks": len(chunks),
        "chunks": chunks
    }

    if output_json:
        with open(output_json, 'w', encoding='utf-8') as out:
            json.dump(result, out, ensure_ascii=False, indent=2)

    return result
