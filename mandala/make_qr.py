# 골든만다라 QR 생성기 — 배포 주소가 바뀌면 BASE만 고치고 다시 실행
#   python3 make_qr.py            → qr/mandala_1.png ~ mandala_5.png + signs.html
#   (필요 패키지: pip install qrcode pillow)
import os, base64, io, qrcode

BASE = "https://yoga-miryang.vercel.app/mandala/"   # ← 실제 배포 주소로 변경 (끝에 / 포함)
SPOTS = {1: "m7k2", 2: "r4q9", 3: "z2p6", 4: "h8w3", 5: "t5n1"}   # index.html 의 SPOTS 와 동일해야 함
NAMES = ["메인무대 근처", "플레이그라운드", "푸드존", "파라솔 휴게존", "부스라인 A"]

os.makedirs("qr", exist_ok=True)
imgs = {}
for n, k in SPOTS.items():
    url = f"{BASE}?s={n}&k={k}"
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=2)
    q.add_data(url); q.make(fit=True)
    im = q.make_image(fill_color="#2a3a8a", back_color="white").convert("RGB")
    im.save(f"qr/mandala_{n}.png")
    b = io.BytesIO(); im.save(b, "PNG"); imgs[n] = base64.b64encode(b.getvalue()).decode()
    print(n, url)

cards = "".join(f'''
<section class="sign">
  <img class="m" src="../img/icon_mandala.png" alt="">
  <div class="no">골든만다라 {n} / 5</div>
  <h1>{NAMES[n-1]}</h1>
  <img class="qr" src="data:image/png;base64,{imgs[n]}" alt="">
  <p class="howto">휴대폰 카메라로 QR을 찍으세요<br><small>Scan with your phone camera · फ़ोन कैमरे से स्कैन करें</small></p>
  <p class="code">QR이 안 되면 앱에서 코드 입력 → <b>{SPOTS[n].upper()}</b></p>
  <p class="foot">5개를 모으면 35번 부스에서 인생네컷 무료 출력 ✨<br>제10회 밀양국제요가컨퍼런스 · 가곡원류</p>
</section>''' for n in SPOTS)

html = f'''<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>골든만다라 표지판 (A4 인쇄용)</title>
<link href="https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;700&family=Fredoka:wght@600&display=swap" rel="stylesheet">
<style>
@page{{size:A4 portrait;margin:0}}
body{{margin:0;font-family:"Noto Sans KR",sans-serif;color:#25304e;background:#eee}}
.sign{{width:210mm;height:297mm;margin:0 auto;background:#fff8ea;position:relative;overflow:hidden;page-break-after:always;text-align:center;padding:22mm 18mm;box-sizing:border-box;border:6mm solid #e5b640}}
.sign .m{{width:48mm;height:48mm;object-fit:contain;filter:drop-shadow(0 6px 12px rgba(229,182,64,.5))}}
.no{{font-family:Fredoka,Jua,sans-serif;font-size:9mm;color:#8a6a10;margin-top:4mm}}
h1{{font-family:Jua,sans-serif;font-weight:400;font-size:17mm;color:#2a3a8a;margin:2mm 0 6mm}}
.qr{{width:95mm;height:95mm;border-radius:8mm;background:#fff;padding:4mm;box-shadow:0 8px 24px rgba(42,58,138,.12)}}
.howto{{font-size:7mm;margin:6mm 0 0;font-family:Jua,sans-serif;color:#2a3a8a}}.howto small{{font-size:4mm;color:#66708c;font-family:"Noto Sans KR",sans-serif}}
.code{{font-size:5mm;margin-top:5mm;color:#66708c}}.code b{{font-family:Fredoka,sans-serif;font-size:9mm;letter-spacing:2mm;color:#8a6a10;background:#fff;padding:1mm 4mm;border-radius:3mm;border:1px dashed #e5b640}}
.foot{{position:absolute;left:0;right:0;bottom:12mm;font-size:4.2mm;color:#8a6a10;line-height:1.6}}
@media screen{{.sign{{margin:10mm auto}}}}
</style></head><body>{cards}</body></html>'''
open("signs.html", "w", encoding="utf-8").write(html)
print("→ qr/*.png, signs.html 생성 완료 (브라우저에서 열어 인쇄 → A4 5장)")
