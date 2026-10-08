# ai_reel_montaj — Claude Code skill

O'z bazasiga ega reel montaj skilli (O'zbek ekspert/podkast reellari, 9:16).

- **A rejim — muallifni o'rganish.** Bitta odamning har xil reellari havolasi beriladi. Skill ularni yuklab, har birini to'liq tahlil qiladi
  (transkript, kesimlar, ritm, rang, audio, SFX) va har video, har element bo'yicha inventar tuzadi: vaqt, joy (%), shrift
  (nomzodlar bilan tekshirilgan), kirish/chiqish. Natija — `baza/<muallif>/PASSPORT.md` + `INVENTORY.md` + `elements.html` (HyperFrames bloklari).
- **B rejim — montaj.** Foydalanuvchi videosi muallifning HAMMA videolari uslubida montaj qilinadi. Doim **2 ta har xil variant**
  (A minimal / B boyroq), bitta reja → "boshla" → render → referens bilan raqamli solishtirish.

## Tarkib
| Fayl | Vazifa |
|---|---|
| `SKILL.md` | skill ko'rsatmasi (ish tartibi, qoidalar) |
| `scripts/learn.py` | havolalarni yuklash (yt-dlp) + tahlil + median/oraliq jadvali |
| `scripts/ov.sh`, `scripts/strips.sh` | umumiy va vaqtli 18 kadrlik varaqlar |
| `baza/INDEX.md` | o'rganilgan mualliflar |
| `baza/asror/` | birinchi muallif: Asror Iskandarov (17 reel) — pasport, to'liq inventar, elementlar andozasi |

## Talablar
- [Claude Code](https://claude.com/claude-code) + HyperFrames (`npx hyperframes`), ffmpeg ≥ 5.1, yt-dlp, Python venv (faster-whisper, opencv, pillow, numpy).
- Bu skill `reel-montaj` va `reel-uslub` skillari ustiga qurilgan (`ref_analyze.py`, `tr.py`, `grade_match.py`, `style_compare.py`,
  shriftlar va andozalar o'shalarda) — ular bu repoda yo'q.
- Referens videolar repoga kiritilmaydi (mualliflik huquqi); ular lokal `AbuDev/ai-reel-baza/_src/` da saqlanadi.

## O'rnatish
```bash
git clone https://github.com/asositgroup/ai_reel_montaj ~/.claude/skills/ai_reel_montaj
```
