---
name: ai_reel_montaj
description: O'zining bazasiga ega montaj skilli — foydalanuvchi BITTA odamning (muallifning) har xil videolarini havola qilib yuboradi, skill ularni /reel-montaj usulida to'liq tahlil qilib "muallif pasporti"ga (baza) saqlaydi; keyin foydalanuvchi o'z videosini tashlasa, uni ham to'liq tahlil qilib, AYNAN shu muallif videolari dizayni/uslubida (barcha videolari birgalikda) premium, silliq reel qilib montaj qiladi. "/ai_reel_montaj", "ai reel montaj", "shu odamning videolarini o'rgan", "bazaga qo'sh", "<muallif> uslubida montaj qil", "bazadagi uslubda montaj qil" so'rovlarida ishlat.
---

# AI reel montaj (o'z bazasi bo'yicha muallif uslubida)

Ish tili: **o'zbekcha**. Bu skill `reel-montaj` + `reel-uslub` ustiga qurilgan:
- avval `~/.claude/skills/reel-montaj/SKILL.md` ni o'qi — **9 ta qat'iy qoida va ish tartibi to'liq amal qiladi**
  (reja → "boshla" → montaj; sinxron; yuzga tushmaydi; B-roll odamlari; papkalar; ElevenLabs/kie.ai yo'q; HAMMA NARSA SILLIQ;
  musiqa ovozni to'smaydi);
- `reel-montaj/references/lessons.md`, `smooth-motion.md`, `sfx-lexicon.md` — har loyihada;
- rang/solishtirish: `reel-uslub/scripts/grade_match.py`, `style_compare.py` (ko'p referensni qabul qiladi).

Farqi: uslub manbasi umumiy design-library emas, balki **shu skillning o'z bazasi** — har muallif uchun alohida pasport,
u muallifning BARCHA o'rganilgan videolaridan (median + oraliq) tuziladi. Bitta videoni tanlab olinmaydi.

**Ustuvorlik:** foydalanuvchi qoidalari > muallif uslubi. Muallifda bo'lsa ham olinmaydi: overshoot/elastic/tepki
(→ smooth-motion ekvivalenti), ovozni to'sadigan musiqa, film/TV parchalari (→ Pexels), qoida 4 ga zid B-roll odamlari.
Har moslashni pasportning "OLINMAYDI" bo'limida ochiq yoz.

## Baza
| Nima | Qayerda |
|---|---|
| Skill bazasi (indeks + pasportlar) | `~/.claude/skills/ai_reel_montaj/baza/INDEX.md`, `baza/<muallif>/PASSPORT.md` |
| Videolar va og'ir tahlil | `~/Desktop/AI-Videos/AbuDev/ai-reel-baza/_src/<id>.mp4`, `_src/<id>_an/` |
| Muallif ro'yxati / metrikalar | `AbuDev/ai-reel-baza/<muallif>/videos.json`, `metrics_agg.md`, `strips/` |
| Muallif elementlari andozasi | `baza/<muallif>/elements.html` (HyperFrames bloklari, lint 0 xato) |
Windows'da: `~/OneDrive/Ishchi stol/AbuDev/ai-reel-baza` (`AI_REEL_BAZA` env bilan). Python: `~/Desktop/AI-Videos/.venv/bin/python`.

## Rejim A — muallifni o'rganish (foydalanuvchi havolalar yuboradi)
1. **Muallif nomi/slug** (masalan `islomxon`) — aniqlanmasa havoladagi uploader'dan ol yoki so'ra. `baza/INDEX.md` da borligini
   tekshir — bor bo'lsa yangi videolar shu pasportga QO'SHILADI (qayta tahlil qilinmaydi).
2. Yuklash + tahlil (har video reel-montaj 1b usulida: texnik, transkript, beat'lar, kesimlar va nutqqa munosabati, ritm,
   grade, kamera, audio, SFX, kontakt varaqlar, video-use timeline_view):
   ```bash
   ~/Desktop/AI-Videos/.venv/bin/python ~/.claude/skills/ai_reel_montaj/scripts/learn.py <muallif> <havola1> <havola2> ...
   ```
   Uzun ish — fonda ishga tushir va foydalanuvchiga holat yoz. Instagram'ga login qilinmaydi; yopiq bo'lsa fayl so'ra.
   Tarmoq uzilsa yuklanmagan havolalar `XATO:` bilan o'tkaziladi — oxirida faqat ularni qayta ishga tushir (tayyorlari qayta tahlil qilinmaydi).
   Takror havolalarni (bir xil id) bir marta ber.
3. **KO'Z bilan**: avval har video uchun umumiy varaq `scripts/ov.sh <muallif> <id>` (18 kadr + qisqa metrika) → `strips/<id>_ov.jpg`
   ni KO'R va `AbuDev/ai-reel-baza/<muallif>/notes.md` ga kuzatuv yoz (video tayyor bo'lishi bilan, keyinga qoldirmay). So'ng har video `report.md`, `contact_*.jpg`, `tv_*.png` ni KO'R. Har grafik element (matn, plashka, karta, raqam,
   o'tish, CTA) kirishi uchun 18 kadrlik strip (`-ss T -t 0.62 -vf scale=216:-1,tile=9x2`) → `strips/` — kirish/chiqish
   vaqti, ease, blur, joylashuv, rang (hex), shrift turi. Vaqtni avval kontakt varaqdan aniq hisobla (lessons.md).
3b. **TO'LIQ INVENTAR — MAJBURIY (foydalanuvchi talabi 2026-10-08: "montaj uslublari hamma narsasiga e'tibor ber").**
   Umumiy varaq bilan cheklanma. HAR video uchun: 1 fps vaqtli varaqlar (`full/R##_*.jpg`, har 40 s) → har grafik hodisa uchun
   `scripts/strips.sh <muallif> <nom> <id> t0:dur ...` (18 kadr, kadr vaqti yozilgan; bitta rasmga ≤3 oyna — ko'p bo'lsa mayda chiqadi) →
   `baza/<muallif>/INVENTORY.md` ga jadval: **Vaqt · Element · Joy (x/y %) · Kirish (turi, davomiyligi) · Turish (kesimdan o'tadimi) · Chiqish**.
   Shrift — referens kesmasini nomzod shriftlar bilan yonma-yon render qilib tekshir (`fonts_id/`), ko'z bilan taxmin qilma.
   Joylashuv — % to'r chizilgan kadrlarda o'lcha (`pos/`). Hech bir videoni "o'xshash" deb o'tkazib yuborma.
4. `baza/<muallif>/PASSPORT.md` yoz (INVENTORY'dan chiqqan qoidalar alohida bo'lim — kirish turlari, overlay kesimdan o'tishi, bob sarlavha turlari, huk turlari, o'tishlar) (andoza: pastdagi "Pasport tuzilmasi"; namunasi —
   `AbuDev/design-library/oila-O-iman/PASSPORT.md`). Raqamlar `metrics_agg.md` dan, elementlar strip'lardan — taxmin emas.
5. `baza/<muallif>/elements.html` (sinov loyihasi `AbuDev/ai-reel-baza/<muallif>/hf_demo/`, fon — referensdan 16 s parcha) — muallifning asosiy elementlari HyperFrames bloklari sifatida (smooth-motion qiymatlari bilan),
   `npx hyperframes lint` 0 xato + snapshot bilan tekshirilgan. Mavjud andozalardan boshla (`reel-montaj/templates/`).
6. `baza/INDEX.md` ga qator, foydalanuvchiga qisqa hisobot: nechta video, uslubning 5–7 asosiy belgisi, kalit kadrlar varag'i,
   nimalar OLINMAYDI. Xotiraga (MEMORY.md) qisqa yozuv.

## Rejim B — montaj (foydalanuvchi o'z videosini tashlaydi)
> **QAT'IY (foydalanuvchi talabi 2026-10-08): har yangi video uchun DOIM 2 TA HAR XIL MONTAJ tayyorlanadi va ikkalasi topshiriladi** —
> foydalanuvchi alohida so'ramasa ham. Ikkalasi ham shu muallif uslubida, lekin bir-biridan ko'zga yaqqol farq qiladi:
> | | Variant A | Variant B |
> |---|---|---|
> | Qolip | videoga eng mos qolip (pasport 1-bo'lim) | ikkinchi mos qolip yoki o'sha qolipning boshqa yo'li |
> | Huk | bir turi (masalan metall raqam + 3 darajali sarlavha) | boshqa turi (masalan split + oq pill / 4 darajali sarlavha + IG teg) |
> | Bob/band sarlavhasi | bir tur (masalan "#N qaror") | boshqa tur (masalan "#N - qoida" typewriter yoki "#N Sabab." shisha karta) |
> | Grafika zichligi | MINIMAL (eng mashhur R15/R17 kabi: sarlavha + raqam + [subtitr] + oq-qora B-roll) | BOYROQ (ro'yxat/pill stack, kartalar, progress bar, CTA karta) |
> | B-roll / musiqa | bir to'plam, bir trek | boshqa to'plam, boshqa trek (ikkalasi ham qoida 9) |
> Umumiy (ikkalasida bir xil): sinxron manba, transkript, grading, subtitr matni, qoidalar 1–9.
> Reja bitta: ikkala variant jadvali yonma-yon → bitta "boshla" ikkalasini tasdiqlaydi (foydalanuvchi bittasini o'zgartirsa — o'shani).
> Topshirish: `3_tayyor/<Nom>_A_v1.mp4` va `<Nom>_B_v1.mp4` + ikkalasining telefon nusxasi, hisobotda farqlar jadvali va har biri uchun style_compare.
1. Qaysi muallif uslubida? Aytilmasa va bazada bitta muallif bo'lsa — o'sha; bir nechta bo'lsa — so'ra.
2. Foydalanuvchi videosini **to'liq tahlil**: reel-montaj 0–1 (`new_project.py`, ffprobe, kontakt varaq, `tr.py` transkript,
   matnni adabiy o'zbekchaga tikla) + `ref_analyze.py` (o'z videosining metrikalari — pasport maqsadlaridan qancha farq).
3. Qolip tanlash: pasport 1-bo'limi (foydalanuvchi videosi formati → muallifning qaysi qolipi).
4. Rang: `grade_match.py <muallifning hamma videolari vergul bilan> <manba.mp4> analysis` → `grade_match.jpg` ni KO'R.
5. **Reja → TASDIQ** (A va B variant yonma-yon): transkript + beat-ma-beat jadval
   `| Vaqt | Gap | Muallifdagi mos element (R#, vaqti) | Bizdagi element |` + muallifdan 3–4 kalit kadr; ❓ savollar
   (handle/avatar, musiqa, pauza kesish). **"boshla" demaguncha qurma.**
6. Montaj: `baza/<muallif>/elements.html` bloklari + reel-montaj 3–5 (manba, aktivlar, kompozitsiya, smooth_check = 0).
7. Render + tekshiruv: reel-montaj 6 + `ref_analyze.py` natijaga → `style_compare.py <muallif hamma metrics.json> analysis/out_an/metrics.json`
   → `FARQ` larni tuzat (≤3 aylanish) — HAR IKKI variant uchun. Topshirish `MY - Videos/<Mavzu>/3_tayyor/` (A va B), hisobotda style_compare jadvali.
8. Foydalanuvchi tuzatishlari muallifga oid bo'lsa — pasportga ("Tuzatishlar" bo'limi) yoz, keyingi montajlar shuni oladi.

## Pasport tuzilmasi (`baza/<muallif>/PASSPORT.md`)
0. Muallif: ism, @handle, mavzu, auditoriya; videolar jadvali R1…Rn (id, sarlavha, davomiylik, like, format, asosiy hissasi).
1. Qoliplar: foydalanuvchi videosi turi → qolip → elementlar (monolog / suhbat / ko'cha / ekran yozuvi …).
2. Tuzilma: HUK → … → CTA, beat vaqtlari (median), huk turlari misollari.
3. Raqamli maqsadlar: `metrics_agg.md` jadvali (median / oraliq) + izoh.
4. Matn tizimi: shrift(lar) + bizdagi nomzod, o'lcham (px @1080), rang hex, bo'laklash, joylashuv (yuzga tushmaydi), urg'u usuli.
5. Grafik elementlar: har biri — qachon ishlatiladi, kirish/chiqish (o'lchangan → bizdagi smooth qiymat), R# manbasi.
6. Montaj: kesim ritmi, kamera (statik/zoom/ko'p kamera), o'tishlar, B-roll turi va ulushi.
7. Rang: grade_match buyrug'i (hamma videolar), vinyetka/oq-qora qoidalari.
8. Audio: musiqa turi, SFX lug'ati (nimaga bog'langan), bizning qoida 9 darajasi.
9. CTA / yakun.
10. OLINMAYDI (sababi bilan). 11. style_compare buyrug'i. 12. Tuzatishlar (foydalanuvchidan, sana bilan).

## Skriptlar
- `scripts/ov.sh <muallif> <id>` — 18 kadrlik umumiy varaq + metrika qatori.
- `scripts/strips.sh <muallif> <nom> <id> t0:dur ...` — har hodisa uchun 18 kadrlik vaqtli strip (kirish/chiqish o'lchovi).
- `scripts/learn.py <muallif> <havola|fayl>... | --agg` — yuklash (yt-dlp, info.json), `ref_analyze.py` (allaqachon bo'lsa
  o'tkazadi), `videos.json` va `metrics_agg.md` (median/oraliq + style_compare argumentlari).
- reel-montaj: `ref_analyze.py`, `tr.py`, `prep.py`, `matte.py`, `broll_*`, `music_pick.py`, `mix_audio.py`, `smooth_check.py`, `av_check.py`.
- reel-uslub: `grade_match.py`, `style_compare.py`.
