#!/usr/bin/env python3
"""LXL-DFIR-001 — all five figures, one script.

    python3 tools/make_diagrams.py            # writes ./diagrams/*.png

Design rules that are not negotiable:
  * PIL only. NEVER an image model. Every registry path, hash prefix and byte
    count here is literal text typed into this file; a generative model will
    corrupt a hex string and a corrupted hash is worse than no figure.
  * 1200 px wide. Legible on a phone, the commonest place a hiring manager
    reads anything.
  * Every figure carries the classification footer.
  * No figure carries the device serial, a password, or a ground-truth value.
"""
import os
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/dejavu/"
def B(s):  return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
def R(s):  return ImageFont.truetype(FD + "DejaVuSans.ttf", s)
def M(s):  return ImageFont.truetype(FD + "DejaVuSansMono.ttf", s)
def MB(s): return ImageFont.truetype(FD + "DejaVuSansMono-Bold.ttf", s)

BG, GRID = (13, 21, 32), (26, 38, 55)
WHITE, GREY, DIM = (240, 244, 250), (150, 166, 186), (110, 126, 146)
GREEN,  GREEN2  = (52, 211, 153), (16, 60, 48)
BLUE,   BLUE2   = (96, 165, 250), (18, 40, 70)
AMBER,  AMBER2  = (251, 191, 36), (60, 46, 12)
RED,    RED2    = (248, 113, 113), (66, 24, 24)
PURPLE, PURPLE2 = (167, 139, 250), (42, 33, 74)
PANEL, LINE = (17, 27, 40), (72, 92, 118)

FOOTER = "SIMULATED ACADEMIC CASE  \u00b7  LXL-DFIR-001"

# ── primitives ───────────────────────────────────────────────────────────────
def canvas(w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    for x in range(0, w, 40): d.line([(x, 0), (x, h)], fill=GRID)
    for y in range(0, h, 40): d.line([(0, y), (w, y)], fill=GRID)
    return img, d

def ctr(d, w, txt, y, font, fill):
    d.text(((w - d.textlength(txt, font=font)) / 2, y), txt, font=font, fill=fill)

def box(d, x0, y0, x1, y1, border, fill=PANEL, r=14, w=2):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill, outline=border, width=w)

def chip(d, x, y, txt, colour, font=None, pad=13, h=38):
    font = font or M(18)
    tw = d.textlength(txt, font=font)
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + h], radius=7,
                        fill=(9, 14, 22), outline=colour, width=2)
    d.text((x + pad, y + (h - font.size) / 2 - 1), txt, font=font, fill=colour)

def foot(d, w, h):
    ctr(d, w, FOOTER, h - 42, R(17), DIM)

# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — incident timeline
# ═════════════════════════════════════════════════════════════════════════════
def fig01(path):
    W, H = 1200, 1560
    img, d = canvas(W, H)
    ctr(d, W, "Ninety minutes, in twelve records", 56, B(40), WHITE)
    ctr(d, W, "30 October 2026  \u00b7  all times IST", 108, R(23), GREY)

    EV = [
        ("16:31:46", "Interactive logon",                   "session 0x109b61f",              BLUE),
        ("16:33:37", "USB device mounted as E:",             "first file writes 16:56",        BLUE),
        ("16:35",    "Four documents opened and closed",     "03_Confidential, 04_Restricted", BLUE),
        ("16:40:15", "Staging folder created",               "Documents\\Backup",              PURPLE),
        ("16:41:13", "Four files copied into staging",       "16:41:13 \u2192 16:42:14",       PURPLE),
        ("16:45:28", "Scheduled task fires as SYSTEM",       "result 2 \u2014 copied nothing", GREY),
        ("16:48:47", "Archive created, password-protected",  "15,058 B \u2192 8,296 B",        PURPLE),
        ("16:56:28", "Three files copied to the USB drive",  "24.2 s total, ~12 s apart",      GREEN),
        ("17:01:01", "Email sent to another company",        "424 B \u2014 no attachment",     GREEN),
        ("17:03:41", "Archive uploaded to external service", "POST /upload, 8,529 B, 200",     GREEN),
        ("17:06:37", "Staging folder deleted",              "no Recycle Bin",                 RED),
        ("17:10:35", "USB device removed",                  "capture stopped 17:12",          RED),
    ]
    y0, TX, BX, AX = 176, 300, 1104, 250
    d.line([(AX, y0 - 6), (AX, y0 + len(EV) * 106 - 40)], fill=(45, 60, 80), width=2)
    for i, (t, ev, sub, col) in enumerate(EV):
        cy = y0 + i * 106
        d.text((96, cy + 6), t, font=MB(23), fill=WHITE)
        d.ellipse([AX - 8, cy + 10, AX + 8, cy + 26], fill=col, outline=BG, width=2)
        box(d, TX, cy, BX, cy + 74, col, PANEL, r=10, w=2)
        d.text((TX + 20, cy + 14), ev, font=B(21), fill=WHITE)
        d.text((TX + 20, cy + 44), sub, font=M(15), fill=col)
    foot(d, W, H); img.save(path)

# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — four recorders, one conclusion
# ═════════════════════════════════════════════════════════════════════════════
def fig02(path):
    W, H = 1200, 1180
    img, d = canvas(W, H)
    ctr(d, W, "Four recorders. One conclusion.", 50, B(40), WHITE)
    ctr(d, W, "None of them knew the others existed.", 100, R(23), GREY)

    SRC = [
        (30,  BLUE,   "E-001  workstation", "Sysmon, event 1", "the 7z command",   "line"),
        (330, GREEN,  "E-002  USB image",   "icat, inode 17",  "archive, 8,296 B", "9c75f0db\u2026"),
        (630, AMBER,  "E-008  service log", "at receipt",      "digest 9c75f0db\u2026", "8,296 stored"),
        (930, PURPLE, "E-003  capture",     "frame 159",       "POST /upload",     "8,529 B, 200"),
    ]
    CW = 240
    for x, col, title, sub, l1, l2 in SRC:
        box(d, x, 180, x + CW, 360, col, PANEL, r=13)
        d.text((x + 14, 198), title, font=B(16), fill=col)
        d.text((x + 14, 226), sub, font=M(12), fill=GREY)
        d.line([(x + 14, 254), (x + CW - 14, 254)], fill=(40, 54, 72), width=1)
        d.text((x + 14, 276), l1, font=R(15), fill=WHITE)
        d.text((x + 14, 304), l2, font=R(15), fill=WHITE)

    for x in (150, 450, 750, 1050):
        d.line([(x, 360), (600, 470)], fill=LINE, width=2)
    d.polygon([(600, 486), (589, 468), (611, 468)], fill=GREEN)

    box(d, 110, 492, 1090, 652, GREEN, GREEN2, r=16)
    d.text((140, 514), "The archive created at 16:48:47 was", font=B(27), fill=WHITE)
    d.text((140, 552), "copied to removable media AND uploaded", font=B(27), fill=WHITE)
    d.text((140, 590), "to an external service, 15 minutes apart.", font=B(27), fill=WHITE)
    d.text((140, 626), "Both copies are byte-identical.", font=R(19), fill=GREEN)

    box(d, 110, 688, 1090, 806, (200, 200, 200), (24, 24, 28), r=14)
    d.text((140, 708), "FACT \u2014 not an inference.", font=B(28), fill=AMBER)
    d.text((140, 748), "Four independent recorders. Two of them hashed the same bytes.", font=R(19), fill=GREY)
    d.text((140, 776), "No single artefact in this case carries that finding alone.", font=R(19), fill=GREY)

    box(d, 110, 842, 1090, 958, DIM, PANEL, r=14, w=2)
    d.text((140, 862), "What these four do NOT establish", font=B(21), fill=RED)
    d.text((140, 898), "Who was at the keyboard. Why the material was taken.", font=R(18), fill=GREY)
    d.text((140, 926), "An account is not a person. A session is not an identity.", font=R(18), fill=GREY)

    foot(d, W, H); img.save(path)

# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — hash correlation
# ═════════════════════════════════════════════════════════════════════════════
def fig03(path):
    W, H = 1200, 1200
    img, d = canvas(W, H)
    ctr(d, W, "Two ways out. One file.", 70, B(44), WHITE)
    ctr(d, W, "The same 8,296 bytes, recorded at both ends.", 132, R(26), GREY)

    box(d, 70, 400, 400, 560, BLUE, BLUE2)
    d.text((96, 424), "The archive", font=B(26), fill=WHITE)
    d.text((96, 462), "created on the workstation", font=R(17), fill=GREY)
    chip(d, 96, 496, "Atlas_backup.7z", BLUE)
    d.text((96, 540), "8,296 bytes", font=R(17), fill=GREY)

    d.line([(400, 452), (520, 452), (520, 330), (640, 330)], fill=GREEN, width=3)
    d.polygon([(640, 330), (626, 323), (626, 337)], fill=GREEN)
    d.line([(400, 510), (520, 510), (520, 700), (640, 700)], fill=AMBER, width=3)
    d.polygon([(640, 700), (626, 693), (626, 707)], fill=AMBER)

    box(d, 640, 230, 1130, 430, GREEN, GREEN2)
    d.text((666, 254), "ROUTE 1 \u2014 removable media", font=B(20), fill=GREEN)
    d.text((666, 286), "read back from the USB image", font=R(17), fill=GREY)
    chip(d, 666, 322, "9c75f0db\u2026037074b", GREEN, MB(19))
    d.text((666, 372), "icat, inode 17", font=M(16), fill=GREY)
    d.text((666, 396), "on the device: 16:56", font=R(16), fill=GREY)

    box(d, 640, 600, 1130, 800, AMBER, AMBER2)
    d.text((666, 624), "ROUTE 2 \u2014 cloud upload", font=B(20), fill=AMBER)
    d.text((666, 656), "hashed by the server at receipt", font=R(17), fill=GREY)
    chip(d, 666, 692, "9c75f0db\u2026037074b", AMBER, MB(19))
    d.text((666, 742), "HTTP 200, POST /upload", font=M(16), fill=GREY)
    d.text((666, 766), "on the wire: 17:03", font=R(16), fill=GREY)

    d.text((452, 296), "copied", font=R(15), fill=GREEN)
    d.text((452, 666), "uploaded", font=R(15), fill=AMBER)

    box(d, 70, 900, 1130, 1050, (200, 200, 200), (24, 24, 28), w=2)
    d.text((100, 926), "Neither route knew about the other.", font=B(30), fill=WHITE)
    d.text((100, 972), "Same bytes. Same hash. Recorded by two systems that never spoke.", font=R(22), fill=GREY)
    d.text((100, 1006), "That is arithmetic, not an inference.", font=B(22), fill=AMBER)

    foot(d, W, H); img.save(path)

# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 4 / 5 — USBSTOR and UAS binding (square and wide)
# ═════════════════════════════════════════════════════════════════════════════
def _usbstor_square(path):
    W = H = 1200
    img, d = canvas(W, H)
    ctr(d, W, "One USB drive. Two places Windows can record it.", 112, B(36), WHITE)
    ctr(d, W, "Only one of them exists on this machine.", 170, R(24), GREY)

    # device
    box(d, 80, 470, 240, 600, BLUE, BLUE2)
    d.text((118, 512), "USB", font=B(24), fill=BLUE)
    d.rectangle([60, 520, 80, 550], fill=(70, 88, 112))
    d.text((80, 624), "USB 3 pen drive", font=B(20), fill=WHITE)
    d.text((80, 654), "UAS-capable", font=R(16), fill=GREY)
    d.text((80, 678), "device attached", font=R(16), fill=GREY)

    # arrow to windows
    d.line([(250, 535), (330, 535)], fill=WHITE, width=3)
    d.polygon([(348, 535), (332, 527), (332, 543)], fill=WHITE)

    box(d, 360, 470, 530, 620, BLUE, BLUE2)
    d.text((372, 500), "Windows 11", font=B(22), fill=WHITE)
    d.text((372, 534), "guest", font=R(17), fill=GREY)
    d.text((372, 560), "driver binds", font=R(17), fill=GREY)

    # green path
    d.line([(530, 500), (600, 500), (600, 330), (680, 330)], fill=GREEN, width=3)
    d.polygon([(680, 330), (664, 322), (664, 338)], fill=GREEN)

    box(d, 680, 210, 1140, 470, GREEN, GREEN2)
    d.text((706, 234), "USB Attached SCSI (UAS)", font=B(21), fill=GREEN)
    d.text((706, 266), "bound to UASPStor \u00b7 SCSI class driver", font=R(16), fill=GREY)
    d.text((706, 290), "the faster protocol \u2014 the path taken here", font=R(16), fill=GREY)
    chip(d, 706, 322, "Enum\\USB", GREEN, M(18), pad=11, h=34)
    chip(d, 706, 368, "Enum\\SCSI", GREEN, M(18), pad=11, h=34)
    d.text((706, 416), "manufacturer, model and full serial", font=R(16), fill=GREEN)
    d.text((706, 440), "number all still present", font=R(16), fill=GREEN)

    # red path, dashed and orthogonal
    d.line([(530, 610), (600, 610)], fill=RED, width=3)
    y = 610
    while y < 690:
        d.line([(600, y), (600, min(y + 12, 690))], fill=RED, width=3)
        y += 22
    x = 600
    while x < 668:
        d.line([(x, 690), (min(x + 12, 668), 690)], fill=RED, width=3)
        x += 22
    d.polygon([(682, 690), (666, 682), (666, 698)], fill=RED)

    box(d, 680, 590, 1140, 830, RED, RED2)
    d.text((706, 614), "Bulk-Only Transport", font=B(21), fill=RED)
    d.text((706, 646), "usbstor.sys never bound this device", font=R(16), fill=GREY)
    d.text((706, 670), "the older path \u2014 not used here", font=R(16), fill=GREY)
    chip(d, 706, 702, "Enum\\USBSTOR", RED, M(18), pad=11, h=34)
    d.text((706, 752), "not an empty key \u2014 the key does not exist", font=R(16), fill=RED)
    d.text((706, 780), "so the device never appears there", font=R(16), fill=RED)

    box(d, 80, 900, 1140, 1040, AMBER, AMBER2)
    d.text((110, 922), "Searching Enum\\USBSTOR alone returns:", font=B(21), fill=AMBER)
    d.text((110, 960), "\u201cno USB storage device was ever connected to this machine.\u201d", font=R(20), fill=GREY)
    d.text((110, 998), "The device was there. The search term was wrong.", font=B(21), fill=WHITE)

    foot(d, W, H); img.save(path)

