// Custom ePoster (IHPBA 2026 size: 31.41 x 55.85 cm) for "Clinical review of robotic distal pancreatectomy"
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa6");
const fs = require("fs");
const { applyTheme } = require(process.env.SKILL + "/scripts/apply_theme.js");

const W = 12.205, H = 21.653, M = 0.55;
const THEME = {
  name: "RDP Poster",
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  colors: {
    dk1: "1D2A2E", lt1: "FFFFFF", dk2: "0C3B43", lt2: "E8F2F1",
    accent1: "13707A", accent2: "D63A47", accent3: "B8892B", accent4: "2E8B57",
    accent5: "C9781A", accent6: "6B7A7D", hlink: "13707A", folHlink: "0C3B43",
  },
};
const K = THEME.colors;
const INK = K.dk2, TEAL = K.accent1, RED = K.accent2, GOLD = K.accent3, TINT = K.lt2, TXT = K.dk1, MUTED = "5B6A6D";
const GOOD = "2E7D4F", GOODBG = "E3F2E8", EQ = "5B6A6D", EQBG = "EEF1F2", BAD = "B86410", BADBG = "FCEFDD";

async function icon(Comp, color, px = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: "#" + color, size: px }));
  const buf = await sharp(Buffer.from(svg)).resize(px, px).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const pres = new pptxgen();
  pres.defineLayout({ name: "EPOSTER", width: W, height: H });
  pres.layout = "EPOSTER";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = "Clinical review of robotic distal pancreatectomy";
  pres.author = "Naeun Hwang";
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  const T = (text, o) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, color: TXT, fontFace: "Arial", valign: "top" }, o));

  // ---------------- HEADER ----------------
  const HH = 3.55;
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: HH, fill: { color: INK }, line: { type: "none" }, objectName: "Header band" });
  // logo tile
  const lw = 3.55, lh = lw * 277 / 600;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: W - M - lw - 0.3, y: 0.5, w: lw + 0.3, h: lh + 0.3, rectRadius: 0.12, fill: { color: "FFFFFF" }, line: { type: "none" }, objectName: "Logo tile" });
  s.addImage({ path: "logo.png", x: W - M - lw - 0.15, y: 0.65, w: lw, h: lh, altText: "IHPBA 2026 Singapore logo", objectName: "IHPBA 2026 logo" });
  T("Clinical review of robotic distal pancreatectomy", { x: M, y: 0.5, w: 7.15, h: 1.72, fontSize: 36, bold: true, color: "FFFFFF", valign: "middle", objectName: "Title" });
  const sup = (t) => ({ text: t, options: { superscript: true } });
  const nm = (t) => ({ text: t, options: {} });
  T([nm("Naeun Hwang"), sup("1"), nm(",  Sam Reddish"), sup("1"), nm(",  Jonathan Koea"), sup("1,2"), nm(",  Sanket Srinivasa"), sup("1,2")],
    { x: M, y: 2.4, w: W - 2 * M, h: 0.42, fontSize: 17, bold: true, color: "FFFFFF", objectName: "Authors" });
  T([sup("1"), { text: "Upper GI Unit, Department of Surgery, Te Whatu Ora Waitematā, Auckland, New Zealand", options: { breakLine: true } },
     sup("2"), { text: "Department of Surgery, University of Auckland, Auckland, New Zealand", options: {} }],
    { x: M, y: 2.85, w: W - 2 * M, h: 0.5, fontSize: 11.5, color: "C9DCDD", objectName: "Affiliations" });

  // ---------------- KEY MESSAGE + STATS ----------------
  let y = HH + 0.3;
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: HH, w: W, h: 3.3, fill: { color: TINT }, line: { type: "none" }, objectName: "Key message band" });
  T([{ text: "Robotic distal pancreatectomy (RDP) ", options: { bold: true, color: INK } },
     { text: "matches or improves on laparoscopic surgery and outperforms open surgery, at a similar overall cost to laparoscopy.", options: { color: TXT } }],
    { x: M, y, w: W - 2 * M, h: 0.9, fontSize: 19, valign: "middle", objectName: "Key message" });
  y += 1.0;
  const stats = [
    ["≈1 day", "shorter hospital stay than laparoscopic", TEAL],
    ["0%", "positive margins (laparoscopic 2%)", TEAL],
    ["≤ LDP", "overall cost; well below open surgery", TEAL],
    ["+30 min", "operating time vs laparoscopic, mostly docking", GOLD],
  ];
  const gap = 0.22, sw = (W - 2 * M - 3 * gap) / 4;
  stats.forEach(([big, lab, col], i) => {
    const x = M + i * (sw + gap);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: sw, h: 1.6, rectRadius: 0.1, fill: { color: "FFFFFF" }, line: { color: col, width: 1.5 }, objectName: "Stat " + big });
    T(big.replace(" ", " "), { x: x + 0.1, y: y + 0.12, w: sw - 0.2, h: 0.7, fontSize: 30, bold: true, color: col, align: "center", valign: "middle" });
    T(lab, { x: x + 0.15, y: y + 0.85, w: sw - 0.3, h: 0.66, fontSize: 12, color: TXT, align: "center", valign: "top" });
  });

  // ---------------- SECTION HELPER ----------------
  const CW = (W - 2 * M - 0.45) / 2, LX = M, RX = M + CW + 0.45;
  const section = (n, title, x, yy) => {
    s.addShape(pres.shapes.OVAL, { x, y: yy, w: 0.5, h: 0.5, fill: { color: RED }, line: { type: "none" }, objectName: "Section number " + n });
    T(String(n).padStart(2, "0"), { x, y: yy, w: 0.5, h: 0.5, fontSize: 13, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(title, { x: x + 0.65, y: yy, w: CW - 0.65, h: 0.5, fontSize: 20, bold: true, color: INK, valign: "middle", objectName: "Section title " + title });
    return yy + 0.72;
  };
  const bullets = (items, o) => T(items.map((it, i) => ({
    text: it.text ?? it, options: Object.assign({ bullet: { indent: 16 }, breakLine: i < items.length - 1, paraSpaceAfter: 6 }, it.options || {}) })), o);

  // ---------------- LEFT COLUMN ----------------
  const top = HH + 3.3 + 0.42;
  y = section(1, "Background & aim", LX, top);
  bullets([
    "Distal pancreatectomy has moved from open (ODP) to minimally invasive surgery: laparoscopic (LDP) and robotic (RDP).",
    "LDP is established but limited by dexterity and visualisation.",
    "Whether RDP's technical gains translate into better outcomes is still debated.",
  ], { x: LX, y, w: CW, h: 1.6, fontSize: 13.5, objectName: "Background bullets" });
  y += 1.62;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LX, y, w: CW, h: 1.0, rectRadius: 0.08, fill: { color: TINT }, line: { type: "none" }, objectName: "Aim box" });
  T([{ text: "Aim  ", options: { bold: true, color: RED } }, { text: "Compare RDP with ODP and LDP: technique, outcomes, cost-effectiveness and challenges.", options: {} }],
    { x: LX + 0.2, y, w: CW - 0.4, h: 1.0, fontSize: 13.5, valign: "middle", objectName: "Aim" });
  y += 1.0 + 0.42;

  y = section(2, "Why robotic?", LX, y);
  const adv = [[fa.FaEye, "3D magnified", "visualisation"], [fa.FaHandDots, "Tremor", "filtration"], [fa.FaMaximize, "Motion", "scaling"], [fa.FaRobot, "Wristed", "instruments"]];
  const aw = (CW - 0.15 * 3) / 4;
  for (let i = 0; i < adv.length; i++) {
    const [C, a, b] = adv[i];
    const x = LX + i * (aw + 0.15);
    s.addShape(pres.shapes.OVAL, { x: x + aw / 2 - 0.42, y, w: 0.84, h: 0.84, fill: { color: TEAL }, line: { type: "none" }, objectName: "Advantage icon bg " + a });
    s.addImage({ data: await icon(C, "FFFFFF"), x: x + aw / 2 - 0.24, y: y + 0.18, w: 0.48, h: 0.48, altText: a + " " + b });
    T([{ text: a, options: { bold: true, breakLine: true } }, { text: b, options: {} }], { x, y: y + 0.95, w: aw, h: 0.6, fontSize: 11.5, align: "center", color: INK });
  }
  y += 1.6;
  T([{ text: "Platforms: ", options: { bold: true, color: INK } }, { text: "almost all evidence is from da Vinci; Versius and hinotori™ have only early case reports.", options: { color: MUTED } }],
    { x: LX, y, w: CW, h: 0.55, fontSize: 11.5, objectName: "Platforms note" });
  y += 0.55 + 0.35;

  y = section(3, "Operative technique", LX, y);
  const fw = 2.35, fh = fw * 1061 / 951;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: LX, y, w: fw + 0.2, h: fh + 0.2, rectRadius: 0.08, fill: { color: "FFFFFF" }, line: { color: "CFDCDD", width: 1 }, objectName: "Figure frame" });
  s.addImage({ path: "fig1.png", x: LX + 0.1, y: y + 0.1, w: fw, h: fh, altText: "Fig. 1 Port placement for robotic distal pancreatectomy", objectName: "Figure 1" });
  T([{ text: "Fig. 1 ", options: { bold: true, color: TXT } }, { text: "Port placement", options: {} }],
    { x: LX, y: y + fh + 0.28, w: fw + 0.2, h: 0.3, fontSize: 11, color: MUTED, align: "center" });
  const steps = [["Position", "Supine; reverse Trendelenburg; dock"], ["Expose", "Enter the lesser sac"],
    ["Control", "Splenic artery and vein"], ["Divide", "Pancreas, clear margin"], ["Resect", "En bloc ± spleen"]];
  const sx = LX + fw + 0.45, sw2 = CW - fw - 0.45;
  let sy = y;
  steps.forEach(([a, b], i) => {
    s.addShape(pres.shapes.OVAL, { x: sx, y: sy + 0.02, w: 0.36, h: 0.36, fill: { color: INK }, line: { type: "none" }, objectName: "Step " + (i + 1) });
    T(String(i + 1), { x: sx, y: sy + 0.02, w: 0.36, h: 0.36, fontSize: 11, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T([{ text: a, options: { bold: true, color: INK, breakLine: true } }, { text: b, options: { color: TXT } }],
      { x: sx + 0.48, y: sy, w: sw2 - 0.48, h: 0.62, fontSize: 12 });
    sy += 0.72;
  });
  T([{ text: "Spleen preserving: ", options: { bold: true, color: INK } }, { text: "splenic vessel preservation or Warshaw technique", options: {} }],
    { x: sx, y: sy + 0.05, w: sw2, h: 0.62, fontSize: 11.5, color: TXT, objectName: "Spleen note" });
  y += Math.max(fh + 0.65, sy - y + 0.7);
  const LEFT_END = y;

  // ---------------- RIGHT COLUMN ----------------
  y = section(4, "Clinical outcomes of RDP", RX, top);
  const cellOpt = (bg, col) => ({ fill: { color: bg }, color: col, fontSize: 11.5, valign: "middle", margin: [3, 6, 3, 6] });
  const sym = { g: "▼ ", u: "▲ ", e: "= " };
  const C = (kind, txt, arrow) => {
    const [bg, col] = kind === "g" ? [GOODBG, GOOD] : kind === "b" ? [BADBG, BAD] : [EQBG, EQ];
    return { text: [{ text: arrow, options: { bold: true } }, { text: txt, options: { bold: kind !== "e" } }], options: cellOpt(bg, col) };
  };
  const R = (t) => ({ text: t, options: { bold: true, color: INK, fontSize: 12, valign: "middle", fill: { color: "FFFFFF" }, margin: [3, 6, 3, 2] } });
  const Hd = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: INK }, fontSize: 12, valign: "middle", margin: [3, 6, 3, 6] } });
  const rows = [
    [Hd("Outcome"), Hd("RDP vs open"), Hd("RDP vs laparoscopic")],
    [R("Blood loss"), C("g", "Lower", "▼ "), C("g", "Lower (planned SP)", "▼ ")],
    [R("Complications"), C("g", "Fewer (fistula, wound)", "▼ "), C("e", "Similar overall and fistula", "= ")],
    [R("Hospital stay"), C("g", "Shorter", "▼ "), C("g", "≈1 day shorter", "▼ ")],
    [R("Conversion"), C("e", "Not applicable", ""), C("g", "Fewer to open", "▼ ")],
    [R("Spleen preservation"), C("g", "Higher", "▲ "), C("g", "Higher", "▲ ")],
    [R("Oncological"), C("e", "Non-inferior R0 and nodes", "= "), C("g", "0% vs 2% R1; more nodes", "▲ ")],
    [R("Operative time"), C("e", "Conflicting", "= "), C("b", "≈30 min longer", "▲ ")],
  ];
  const rh = [0.44, 0.47, 0.6, 0.47, 0.47, 0.47, 0.6, 0.47];
  s.addTable(rows, { x: RX, y, w: CW, colW: [1.55, 1.85, CW - 3.4], rowH: rh, border: { type: "solid", pt: 1.5, color: "FFFFFF" }, fontFace: "Arial", objectName: "Outcomes table" });
  y += rh.reduce((a, b) => a + b, 0) + 0.12;
  const key = (bg, col, t) => [{ text: "■ ", options: { color: col } }, { text: t + "  ", options: { color: MUTED } }];
  T([...key(GOODBG, GOOD, "favours RDP"), ...key(EQBG, EQ, "no clear difference"), ...key(BADBG, BAD, "favours comparator"),
     { text: "SP, spleen preservation", options: { color: MUTED } }],
    { x: RX, y, w: CW, h: 0.32, fontSize: 10, objectName: "Table key" });
  y += 0.32 + 0.38;

  y = section(5, "Cost-effectiveness", RX, y);
  const chips = [["Operative cost", "RDP higher"], ["Overall cost", "RDP ≤ LDP < ODP"], ["Quality of life", "RDP > LDP"]];
  const cw3 = (CW - 0.3) / 3;
  chips.forEach(([a, b], i) => {
    const x = RX + i * (cw3 + 0.15);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cw3, h: 0.95, rectRadius: 0.08, fill: { color: i === 0 ? BADBG : GOODBG }, line: { type: "none" }, objectName: "Cost chip " + a });
    T([{ text: a, options: { color: MUTED, fontSize: 11, breakLine: true } }, { text: b, options: { bold: true, color: i === 0 ? BAD : GOOD, fontSize: 13 } }],
      { x: x + 0.05, y, w: cw3 - 0.1, h: 0.95, align: "center", valign: "middle" });
  });
  y += 1.1;
  bullets([
    { text: "Theatre costs are offset by shorter stay, fewer conversions and lower morbidity." },
    { text: "Costs fall as case volume grows." },
    { text: "More QALYs than LDP at similar cost (ROBOCOSTES and others)." },
  ], { x: RX, y, w: CW, h: 1.4, fontSize: 13.5, objectName: "Cost bullets" });
  y += 1.4 + 0.3;

  y = section(6, "Challenges", RX, y);
  const ch = [[fa.FaClock, "Operative time", "Docking adds time; falls along the learning curve"],
    [fa.FaUserDoctor, "Team & training", "Dedicated robotic team; few training centres"],
    [fa.FaScaleUnbalanced, "Access", "High upfront cost; robots concentrated in advanced economies"]];
  for (const [Ic, a, b] of ch) {
    s.addShape(pres.shapes.OVAL, { x: RX, y, w: 0.6, h: 0.6, fill: { color: GOLD }, line: { type: "none" }, objectName: "Challenge icon bg " + a });
    s.addImage({ data: await icon(Ic, "FFFFFF"), x: RX + 0.15, y: y + 0.15, w: 0.3, h: 0.3, altText: a });
    T([{ text: a, options: { bold: true, color: INK, breakLine: true } }, { text: b, options: { color: TXT } }],
      { x: RX + 0.8, y: y - 0.02, w: CW - 0.8, h: 0.7, fontSize: 12.5 });
    y += 0.76;
  }
  const RIGHT_END = y;

  // ---------------- FOOTER: CONCLUSION ----------------
  const FY = Math.max(LEFT_END, RIGHT_END) + 0.2;
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: FY, w: W, h: H - FY, fill: { color: INK }, line: { type: "none" }, objectName: "Conclusion band" });
  T("CONCLUSION", { x: M, y: FY + 0.35, w: 4, h: 0.35, fontSize: 14, bold: true, color: GOLD, charSpacing: 4 });
  const qr = 1.35;
  T([{ text: "RDP offers greater precision, better clinical outcomes and more spleen preservation than open and laparoscopic surgery, and is cost-effective. ", options: { bold: true, color: "FFFFFF" } },
     { text: "Wider adoption depends on training and equitable access.", options: { color: "C9DCDD" } }],
    { x: M, y: FY + 0.75, w: W - 2 * M - qr - 0.5, h: H - FY - 1.0, fontSize: 15.5, valign: "top", objectName: "Conclusion" });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: W - M - qr, y: FY + 0.35, w: qr, h: qr, rectRadius: 0.06, fill: { color: "FFFFFF" }, line: { type: "none" }, objectName: "QR tile" });
  s.addImage({ path: "qr.png", x: W - M - qr + 0.08, y: FY + 0.43, w: qr - 0.16, h: qr - 0.16, altText: "QR code linking to the full paper (doi.org/10.1016/j.lers.2025.02.001)", objectName: "QR code" });
  T("Full paper: Lap Endosc Robot Surg 2025;8:80–83", { x: W - M - 3.2, y: FY + 0.35 + qr + 0.08, w: 3.2, h: 0.3, fontSize: 9.5, color: "C9DCDD", align: "right" });

  console.log("left end", LEFT_END.toFixed(2), "right end", RIGHT_END.toFixed(2), "footer y", FY.toFixed(2), "footer h", (H - FY).toFixed(2));
  await pres.writeFile({ fileName: "poster_custom.pptx" });
  await applyTheme("poster_custom.pptx", THEME);
})();
