#!/usr/bin/env python3
"""news-23 b47 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024, 31 stories. Scenes are drawn illustrations, not photographs."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu"

def fb(sz):  return ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", sz)
def fr(sz):  return ImageFont.truetype(f"{FD}/DejaVuSans.ttf", sz)
def serif(sz): return ImageFont.truetype(f"{FD}/DejaVuSerif-Bold.ttf", sz)

# palette
BLACK = (0, 0, 0); WHITE = (255, 255, 255); GOLD = (212, 175, 55)
RED = (178, 34, 34); DARKRED = (139, 0, 0); NAVY = (13, 27, 62)
TEAL = (14, 124, 123); CREAM = (245, 238, 218); GREY = (90, 90, 90)
LBLUE = (210, 225, 240); LGREEN = (150, 205, 150); DARKBLUE = (20, 40, 90)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, color):
    f = fb(10)
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([x, y, x + tw + 10, y + 14], radius=2, fill=color)
    d.text((x + 5, y + 1), label, font=f, fill=WHITE)
    return tw + 10

# ---------- masthead ----------
d.rectangle([0, 0, W, 56], fill=BLACK)
d.text((14, 8), "THE WORLD TODAY", font=serif(40), fill=WHITE)
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 14 - d.textlength(dt, font=fb(20)), 16), dt, font=fb(20), fill=GOLD)

# ---------- kicker ----------
d.text((14, 60), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=fb(13), fill=RED)

# ---------- number strip (2 rows x 5 cols) ----------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", (30, 90, 160)),
    ("11,762", "EBOLA CASES, DRC", (20, 120, 60)), ("10T won", "SEOUL STABILISATION FUND", (150, 110, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", (120, 60, 160)),
    ("$450M", "SKUBAL DEAL", (130, 40, 140)), ("165", "RUSSIAN MISSILES IN A WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", (30, 90, 160)), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", (150, 110, 0)),
    ("$107.3B", "ANTHROPIC IPO \u2014 LARGEST", (120, 60, 160)),
]
cw = W // 5
for i, (num, lab, col) in enumerate(nums):
    x = (i % 5) * cw + 10
    y = 80 + (i // 5) * 34
    d.text((x, y), num, font=fb(22), fill=col)
    d.text((x, y + 24), lab, font=fb(9), fill=BLACK)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", 290, (0, 128, 128)), ("AMERICAS 8", 290, (30, 60, 140)),
           ("MIDDLE EAST 6", 190, (150, 110, 0)), ("EUROPE 5", 116, (120, 60, 160)),
           ("AFRICA 3", 66, (190, 40, 40)), ("WORLD 2", 72, (60, 60, 60))]
x = 0
for label, wdt, col in regions:
    d.rectangle([x, 148, x + wdt, 166], fill=col)
    tw = d.textlength(label, font=fb(10))
    d.text((x + (wdt - tw) / 2, 152), label, font=fb(10), fill=WHITE)
    x += wdt

# ---------- UTC strip ----------
d.rectangle([0, 166, W, 182], fill=NAVY)
d.text((10, 169), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 IPO $97.17",
       font=fr(10), fill=WHITE)
d.text((W - 10 - d.textlength("~ APPROX", font=fr(10)), 169), "~ APPROX", font=fr(10), fill=(180, 180, 180))

# ---------- hero scenes ----------
HX = [0, 341, 683]
HW = [341, 342, 341]
SC_Y, SC_H = 182, 140
CAP_Y, CAP_H = 322, 14

# scene 1: Kospi chart
d.rectangle([HX[0], SC_Y, HX[0] + HW[0], SC_Y + SC_H], fill=NAVY)
d.text((HX[0] + 10, SC_Y + 4), "-3.3%", font=fb(34), fill=(255, 90, 80))
pts = [(HX[0] + 12 + i * 32, SC_Y + 78 - v) for i, v in enumerate([18, 30, 22, 38, 26, 34, 20, 30, 24, 32])]
d.line(pts, fill=(255, 120, 100), width=2)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 90))
# skyline
import random
random.seed(47)
bx = HX[0] + 8
while bx < HX[0] + HW[0] - 12:
    bw = random.randint(16, 26); bh = random.randint(28, 62)
    d.rectangle([bx, SC_Y + SC_H - bh, bx + bw, SC_Y + SC_H], fill=(24, 44, 92))
    for wy in range(SC_Y + SC_H - bh + 5, SC_Y + SC_H - 4, 9):
        for wx in range(bx + 3, bx + bw - 3, 7):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 100))
    bx += bw + 3
d.rectangle([HX[0], CAP_Y, HX[0] + HW[0], CAP_Y + CAP_H], fill=BLACK)
d.text((HX[0] + 8, CAP_Y + 1), "KOSPI 4,708.54  \u00b7  -161 PTS", font=fb(10), fill=WHITE)

# scene 2: Guterres
d.rectangle([HX[1], SC_Y, HX[1] + HW[1], SC_Y + SC_H], fill=TEAL)
d.text((HX[1] + 10, SC_Y + 6), "150 DELEGATES", font=fb(30), fill=GOLD)
d.text((HX[1] + 10, SC_Y + 40), "BACK A RISK", font=fb(30), fill=WHITE)
d.text((HX[1] + 10, SC_Y + 74), "FRAMEWORK", font=fb(30), fill=WHITE)
gx, gy, gr = HX[1] + HW[1] - 34, SC_Y + SC_H - 30, 22
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=WHITE, width=2)
d.ellipse([gx - gr + 7, gy - gr, gx + gr - 7, gy + gr], outline=WHITE, width=1)
d.line([gx - gr, gy, gx + gr, gy], fill=WHITE, width=1)
d.rectangle([HX[1], CAP_Y, HX[1] + HW[1], CAP_Y + CAP_H], fill=BLACK)
d.text((HX[1] + 8, CAP_Y + 1), "UN  \u00b7  BRIDGETOWN", font=fb(10), fill=WHITE)

# scene 3: power bars
d.rectangle([HX[2], SC_Y, HX[2] + HW[2], SC_Y + SC_H], fill=CREAM)
d.text((HX[2] + 10, SC_Y + 4), "NARROWEST SINCE 2018", font=fb(12), fill=BLACK)
d.text((HX[2] + HW[2] - 10 - d.textlength("GAP 5.3", font=fb(12)), SC_Y + 4), "GAP 5.3", font=fb(12), fill=(170, 130, 20))
bars = [("78.9", "US", NAVY, 96), ("73.6", "CHINA", RED, 88), ("40.5", "INDIA", (190, 150, 30), 52)]
bx = HX[2] + 14
for val, lab, col, bh in bars:
    d.rectangle([bx, SC_Y + 26, bx + 92, SC_Y + 26 + bh], fill=col)
    d.text((bx + 46 - d.textlength(val, font=fb(15)) / 2, SC_Y + 30), val, font=fb(15), fill=WHITE)
    d.text((bx + 46 - d.textlength(lab, font=fb(11)) / 2, SC_Y + 26 + bh - 18), lab, font=fb(11), fill=WHITE)
    bx += 104
d.rectangle([HX[2], CAP_Y, HX[2] + HW[2], CAP_Y + CAP_H], fill=BLACK)
d.text((HX[2] + 8, CAP_Y + 1), "ASIA POWER INDEX 2026", font=fb(10), fill=WHITE)

# ---------- hero text ----------
heroes = [
    ("1", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
     "KOREA EXCHANGE"),
    ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS"),
    ("3", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (num, head, body, src) in enumerate(heroes):
    x0 = HX[i] + 10
    wmax = HW[i] - 20
    y = 340
    # number badge
    d.ellipse([x0, y + 2, x0 + 16, y + 18], fill=RED)
    d.text((x0 + 5, y + 3), num, font=fb(11), fill=WHITE)
    hl = wrap(head, fb(16), wmax - 22)
    hy = y
    for ln in hl:
        d.text((x0 + 22, hy), ln, font=fb(16), fill=BLACK)
        hy += 19
    by = hy + 2
    bl = wrap(body, fr(11), wmax)
    for ln in bl:
        d.text((x0, by), ln, font=fr(11), fill=BLACK)
        by += 13
    sy = by + 4
    d.text((x0, sy), src, font=fr(9), fill=GREY)
    chip(x0 + wmax - 62, sy - 1, "REPORTED", DARKBLUE)

# ---------- MORE OF THE DAY ----------
d.rectangle([0, 430, W, 448], fill=BLACK)
d.text((10, 433), "MORE OF THE DAY  \u2014  10 STORIES", font=fb(13), fill=WHITE)

cards = [
    ("AMERICAS", (30, 60, 140), "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED"),
    ("FBI", (150, 40, 40), "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED"),
    ("WHITE HOUSE", (150, 110, 0), "IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", (20, 120, 60), "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", (178, 34, 34), "SKUBAL'S $450M DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", (178, 34, 34), "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", (110, 60, 150), "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED"),
    ("TECH", (20, 90, 160), "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", (120, 60, 160), "POLAND: 3 MISSILES CROSS", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (90, 90, 90), "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", "CLAIM"),
]
CCW = W // 5
for i, (tag, tcol, head, body, src, st) in enumerate(cards):
    cx = (i % 5) * CCW
    cy = 448 + (i // 5) * 66
    d.rectangle([cx, cy, cx + CCW - 1, cy + 13], fill=tcol)
    d.text((cx + 6, cy + 1), tag, font=fb(9), fill=WHITE)
    n = str(i + 1)
    d.text((cx + CCW - 12 - d.textlength(n, font=fb(9)), cy + 1), n, font=fb(9), fill=WHITE)
    hl = wrap(head, fb(12), CCW - 12)
    hy = cy + 16
    for ln in hl[:2]:
        d.text((cx + 6, hy), ln, font=fb(12), fill=BLACK)
        hy += 14
    d.text((cx + 6, hy), body, font=fr(10), fill=BLACK)
    sy = hy + 13
    d.text((cx + 6, sy), src, font=fr(9), fill=GREY)
    chip(cx + CCW - 68, sy - 1, st, DARKBLUE if st == "REPORTED" else RED)

# ---------- map + ALSO header ----------
d.rectangle([0, 580, W, 602], fill=BLACK)
d.text((10, 584), "WHERE IT HAPPENED", font=fb(13), fill=WHITE)
d.text((340, 584), "ALSO ON MONDAY", font=fb(13), fill=WHITE)

# map box
d.rectangle([0, 602, 330, 826], outline=(150, 180, 210), width=1)
for gx in range(0, 331, 13):
    d.line([(gx, 602), (gx, 826)], fill=LBLUE, width=1)
for gy in range(602, 827, 13):
    d.line([(0, gy), (330, gy)], fill=LBLUE, width=1)
# continents (stylised blobs)
d.ellipse([18, 622, 150, 700], fill=LGREEN)      # North America
d.ellipse([60, 706, 130, 790], fill=LGREEN)      # South America
d.ellipse([196, 628, 240, 668], fill=LGREEN)     # Europe
d.ellipse([200, 672, 258, 748], fill=LGREEN)     # Africa
d.ellipse([246, 622, 326, 706], fill=LGREEN)     # Asia
d.ellipse([282, 758, 322, 792], fill=LGREEN)     # Australia
pins = [(290, 648, 1), (98, 776, 2), (272, 652, 3), (72, 692, 4), (102, 676, 5),
        (222, 672, 6), (82, 656, 7), (52, 712, 8), (68, 736, 9), (84, 764, 10),
        (204, 646, 11), (218, 656, 12), (238, 640, 13)]
for px, py, n in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    ns = str(n)
    d.text((px - d.textlength(ns, font=fb(8)) / 2, py - 5), ns, font=fb(8), fill=WHITE)
leg = ["Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing",
       "4 Washington  \u00b7  5 New York  \u00b7  6 Tehran  \u00b7  7 Chicago",
       "8 SF  \u00b7  9 Denver  \u00b7  10 Austin  \u00b7  11 Warsaw  \u00b7  12 Kyiv  \u00b7  13 Moscow"]
ly = 798
for ln in leg:
    d.text((8, ly), ln, font=fr(8), fill=BLACK)
    ly += 10

# ALSO list
also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules", "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    ax = 346 if i < 9 else 686
    ay = 612 + (i % 9) * 24
    d.text((ax, ay), item, font=fr(11), fill=BLACK)

# ---------- DATE CHECK ----------
d.rectangle([8, 826, 1016, 912], outline=RED, width=2)
d.text((14, 832), "DATE CHECK", font=fb(14), fill=RED)
d.text((1016 - 14 - d.textlength("READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=fb(9)), 836),
       "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=fb(9), fill=RED)
left = "LEFT OUT \u2014 NOT 23 NOV:  Democrats reach 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)  \u00b7  EU-Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)"
ll = wrap(left, fr(11), 990)
ly = 854
for ln in ll:
    d.text((14, ly), ln, font=fr(11), fill=BLACK)
    ly += 14
d.text((14, ly + 2), "NOT YET:  Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=fr(11), fill=BLACK)

# ---------- footer ----------
d.text((14, 920), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=fr(10), fill=GREY)
d.text((14, 934), "CHIPS: REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim, not independently confirmed  \u00b7  ONGOING = still developing",
       font=fr(10), fill=GREY)
d.text((14, 946), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=fr(9), fill=GREY)

# ---------- bottom bar ----------
d.rectangle([0, 962, W, H], fill=BLACK)
bt = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - d.textlength(bt, font=fb(18))) / 2, 982), bt, font=fb(18), fill=GOLD)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out)
print("saved", out, os.path.getsize(out), "bytes")
