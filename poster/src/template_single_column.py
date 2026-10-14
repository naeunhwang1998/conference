"""Single-column IHPBA 2026 ePoster (template layout 1), styled like the custom poster."""
import os, re, shutil, sys
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
exec(src[:src.index("S = []")])  # shared XML helpers: run, para, ph, box, cell, table, pic, e, EMU ...

U, FIG, ICONS, QR = sys.argv[1:5]
NAVY, GOLD = "213C80", "BB890B"
TXT, MUTED = "1F2937", "5B6472"
TINT = "EEF1F8"
GOOD, GOODBG, EQ, EQBG, BAD, BADBG = "2E7D4F", "E3F2E8", "5B6472", "EEF0F3", "B86410", "FCEFDD"

S = []
media = {}  # rid -> (target filename, source path)
def img(key, path):
    rid = "rIdImg" + key
    media[rid] = ("p1_" + os.path.basename(path), path)
    return rid

PX0, PX1 = 0.35, 11.83          # white panel from the slide master
L, R_ = 0.75, 11.43
W = R_ - L

# ---------- title block (template placeholders on the gold band) ----------
S.append(ph(26, "Title", 4.51, 0.38, 7.33, 1.43,
            [para(run("Clinical review of robotic distal pancreatectomy", sz=28, b=True))], anchor="b"))
sup = lambda s: run(s, sz=13, baseline="30000")
S.append(ph(27, "Authors", 4.51, 1.95, 7.33, 0.6,
            [para(run("Naeun Hwang", sz=16, b=True) + sup("1") + run(", Sam Reddish", sz=16, b=True) + sup("1") +
                  run(", Jonathan Koea", sz=16, b=True) + sup("1,2") + run(", Sanket Srinivasa", sz=16, b=True) + sup("1,2"))]))
S.append(ph(25, "Affiliations", 4.51, 2.62, 7.33, 1.1,
            [para(sup("1") + run("Upper GI Unit, Department of Surgery, Te Whatu Ora Waitematā, Auckland, New Zealand", sz=12), after=2),
             para(sup("2") + run("Department of Surgery, University of Auckland, Auckland, New Zealand", sz=12))]))

# ---------- key message + stats ----------
y = 4.62
KEY = (box("Key message", L, y, W, 0.85, [para(
    run("Robotic distal pancreatectomy (RDP) ", sz=17, b=True, color=NAVY) +
    run("matches or improves on laparoscopic surgery and outperforms open surgery, at a similar overall cost to laparoscopy.", sz=17, color=TXT))],
    anchor="ctr"))
y += 0.05
stats = [("≈1 day", "shorter hospital stay than laparoscopic", NAVY), ("0%", "positive margins (laparoscopic 2%)", NAVY),
         ("≤ LDP", "overall cost; well below open surgery", NAVY), ("+30 min", "operating time vs laparoscopic, mostly docking", GOLD)]
gap = 0.2; sw = (W - 3 * gap) / 4
for k, (big, lab, col) in enumerate(stats):
    x = L + k * (sw + gap)
    S.append(box("Stat " + big, x, y, sw, 1.2, [
        para(run(big, sz=28, b=True, color=col), algn="ctr", after=2),
        para(run(lab, sz=11.5, color=TXT), algn="ctr")],
        line=col, geom="roundRect", anchor="ctr", ins=0.08, adj=9000))
y += 1.2 + 0.3

def section(n, title, x, yy, w):
    S.append(box(f"Section {n} number", x, yy, 0.46, 0.46, [para(run(f"{n:02d}", sz=12, b=True, color="FFFFFF"), algn="ctr")],
                 fill=GOLD, geom="ellipse", anchor="ctr"))
    S.append(box(f"Section {n} title", x + 0.6, yy, w - 0.6, 0.46, [para(run(title, sz=18, b=True, color=NAVY))], anchor="ctr"))
    return yy + 0.56

HW = (W - 0.45) / 2; RX = L + HW + 0.45

# ---------- row A: background | why robotic ----------
top = y
y = section(1, "Background & aim", L, top, HW)
S.append(box("Background", L, y, HW, 1.2, [
    para(run("Distal pancreatectomy has moved from open (ODP) to laparoscopic (LDP) and robotic (RDP) surgery.", sz=12.5), bullet=True, after=4),
    para(run("LDP is limited by dexterity and visualisation.", sz=12.5), bullet=True, after=4),
    para(run("Whether RDP's technical gains improve outcomes is still debated.", sz=12.5), bullet=True)]))
y += 1.24
S.append(box("Aim", L, y, HW, 0.82, [para(run("Aim  ", sz=12.5, b=True, color=GOLD) +
    run("Compare RDP with ODP and LDP: technique, outcomes, cost and challenges.", sz=12.5))],
    fill=TINT, geom="roundRect", anchor="ctr", ins=0.12, adj=12000))
yA_left = y + 0.82

