#!/usr/bin/env python3
"""ai_reel_montaj — bitta muallifning videolarini bazaga o'rganish.

  python learn.py <muallif-slug> <havola|fayl> [<havola|fayl> ...]
  python learn.py <muallif-slug> --agg            # faqat yig'ma jadvalni qayta hisobla

Har video: _src/<id>.mp4 (+info.json) -> reel-montaj ref_analyze.py -> _src/<id>_an/{report.md,metrics.json,...}.
Oxirida <baza>/<slug>/videos.json (ro'yxat) va <baza>/<slug>/metrics_agg.md (median / oraliq) yoziladi.
Allaqachon tahlil qilingan video qayta tahlil qilinmaydi.
"""
import json, os, re, shutil, statistics, subprocess, sys

HOME = os.path.expanduser("~")
BAZA = os.environ.get("AI_REEL_BAZA", os.path.join(HOME, "Desktop/AI-Videos/AbuDev/ai-reel-baza"))
SRC = os.path.join(BAZA, "_src")
PY = os.path.join(HOME, "Desktop/AI-Videos/.venv/bin/python")
PY = PY if os.path.exists(PY) else sys.executable
REF_AN = os.path.join(HOME, ".claude/skills/reel-montaj/scripts/ref_analyze.py")
YTDLP = shutil.which("yt-dlp") or os.path.join(HOME, ".local/bin/yt-dlp")

KEYS = [("dur", "Davomiylik, s"), ("fps", "FPS"), ("lufs", "LUFS"), ("wpm", "So'z/daqiqa"),
        ("long_pauses", "Uzun pauzalar (≥0.4 s)"), ("cut_every_s", "Kesim har N s"), ("shot_median_s", "Kadr median, s"),
        ("cuts_in_speech_share", "Gap o'rtasida kesim"), ("luma_p50", "O'rta yorug'lik"), ("contrast", "Kontrast"),
        ("sat", "To'yinganlik"), ("warm", "Iliqlik (R−B)"), ("motion", "Kamera harakati"), ("bw_shots", "Oq-qora kadrlar"),
        ("speech_minus_pause_db", "Nutq − pauza, dB"), ("bass_share_db", "Bas ulushi, dB"), ("sfx_onsets", "SFX zarbalari"),
        ("sfx_on_cuts", "SFX kesimda")]


def clean_url(u):
    u = u.split("?")[0].rstrip("/")
    return u + "/"


def vid_id(u):
    m = re.search(r"/(?:reel|reels|p|tv|shorts|video)/([^/?#]+)", u)
    return m.group(1) if m else re.sub(r"\W+", "_", u)[-24:]


def fetch(item):
    if os.path.exists(item):
        stem = os.path.splitext(os.path.basename(item))[0]
        dst = os.path.join(SRC, stem + ".mp4")
        if not os.path.exists(dst):
            shutil.copy2(item, dst)
        return stem
    url = clean_url(item)
    vid = vid_id(url)
    if not os.path.exists(os.path.join(SRC, vid + ".mp4")):
        subprocess.run([YTDLP, "-q", "-o", os.path.join(SRC, vid + ".%(ext)s"), "--merge-output-format", "mp4",
                        "--write-info-json", url], check=True)
    return vid


def analyze(vid):
    an = os.path.join(SRC, vid + "_an")
    if os.path.exists(os.path.join(an, "metrics.json")):
        print(f"  {vid}: tahlil bor, o'tkazildi")
        return
    with open(an + ".log", "w") as log:
        subprocess.run([PY, REF_AN, os.path.join(SRC, vid + ".mp4"), an], stdout=log, stderr=subprocess.STDOUT, check=True)
    print(f"  {vid}: tahlil tayyor -> {an}/report.md")


def info(vid):
    p = os.path.join(SRC, vid + ".info.json")
    if not os.path.exists(p):
        return {}
    d = json.load(open(p))
    if (d.get("title") or "").startswith("Video by") and d.get("description"):
        d["title"] = d["description"].strip().split("\n")[0]
    return {k: d.get(k) for k in ("uploader", "channel", "title", "like_count", "comment_count", "view_count",
                                  "upload_date", "webpage_url", "duration")}


def aggregate(slug):
    d = os.path.join(BAZA, slug)
    vids = json.load(open(os.path.join(d, "videos.json")))
    rows, ms = [], []
    for i, v in enumerate(vids, 1):
        mp = os.path.join(SRC, v["id"] + "_an", "metrics.json")
        if os.path.exists(mp):
            ms.append((f"R{i}", json.load(open(mp))))
    out = [f"# {slug} — {len(ms)} video metrikalari (median / oraliq)\n",
           "| Ko'rsatkich | Median | Oraliq | " + " | ".join(r for r, _ in ms) + " |",
           "|---|---|---|" + "---|" * len(ms)]
    for k, name in KEYS:
        vals = [m.get(k) for _, m in ms]
        nums = [x for x in vals if isinstance(x, (int, float))]
        if not nums:
            continue
        f = (lambda x: f"{x:.3g}" if isinstance(x, (int, float)) else "–")
        out.append(f"| {name} | {f(statistics.median(nums))} | {f(min(nums))}…{f(max(nums))} | "
                   + " | ".join(f(x) for x in vals) + " |")
    out.append("\n| R | id | Sarlavha | Like | Davomiylik |\n|---|---|---|---|---|")
    for i, v in enumerate(vids, 1):
        t = (v.get("title") or "").replace("\n", " ").replace("|", "/")[:70]
        dur = v.get("duration") or dict(ms).get(f"R{i}", {}).get("dur") or "–"
        out.append(f"| R{i} | {v['id']} | {t} | {v.get('like_count') or '–'} | {dur} |")
    out.append("\nstyle_compare uchun:\n```\n" + " ".join(f"$S/{v['id']}_an/metrics.json" for v in vids) + "\n```")
    open(os.path.join(d, "metrics_agg.md"), "w").write("\n".join(out) + "\n")
    print(f"-> {d}/metrics_agg.md")


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    slug, items = sys.argv[1], sys.argv[2:]
    d = os.path.join(BAZA, slug)
    os.makedirs(d, exist_ok=True)
    os.makedirs(SRC, exist_ok=True)
    vj = os.path.join(d, "videos.json")
    vids = json.load(open(vj)) if os.path.exists(vj) else []
    if items != ["--agg"]:
        for it in items:
            print(f"* {it}")
            try:
                vid = fetch(it)
                analyze(vid)
            except subprocess.CalledProcessError as e:
                print(f"  XATO: {it}: {e}")
                continue
            if vid not in [v["id"] for v in vids]:
                vids.append({"id": vid, **info(vid)})
        json.dump(vids, open(vj, "w"), ensure_ascii=False, indent=1)
    aggregate(slug)


if __name__ == "__main__":
    main()
