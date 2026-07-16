#!/usr/bin/env python3
"""Clean a YouTube auto-caption VTT into a timestamped transcript.

Usage: python clean_vtt.py <file.vtt> [bucket_seconds]

Writes the transcript to stdout, one line per time bucket: [MMM:SS] text
Auto-subs repeat each caption line across consecutive cues; duplicates are
dropped and the surviving lines merged into ~bucket_seconds buckets
(default 30).
"""
import re
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    bucket_secs = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    entries = []  # (cue_start_seconds, text)
    cur = None
    with open(path, encoding="utf-8") as f:
        for ln in f.read().splitlines():
            m = re.match(r"^(\d+):(\d+):(\d+)\.\d+ --> ", ln)
            if m:
                cur = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
                continue
            if cur is None or not ln.strip():
                continue
            if ln.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
                continue
            txt = re.sub(r"<[^>]+>", "", ln).strip()
            if txt and (not entries or txt != entries[-1][1]):
                entries.append((cur, txt))

    def flush(start, parts):
        print(f"[{start // 60:03d}:{start % 60:02d}] {' '.join(parts)}")

    bucket_start, bucket_txt = None, []
    for ts, txt in entries:
        if bucket_start is None:
            bucket_start = ts
        if ts - bucket_start >= bucket_secs and bucket_txt:
            flush(bucket_start, bucket_txt)
            bucket_start, bucket_txt = ts, []
        bucket_txt.append(txt)
    if bucket_txt:
        flush(bucket_start, bucket_txt)


if __name__ == "__main__":
    main()