y = section(2, "Why robotic?", RX, top, HW)
adv = [("FaEye", "3D magnified", "vision"), ("FaHandDots", "Tremor", "filtration"), ("FaMaximize", "Motion", "scaling"), ("FaRobot", "Wristed", "instruments")]
aw = (HW - 0.1 * 3) / 4
for k, (ic, a, b_) in enumerate(adv):
    x = RX + k * (aw + 0.1)
    S.append(box("Advantage circle " + a, x + aw / 2 - 0.38, y + 0.05, 0.76, 0.76, None, fill=NAVY, geom="ellipse"))
    S.append(pic(img(ic, os.path.join(ICONS, ic + ".png")), "Icon " + a, a + " " + b_, x + aw / 2 - 0.21, y + 0.26, 0.42, 0.42))
    S.append(box("Advantage " + a, x - 0.05, y + 0.9, aw + 0.1, 0.55, [para(run(a, sz=11, b=True, color=NAVY), algn="ctr"),
                                                                    para(run(b_, sz=11, color=TXT), algn="ctr")]))
y += 1.5
S.append(box("Platforms note", RX, y, HW, 0.55, [para(run("Platforms: ", sz=11.5, b=True, color=NAVY) +
    run("almost all evidence is from da Vinci; Versius and hinotori™ have only early case reports.", sz=11.5, color=MUTED))]))
yA_right = y + 0.55
y = max(yA_left, yA_right) + 0.28

# ---------- 03 technique (full width) ----------
y = section(3, "Operative technique", L, y, W)
fw = 1.8; fh = fw * 1061 / 951
S.append(box("Figure frame", L, y, fw + 0.16, fh + 0.16, None, line="CFD6E4", geom="roundRect", adj=5000))
S.append(pic(img("Fig", FIG), "Figure 1", "Fig. 1 Port placement for robotic distal pancreatectomy", L + 0.08, y + 0.08, fw, fh))
S.append(box("Fig caption", L, y + fh + 0.2, fw + 0.16, 0.3, [para(run("Fig. 1 ", sz=10.5, b=True) + run("Port placement", sz=10.5, color=MUTED), algn="ctr")]))
steps = [("Position", "Supine or split legs; steep reverse Trendelenburg; dock"), ("Expose", "Enter the lesser sac"),
         ("Control", "Splenic artery and splenic vein"), ("Divide", "Pancreas with a macroscopic margin"),
         ("Resect", "En bloc retroperitoneal dissection ± spleen")]
sx0 = L + fw + 0.5; scw = (R_ - sx0 - 0.3) / 2
for k, (a, b_) in enumerate(steps):
    col, row = (0, k) if k < 3 else (1, k - 3)
    sx = sx0 + col * (scw + 0.3); sy = y + row * 0.72
    S.append(box(f"Step {k+1}", sx, sy + 0.02, 0.38, 0.38, [para(run(str(k + 1), sz=11, b=True, color="FFFFFF"), algn="ctr")], fill=NAVY, geom="ellipse", anchor="ctr"))
    S.append(box(f"Step {k+1} text", sx + 0.5, sy, scw - 0.5, 0.78, [para(run(a, sz=12, b=True, color=NAVY)), para(run(b_, sz=11.5, color=TXT))]))
S.append(box("Spleen note", sx0 + scw + 0.3, y + 2 * 0.72, scw, 0.66, [para(run("Spleen preserving: ", sz=11.5, b=True, color=NAVY) +
    run("splenic vessel preservation or Warshaw technique", sz=11.5))], fill="F7EFD9", geom="roundRect", anchor="ctr", ins=0.1, adj=12000))
y += max(fh + 0.52, 3 * 0.72) + 0.28

# ---------- 04 outcomes (full width) ----------
y = section(4, "Clinical outcomes of RDP", L, y, W)
hdr = lambda t: para(run(t, sz=12, b=True, color="FFFFFF"))
def oc(kind, sym, t):
    bg, col = {"g": (GOODBG, GOOD), "e": (EQBG, EQ), "b": (BADBG, BAD)}[kind]
    return cell([para(run(sym, sz=12, b=True, color=col) + run(t, sz=12, b=kind != "e", color=col))], bg, mar=0.08)
lab = lambda t: cell([para(run(t, sz=12, b=True, color=NAVY))], "FFFFFF", mar=0.08)
rows = [[cell([hdr("Outcome")], NAVY, mar=0.08), cell([hdr("RDP vs open")], NAVY, mar=0.08), cell([hdr("RDP vs laparoscopic")], NAVY, mar=0.08)],
        [lab("Blood loss"), oc("g", "▼ ", "Lower"), oc("g", "▼ ", "Lower (planned spleen preservation)")],
        [lab("Complications"), oc("g", "▼ ", "Fewer (fistula, respiratory, wound)"), oc("e", "= ", "Similar overall, major and fistula")],
        [lab("Hospital stay"), oc("g", "▼ ", "Shorter"), oc("g", "▼ ", "≈1 day shorter")],
        [lab("Conversion to open"), oc("e", "", "Not applicable"), oc("g", "▼ ", "Fewer")],
        [lab("Spleen preservation"), oc("g", "▲ ", "Higher"), oc("g", "▲ ", "Higher; fewer conversions to splenectomy")],
        [lab("Oncological"), oc("e", "= ", "Non-inferior R0 and lymph node yield"), oc("g", "▲ ", "0% vs 2% R1; more lymph nodes")],
        [lab("Operative time"), oc("e", "= ", "Conflicting"), oc("b", "▲ ", "≈30 min longer (docking)")]]
