#!/bin/zsh
# ov.sh <muallif> <id> [n=18] -> ai-reel-baza/<muallif>/strips/<id>_ov.jpg (n kadr teng oraliqda, 6 ustun) + qisqa info
B=${AI_REEL_BAZA:-~/Desktop/AI-Videos/AbuDev/ai-reel-baza}; cd $B/_src
a=$1; id=$2; n=${3:-18}; mkdir -p ../$a/strips
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $id.mp4)
ffmpeg -v error -y -i $id.mp4 -vf "fps=$(python3 -c "print(${n}/${d})"),scale=300:-1,tile=6x$(( (n+5)/6 )):padding=3" -frames:v 1 ../$a/strips/${id}_ov.jpg
python3 - <<P
import json;d=json.load(open("$id.info.json"));m=json.load(open("${id}_an/metrics.json"))
print(d.get("description","")[:150].replace("\n"," "),"| like",d.get("like_count"),"| dur",m["dur"],"fps",m["fps"],"| cut/s",m["cut_every_s"],"| wpm",m["wpm"],"| luma",m["luma_p50"],"warm",m["warm"],"| sp-pause",m["speech_minus_pause_db"])
P
