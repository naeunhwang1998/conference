"""Build the IHPBA 2026 ePoster (double-column layout) from the unpacked template."""
import os, re, shutil, sys
from xml.sax.saxutils import escape

U = sys.argv[1]          # unpacked template dir
FIG = sys.argv[2]        # port placement image
EMU = 914400
NAVY, DNAVY, GOLD = "213C80", "002060", "BB890B"
GREEN, AMBER, GREY = "1E7B3C", "B45309", "5B6170"
TINT, GOLDTINT = "EEF1F8", "F7EFD9"

_id = [100]
def nid():
    _id[0] += 1
    return _id[0]

def e(v):
    return int(round(v * EMU))

def xfrm(x, y, w, h):
    return f'<a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>'

def run(text, sz=None, b=False, i=False, color=None, baseline=None):
    a = ' lang="en-US"'
    if sz: a += f' sz="{int(sz*100)}"'
    if b: a += ' b="1"'
    if i: a += ' i="1"'
    if baseline: a += f' baseline="{baseline}"'
    fill = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>' if color else ''
    sp = ' xml:space="preserve"' if text != text.strip() else ''
    return f'<a:r><a:rPr{a} dirty="0">{fill}</a:rPr><a:t{sp}>{escape(text)}</a:t></a:r>'

def para(runs, bullet=False, algn=None, after=0, before=0, lvl=0, bucolor=NAVY):
    p = ''
    if algn: p += f' algn="{algn}"'
    inner = ''
    if before: inner += f'<a:spcBef><a:spcPts val="{int(before*100)}"/></a:spcBef>'
    else: inner += '<a:spcBef><a:spcPts val="0"/></a:spcBef>'
    inner += f'<a:spcAft><a:spcPts val="{int(after*100)}"/></a:spcAft>'
    if bullet:
        ind = 0.17 + 0.17 * lvl
        p += f' marL="{e(ind)}" indent="{-e(0.17)}"'
        inner += f'<a:buClr><a:srgbClr val="{bucolor}"/></a:buClr><a:buFont typeface="Arial"/><a:buChar char="{"•" if lvl == 0 else "–"}"/>'
    else:
        p += ' marL="0" indent="0"'
        inner += '<a:buNone/>'
    return f'<a:p><a:pPr{p}>{inner}</a:pPr>{runs}</a:p>'

def body(paras, anchor="t", ins=0.0, autofit=False):
    fit = '<a:normAutofit/>' if autofit else '<a:noAutofit/>'
    i = e(ins)
    return (f'<p:txBody><a:bodyPr wrap="square" lIns="{i}" tIns="{i}" rIns="{i}" bIns="{i}" anchor="{anchor}">{fit}</a:bodyPr>'
            f'<a:lstStyle/>{"".join(paras)}</p:txBody>')

def ph(idx, name, x, y, w, h, paras, anchor="t"):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{nid()}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph type="body" sz="quarter" idx="{idx}"/></p:nvPr></p:nvSpPr>'
            f'<p:spPr>{xfrm(x,y,w,h)}</p:spPr>'
            f'<p:txBody><a:bodyPr anchor="{anchor}"><a:noAutofit/></a:bodyPr><a:lstStyle/>{"".join(paras)}</p:txBody></p:sp>')