colw = [2.3, 3.9, W - 6.2]; rowh = [0.38] + [0.36] * 7
S.append(table("Outcomes table", L, y, colw, rowh, rows))
y += sum(rowh) + 0.1
S.append(box("Table key", L, y, W, 0.3, [para(
    run("■ ", sz=10.5, color=GOOD) + run("favours RDP     ", sz=10.5, color=MUTED) + run("■ ", sz=10.5, color=EQ) + run("no clear difference     ", sz=10.5, color=MUTED) +
    run("■ ", sz=10.5, color=BAD) + run("favours comparator", sz=10.5, color=MUTED))]))
y += 0.3 + 0.28

# ---------- row B: cost | challenges ----------
top = y
y = section(5, "Cost-effectiveness", L, top, HW)
chips = [("Operative cost", "RDP higher", BADBG, BAD), ("Overall cost", "RDP ≤ LDP < ODP", GOODBG, GOOD), ("Quality of life", "RDP > LDP", GOODBG, GOOD)]
cw3 = (HW - 0.2) / 3
for k, (a, b_, bg, col) in enumerate(chips):
    S.append(box("Cost chip " + a, L + k * (cw3 + 0.1), y, cw3, 0.85, [para(run(a, sz=10.5, color=MUTED), algn="ctr", after=1),
             para(run(b_, sz=11.5, b=True, color=col), algn="ctr")], fill=bg, geom="roundRect", anchor="ctr", ins=0.03, adj=12000))
y += 0.97
S.append(box("Cost bullets", L, y, HW, 1.05, [
    para(run("Theatre costs offset by shorter stay, fewer conversions and lower morbidity; costs fall with volume.", sz=12), bullet=True, after=3),
    para(run("More QALYs than LDP at similar cost (ROBOCOSTES).", sz=12), bullet=True)]))
yB_left = y + 1.05

y = section(6, "Challenges", RX, top, HW)
ch = [("FaClock", "Operative time", "Docking adds time; falls with the learning curve"),
      ("FaUserDoctor", "Team & training", "Dedicated robotic team; few training centres"),
      ("FaScaleUnbalanced", "Access", "High upfront cost; robots mostly in advanced economies")]
for ic, a, b_ in ch:
    S.append(box("Challenge circle " + a, RX, y + 0.04, 0.56, 0.56, None, fill=GOLD, geom="ellipse"))
    S.append(pic(img(ic, os.path.join(ICONS, ic + ".png")), escape("Icon " + a), a, RX + 0.14, y + 0.18, 0.28, 0.28))
    S.append(box("Challenge " + a, RX + 0.72, y, HW - 0.72, 0.7, [para(run(a, sz=12, b=True, color=NAVY)), para(run(b_, sz=11.5, color=TXT))]))
    y += 0.7
yB_right = y
y = max(yB_left, yB_right) + 0.2

# ---------- conclusion ----------
CH = 21.08 - y
qr = 1.12
S.append(box("Conclusion box", L - 0.15, y, W + 0.3, CH, None, fill=NAVY, geom="roundRect", adj=7000))
S.append(box("Conclusion", L + 0.15, y, W - qr - 0.6, CH, [
    para(run("CONCLUSION", sz=12, b=True, color=GOLD), after=4),
    para(run("RDP offers greater precision, better clinical outcomes and more spleen preservation than open and laparoscopic surgery, and is cost-effective. ", sz=15, b=True, color="FFFFFF") +
         run("Wider adoption depends on training and equitable access.", sz=15, color="D6DCEB"))], anchor="ctr"))
S.append(box("QR tile", R_ - qr, y + (CH - qr) / 2, qr, qr, None, fill="FFFFFF", geom="roundRect", adj=6000))
S.append(pic(img("QR", QR), "QR code", "QR code linking to the full paper, doi.org/10.1016/j.lers.2025.02.001", R_ - qr + 0.07, y + (CH - qr) / 2 + 0.07, qr - 0.14, qr - 0.14))
print(f"conclusion y={y:.2f} h={CH:.2f}")

# ---------- write slide1, drop slide2 ----------
p = os.path.join(U, "ppt/slides/slide1.xml")
x = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write(x[:x.index("<p:sp>")] + "".join(S) + x[x.index("</p:spTree>"):])
rels = os.path.join(U, "ppt/slides/_rels/slide1.xml.rels")
r = open(rels).read()
for rid, (name, path) in media.items():
    shutil.copy(path, os.path.join(U, "ppt/media", name))
    r = r.replace("</Relationships>", f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{name}"/></Relationships>')
open(rels, "w").write(r)
pp = os.path.join(U, "ppt/presentation.xml")
px = open(pp).read().replace('<p:sldId id="267" r:id="rId3"/>', '')
open(pp, "w").write(px)