def _usbstor_wide(path):
    W, H = 1200, 675
    img, d = canvas(W, H)
    ctr(d, W, "One USB drive. Two places Windows can record it.", 40, B(30), WHITE)
    ctr(d, W, "Only one of them exists on this machine.", 82, R(19), GREY)

    box(d, 40, 200, 150, 290, BLUE, BLUE2, r=11)
    d.text((68, 232), "USB", font=B(18), fill=BLUE)
    d.text((40, 306), "UAS-capable", font=R(14), fill=GREY)
    d.rectangle([26, 232, 40, 258], fill=(70, 88, 112))

    d.line([(156, 245), (206, 245)], fill=WHITE, width=2)
    d.polygon([(220, 245), (207, 239), (207, 251)], fill=WHITE)
    box(d, 224, 200, 336, 292, BLUE, BLUE2, r=11)
    d.text((236, 226), "Windows 11", font=B(16), fill=WHITE)
    d.text((236, 254), "driver binds", font=R(14), fill=GREY)

    d.line([(336, 220), (390, 220), (390, 150), (440, 150)], fill=GREEN, width=2)
    d.polygon([(440, 150), (427, 144), (427, 156)], fill=GREEN)
    box(d, 444, 76, 1160, 236, GREEN, GREEN2, r=12)
    d.text((462, 92), "USB Attached SCSI (UAS)", font=B(17), fill=GREEN)
    d.text((462, 118), "SCSI class driver \u2014 the path taken here", font=R(14), fill=GREY)
    chip(d, 462, 142, "Enum\\USB", GREEN, M(15), pad=9, h=28)
    chip(d, 462, 178, "Enum\\SCSI", GREEN, M(15), pad=9, h=28)
    d.text((600, 148), "manufacturer, model and", font=R(14), fill=GREEN)
    d.text((600, 168), "full serial present", font=R(14), fill=GREEN)

    d.line([(336, 272), (388, 272)], fill=RED, width=2)
    x = 388
    while x < 440:
        d.line([(x, 272), (min(x + 10, 440), 272)], fill=RED, width=2); x += 18
    d.polygon([(440, 272), (427, 266), (427, 278)], fill=RED)
    box(d, 444, 300, 1160, 452, RED, RED2, r=12)
    d.text((462, 316), "Bulk-Only Transport", font=B(17), fill=RED)
    d.text((462, 342), "usbstor.sys never bound this device", font=R(14), fill=GREY)
    chip(d, 462, 366, "Enum\\USBSTOR", RED, M(15), pad=9, h=28)
    d.text((610, 372), "the key does not exist \u2014 not empty", font=R(14), fill=RED)

    box(d, 40, 500, 1160, 600, AMBER, AMBER2, r=12)
    d.text((62, 516), "Searching Enum\\USBSTOR alone returns a clean, confident zero.", font=B(17), fill=AMBER)
    d.text((62, 550), "The device was there. The search term was wrong.", font=R(16), fill=WHITE)

    foot(d, W, H); img.save(path)

FIGURES = [
    ("01_incident_timeline.png",  fig01),
    ("02_four_recorders.png",     fig02),
    ("03_hash_correlation.png",   fig03),
    ("04_usbstor_uas_binding.png", _usbstor_square),
    ("05_usbstor_uas_wide.png",   _usbstor_wide),
]

def main(outdir="diagrams"):
    os.makedirs(outdir, exist_ok=True)
    for name, fn in FIGURES:
        p = os.path.join(outdir, name)
        fn(p)
        print(f"  {p}")

if __name__ == "__main__":
    print("building 5 figures:")
    main()