def box(name, x, y, w, h, paras=None, fill=None, line=None, geom="rect", anchor="t", ins=0.0, adj=None):
    f = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    l = f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else '<a:ln><a:noFill/></a:ln>'
    av = f'<a:avLst><a:gd name="adj" fmla="val {adj}"/></a:avLst>' if adj is not None else '<a:avLst/>'
    tx = body(paras or [para(run(""))], anchor=anchor, ins=ins)
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{nid()}" name="{escape(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="{geom}">{av}</a:prstGeom>{f}{l}</p:spPr>{tx}</p:sp>')

def header(idx, x, y, w, text):
    return ph(idx, f"Section Title {idx}", x, y, w, 0.42, [para(run(text.upper()), algn="ctr")], anchor="ctr")

def cell(paras, fill=None, anchor="ctr", mar=0.05):
    f = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    m = e(mar)
    bd = ''.join(f'<a:{t} w="6350"><a:solidFill><a:srgbClr val="D5DAE6"/></a:solidFill></a:{t}>' for t in ('lnL', 'lnR', 'lnT', 'lnB'))
    return (f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/>{"".join(paras)}</a:txBody>'
            f'<a:tcPr marL="{m}" marR="{m}" marT="{e(0.03)}" marB="{e(0.03)}" anchor="{anchor}">{bd}{f}</a:tcPr></a:tc>')

def table(name, x, y, colw, rowh, rows):
    grid = ''.join(f'<a:gridCol w="{e(c)}"/>' for c in colw)
    trs = ''
    for r, h in zip(rows, rowh):
        trs += f'<a:tr h="{e(h)}">{"".join(r)}</a:tr>'
    return (f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{nid()}" name="{name}"/>'
            f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
            f'<p:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(sum(colw))}" cy="{e(sum(rowh))}"/></p:xfrm>'
            f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
            f'<a:tbl><a:tblPr firstRow="1" bandRow="1"/><a:tblGrid>{grid}</a:tblGrid>{trs}</a:tbl></a:graphicData></a:graphic></p:graphicFrame>')

def pic(rid, name, descr, x, y, w, h):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{nid()}" name="{name}" descr="{escape(descr)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr>{xfrm(x,y,w,h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')

S = []   # shapes
LX, RX, CW = 0.58, 6.51, 5.12
BODY = 13.5  # pt

# ---------- Title block (on gold band) ----------
S.append(ph(26, "Title", 4.55, 0.38, 7.33, 1.43,
            [para(run("Clinical review of robotic distal pancreatectomy", sz=26, b=True))], anchor="b"))
sup = lambda s: run(s, sz=13, baseline="30000")
S.append(ph(27, "Authors", 4.55, 1.90, 7.33, 0.62,
            [para(run("Naeun Hwang", sz=16) + sup("1") + run(", Sam Reddish", sz=16) + sup("1") +
                  run(", Jonathan Koea", sz=16) + sup("1,2") + run(", Sanket Srinivasa", sz=16) + sup("1,2"))]))
S.append(ph(25, "Affiliations", 4.55, 2.62, 7.33, 1.20,
            [para(sup("1") + run("Upper GI Unit, Department of Surgery, Te Whatu Ora Waitematā, Auckland, New Zealand", sz=12), after=2),
             para(sup("2") + run("Department of Surgery, University of Auckland, Auckland, New Zealand", sz=12))]))

# ---------- LEFT COLUMN ----------
y = 4.62
S.append(header(28, LX, y, CW, "Background"))
y += 0.50
bg = [
    para(run("Distal pancreatectomy has shifted from open (ODP) to minimally invasive surgery: laparoscopic (LDP, since 1994) and robotic (RDP).", sz=BODY), bullet=True, after=5),
    para(run("LDP is established but limited by ", sz=BODY) + run("dexterity and visualisation", sz=BODY, b=True) + run(".", sz=BODY), bullet=True, after=5),
    para(run("RDP addresses these limits, yet whether it improves outcomes over LDP remains unsettled.", sz=BODY), bullet=True, after=0),
]
S.append(ph(29, "Background Text", LX, y, CW, 2.0, bg))
y += 2.05
S.append(box("Aim", LX, y, CW, 1.1, [
    para(run("AIM  ", sz=BODY, b=True, color=NAVY) +
         run("A clinical review comparing RDP with ODP and LDP: technique, clinical outcomes, cost-effectiveness and challenges.", sz=BODY))],
    fill=TINT, geom="roundRect", anchor="ctr", ins=0.12, adj=12000))
y += 1.45

S.append(box("Section Title Advantages", LX, y, CW, 0.42, [para(run("WHY ROBOTIC?", sz=15.48, b=True, color=NAVY), algn="ctr")], anchor="ctr"))
y += 0.52
adv = [("3D", "magnified\nvisualisation"), ("Tremor", "filtration"), ("Motion", "scaling"), ("Wristed", "articulating\ninstruments")]
aw = (CW - 3 * 0.15) / 4
for k, (a, b_) in enumerate(adv):
    ps = [para(run(a, sz=16, b=True, color=NAVY), algn="ctr", after=1)] + [para(run(t, sz=11.5, color=GREY), algn="ctr") for t in b_.split("\n")]
    S.append(box("Advantage " + a, LX + k * (aw + 0.15), y, aw, 1.15, ps, fill=TINT, geom="roundRect", anchor="ctr", ins=0.04, adj=14000))
y += 1.15 + 0.12
S.append(box("Platforms note", LX, y, CW, 0.65, [para(
    run("Platforms: ", sz=12, b=True, color=NAVY) +
    run("almost all evidence is from da Vinci; Versius and hinotori™ have only early case reports, and none yet for Hugo.", sz=12, color=GREY))]))
y += 0.65 + 0.4
S.append(header(32, LX, y, CW, "Operative Technique"))
y += 0.52
fw = 2.35; fh = fw * 1061 / 951
S.append(pic("rIdFig", "Figure 1", "Port placement for robotic distal pancreatectomy", LX, y, fw, fh))
S.append(box("Fig caption", LX, y + fh + 0.04, fw, 0.75, [
    para(run("Fig. 1 ", sz=11, b=True) + run("Port placement: 8 mm robotic arms, 12 mm camera, 5 and 12 mm assistant ports", sz=11, color=GREY), algn="ctr")]))
steps = [
    ("Position", "Supine or split legs; steep reverse Trendelenburg, then dock"),
    ("Expose", "Enter the lesser sac to expose the pancreas"),
    ("Control", "Splenic artery and splenic vein"),
    ("Divide", "Pancreas with a macroscopic margin"),
    ("Resect", "En bloc retroperitoneal dissection ± spleen"),
]
tx = LX + fw + 0.18; tw = CW - fw - 0.18
sp_paras = []
for k, (a, b_) in enumerate(steps):
    sp_paras.append(para(run(f"{k+1}  ", sz=12.5, b=True, color=GOLD) + run(a + "  ", sz=12.5, b=True, color=NAVY) + run(b_, sz=12.5), after=7))
S.append(ph(33, "Technique Steps", tx, y, tw, 3.0, sp_paras))
S.append(box("Spleen preserving", tx, y + 3.08, tw, 0.82, [
    para(run("Spleen-preserving options: ", sz=12, b=True, color=NAVY) + run("splenic vessel preservation or Warshaw technique", sz=12))],
    fill=GOLDTINT, geom="roundRect", anchor="ctr", ins=0.08, adj=14000))
y += max(fh + 0.8, 3.9) + 0.4

hdr = lambda t: para(run(t, sz=12, b=True, color="FFFFFF"))
c = lambda t, **k: para(run(t, sz=11.5, **k))
S.append(header(40, LX, y, CW, "Challenges"))
y += 0.52
chal = [
    ("Operative time", "≈30 min longer than LDP in meta-analysis, largely robot docking; shortens along the learning curve."),
    ("Team & training", "Needs a console surgeon, skilled bedside assistant and robot-trained scrub nurse; few training centres."),
    ("Cost & access", "High upfront cost; robots concentrated in advanced economies, creating inequity of access."),
]
for t, d in chal:
    S.append(box("Challenge icon", LX, y + 0.05, 0.42, 0.42, [para(run("!", sz=16, b=True, color="FFFFFF"), algn="ctr")],
                 fill=GOLD, geom="ellipse", anchor="ctr"))
    S.append(box("Challenge " + t, LX + 0.58, y, CW - 0.58, 1.05, [
        para(run(t, sz=BODY, b=True, color=NAVY), after=1), para(run(d, sz=12.5))]))
    y += 1.12
LEFT_END = y

# ---------- RIGHT COLUMN ----------
y = 4.62
S.append(header(30, RX, y, CW, "Clinical Outcomes of RDP"))
y += 0.50
UP, DN, EQ = "▲", "▼", "="
def oc(sym, txt, col):
    return cell([para(run(sym + " ", sz=11.5, b=True, color=col) + run(txt, sz=11.5, color=col if col != GREY else None), algn="l")])
G, A, N = GREEN, AMBER, GREY
orows = [
    [cell([hdr("Outcome")], NAVY), cell([hdr("RDP vs ODP")], NAVY), cell([hdr("RDP vs LDP")], NAVY)],
    [cell([c("Blood loss", b=True)]), oc(DN, "Lower", G), oc(DN, "Lower (planned SP)", G)],
    [cell([c("Complications", b=True)]), oc(DN, "Fewer (fistula, respiratory, wound)", G), oc(EQ, "Similar overall, major & fistula", N)],
    [cell([c("Hospital stay", b=True)]), oc(DN, "Shorter", G), oc(DN, "≈1 day shorter", G)],
    [cell([c("Conversion to open", b=True)]), cell([c("n/a", color=GREY)]), oc(DN, "Lower", G)],
    [cell([c("Spleen preservation", b=True)]), oc(UP, "Higher", G), oc(UP, "Higher; fewer conversions to splenectomy", G)],
    [cell([c("Oncological", b=True)]), oc(EQ, "Non-inferior R0 and LN yield (MIDP)", N), oc(UP, "0% vs 2% R1; more lymph nodes", G)],
    [cell([c("Operative time", b=True)]), oc(EQ, "Conflicting", N), oc(UP, "≈30 min longer (docking)", A)],
]
ocolw = [1.42, 1.74, 1.96]
orowh = [0.42, 0.46, 0.66, 0.46, 0.46, 0.66, 0.66, 0.46]
# zebra
for k in range(2, len(orows), 2):
    orows[k] = [x.replace('<a:noFill/></a:tcPr>', f'<a:solidFill><a:srgbClr val="{TINT}"/></a:solidFill></a:tcPr>') for x in orows[k]]
S.append(table("Outcomes table", RX, y, ocolw, orowh, orows))
y += sum(orowh) + 0.08
S.append(box("Legend", RX, y, CW, 0.30, [para(
    run("Green ", sz=9.5, b=True, color=GREEN) + run("favours RDP   ", sz=9.5, color=GREY) +
    run("Grey ", sz=9.5, b=True, color=GREY) + run("no clear difference   ", sz=9.5, color=GREY) +
    run("Amber ", sz=9.5, b=True, color=AMBER) + run("favours comparator.  SP, spleen preservation; MIDP, minimally invasive DP", sz=9.5, color=GREY))]))
y += 0.42

# key numbers
stats = [("1 day", "shorter stay\nvs LDP"), ("0%", "positive margins\n(LDP 2%)"), ("+30 min", "operative time\nvs LDP")]
sw = (CW - 2 * 0.15) / 3
for k, (big, small) in enumerate(stats):
    sx = RX + k * (sw + 0.15)
    lines = small.split("\n")
    S.append(box("Stat " + big, sx, y, sw, 1.5, [
        para(run(big, sz=25, b=True, color="FFFFFF" if k < 2 else NAVY), algn="ctr", after=2),
        para(run(lines[0], sz=11.5, color="FFFFFF" if k < 2 else NAVY), algn="ctr"),
        para(run(lines[1], sz=11.5, color="FFFFFF" if k < 2 else NAVY), algn="ctr")],
        fill=NAVY if k < 2 else GOLDTINT, geom="roundRect", anchor="ctr", ins=0.06, adj=10000))
y += 1.5 + 0.45

S.append(header(34, RX, y, CW, "Cost-effectiveness"))
y += 0.52
chips = [("Operative cost", "RDP > LDP, ODP"), ("Overall cost", "RDP ≤ LDP < ODP"), ("QALYs", "RDP > LDP")]
for k, (a, b_) in enumerate(chips):
    sx = RX + k * (sw + 0.15)
    S.append(box("Cost chip " + a, sx, y, sw, 0.92, [
        para(run(a, sz=11, color=GREY), algn="ctr", after=1),
        para(run(b_, sz=12, b=True, color=NAVY), algn="ctr")],
        line=NAVY, geom="roundRect", anchor="ctr", ins=0.04, adj=14000))
y += 1.06
cost = [
    para(run("Higher instrument and platform costs are ", sz=BODY) + run("offset by shorter stay, fewer conversions and lower morbidity", sz=BODY, b=True) + run(".", sz=BODY), bullet=True, after=5),
    para(run("Costs fall with case volume (learning curve, robot-specific instruments).", sz=BODY), bullet=True, after=5),
    para(run("Higher QALYs than LDP at similar cost, within the European acceptability threshold; supported by the multicentre ROBOCOSTES trial.", sz=BODY), bullet=True),
]
S.append(ph(35, "Cost Text", RX, y, CW, 2.45, cost))
y += 2.55

S.append(header(38, RX, y, CW, "Conclusion"))
y += 0.52
S.append(box("Conclusion box", RX, y, CW, 2.45, [
    para(run("RDP is a safe, cost-effective advance in distal pancreatectomy, offering greater precision, better clinical outcomes and higher spleen preservation than open and laparoscopic approaches.", sz=14, b=True, color="FFFFFF"), after=8),
    para(run("Wider adoption depends on expanding training, dedicated robotic teams and equitable access.", sz=13.5, color="FFFFFF"))],
    fill=NAVY, geom="roundRect", anchor="ctr", ins=0.18, adj=8000))
y += 2.45 + 0.2
S.append(ph(39, "Reference", RX, y, CW, 0.62, [
    para(run("Hwang N, Reddish S, Koea J, Srinivasa S. Clinical review of robotic distal pancreatectomy. ", sz=9, color=GREY) +
         run("Laparoscopic, Endoscopic and Robotic Surgery", sz=9, i=True, color=GREY) +
         run(" 2025;8:80–83. doi:10.1016/j.lers.2025.02.001", sz=9, color=GREY))]))
RIGHT_END = y + 0.62
print("left end", round(LEFT_END, 2), "right end", round(RIGHT_END, 2), "(panel bottom 21.24)")

# ---------- write slide ----------
src = open(os.path.join(U, "ppt/slides/slide2.xml"), encoding="utf-8").read()
head = src[:src.index("<p:sp>")]
tail = src[src.index("</p:spTree>"):]
open(os.path.join(U, "ppt/slides/slide2.xml"), "w", encoding="utf-8").write(head + "".join(S) + tail)

rels = os.path.join(U, "ppt/slides/_rels/slide2.xml.rels")
r = open(rels).read()
if "rIdFig" not in r:
    r = r.replace("</Relationships>", '<Relationship Id="rIdFig" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/fig1_ports.png"/></Relationships>')
    open(rels, "w").write(r)
shutil.copy(FIG, os.path.join(U, "ppt/media/fig1_ports.png"))

# drop the single-column slide (slide1) from the deck
p = os.path.join(U, "ppt/presentation.xml")
x = open(p).read()
x = x.replace('<p:sldId id="266" r:id="rId2"/>', '')
open(p, "w").write(x)
