#!/bin/zsh
# strips.sh <muallif> <out_nomi> <id> <t0:dur> [<t0:dur> ...]  -> <muallif>/motion/<out>.jpg
# har oyna = 18 kadr (9x2), kadr vaqti tepada; oynalar ustma-ust
B=${AI_REEL_BAZA:-~/Desktop/AI-Videos/AbuDev/ai-reel-baza}; cd $B/_src
a=$1; o=$2; id=$3; shift 3; mkdir -p ../$a/motion; L=()
for w in "$@"; do t=${w%%:*}; d=${w##*:}
  ~/Desktop/AI-Videos/.venv/bin/python - "$id" "$t" "$d" "/tmp/st_$t.jpg" <<'P'
import sys,subprocess,os
from PIL import Image,ImageDraw,ImageFont
id,t,d,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
ft=ImageFont.truetype(os.path.expanduser("~/.claude/skills/reel-montaj/assets/fonts/Inter-var.ttf"),20)
tiles=[]
for k in range(18):
    tt=t+d*k/17; f=f"/tmp/sf_{k}.png"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{tt:.3f}","-i",f"{id}.mp4","-frames:v","1","-vf","scale=216:384",f],check=True)
    im=Image.open(f).convert("RGB"); ImageDraw.Draw(im).text((4,4),f"{tt:.2f}",font=ft,fill=(255,255,0)); tiles.append(im)
o=Image.new("RGB",(216*9,384*2))
for k,im in enumerate(tiles): o.paste(im,((k%9)*216,(k//9)*384))
o.save(out,quality=85)
P
  L+=(/tmp/st_$t.jpg); done
ffmpeg -v error -y $(for f in $L; do echo -i $f; done) -filter_complex "vstack=${#L}" ../$a/motion/$o.jpg 2>/dev/null || cp $L[1] ../$a/motion/$o.jpg
echo ../$a/motion/$o.jpg
