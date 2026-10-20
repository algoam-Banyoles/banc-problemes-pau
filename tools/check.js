// Valida un fitxer de dades d'examen: node tools/check.js data/tecno/2025-J.json [...]
const fs = require("fs");
const path = require("path");
const katex = require("katex");
console.warn = () => {};

const ROOT = path.resolve(__dirname, "..");
const TEMES = {
  tecno: ["estatica", "resistencia", "materials", "mecanismes", "mecanica", "termica", "energia", "circuits",
    "maquines-electriques", "electronica", "digital", "control", "pneumatica", "fabricacio", "programacio",
    "disseny", "economia"],
  mates: ["matrius", "sistemes", "geometria", "funcions", "derivades", "optimitzacio", "integrals", "probabilitat", "estadistica"],
  fisica: ["mecanica", "gravitacio", "camp-electric", "camp-magnetic", "induccio", "oscillacions", "ones", "optica",
    "relativitat", "quantica", "nuclear"],
  dibuix: ["geometria-plana", "transformacions", "corbes", "diedric", "cossos", "axonometria", "conica", "normalitzacio"],
};

function mathErrors(text, where) {
  const errs = [];
  if (typeof text !== "string") return errs;
  const re = /\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$/g;
  let m;
  while ((m = re.exec(text))) {
    const tex = m[1] ?? m[2];
    try {
      katex.renderToString(tex, { throwOnError: true, strict: "ignore", displayMode: !!m[1] });
    } catch (e) {
      errs.push(`${where}: KaTeX: ${e.message.split("\n")[0]}  ← ${tex.slice(0, 80)}`);
    }
  }
  const stripped = text.replace(re, "");
  if ((stripped.match(/\$/g) || []).length) errs.push(`${where}: "$" desaparellat`);
  return errs;
}

function check(file) {
  const errs = [];
  let data;
  try {
    data = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch (e) {
    return [`JSON invàlid: ${e.message}`];
  }
  const ex = data.examen || {};
  for (const k of ["id", "assignatura", "materia", "any", "convocatoria", "pdf_examen"])
    if (ex[k] === undefined || ex[k] === "") errs.push(`examen.${k} falta`);
  const temes = TEMES[ex.assignatura];
  const ids = new Set();
  (data.problemes || []).forEach((p, i) => {
    const w = p.id || `problema[${i}]`;
    if (!p.id) errs.push(`${w}: falta id`);
    if (ids.has(p.id)) errs.push(`${w}: id repetit`);
    ids.add(p.id);
    if (!["test", "problema"].includes(p.tipus)) errs.push(`${w}: tipus invàlid`);
    for (const k of ["titol", "tema", "solucio"]) if (!p[k]) errs.push(`${w}: falta ${k}`);
    if (!p.enunciat && !(p.apartats || []).length) errs.push(`${w}: falta enunciat`);
    if (temes) {
      if (!temes.includes(p.tema)) errs.push(`${w}: tema desconegut "${p.tema}"`);
      for (const t of p.temes_secundaris || []) if (!temes.includes(t)) errs.push(`${w}: tema secundari desconegut "${t}"`);
    }
    if (p.tipus === "test") {
      if (!p.opcions || Object.keys(p.opcions).length < 2) errs.push(`${w}: test sense opcions`);
      if (!p.solucio?.resposta) errs.push(`${w}: test sense solucio.resposta`);
      else if (p.opcions && !p.opcions[p.solucio.resposta]) errs.push(`${w}: resposta "${p.solucio.resposta}" no és cap opció`);
    }
    if (!p.solucio?.passos?.length) errs.push(`${w}: solució sense passos`);
    for (const f of p.figures || []) {
      if (typeof f !== "object" || !f.src) { errs.push(`${w}: cada figura ha de ser {"src": "...", "peu": "..."}`); continue; }
      if (!fs.existsSync(path.join(ROOT, f.src))) errs.push(`${w}: figura no existeix ${f.src}`);
    }
    const texts = [[p.enunciat, "enunciat"]];
    for (const [k, v] of Object.entries(p.opcions || {})) texts.push([v, `opció ${k}`]);
    for (const a of p.apartats || []) texts.push([a.enunciat, `apartat ${a.id}`]);
    for (const [j, s] of (p.solucio?.passos || []).entries()) {
      texts.push([s.cos, `pas ${j + 1}`]);
      texts.push([s.titol, `títol pas ${j + 1}`]);
    }
    for (const r of p.solucio?.resultats || []) texts.push([r.valor, `resultat ${r.apartat ?? ""}`]);
    texts.push([p.solucio?.nota, "nota"]);
    for (const [t, where] of texts) errs.push(...mathErrors(t, `${w} ${where}`));
    // imatges dins de la solució
    for (const s of p.solucio?.passos || []) {
      for (const m of (s.cos || "").matchAll(/!\[[^\]]*\]\(([^)]+)\)/g))
        if (!fs.existsSync(path.join(ROOT, m[1]))) errs.push(`${w}: imatge de solució no existeix ${m[1]}`);
    }
  });
  if (!ids.size) errs.push("cap problema");
  return errs;
}

let bad = 0;
for (const f of process.argv.slice(2)) {
  const errs = check(f);
  const n = (() => { try { return JSON.parse(fs.readFileSync(f, "utf8")).problemes.length; } catch { return "?"; } })();
  if (errs.length) {
    bad++;
    console.log(`✗ ${f} (${n} problemes, ${errs.length} errors)`);
    for (const e of errs) console.log("   " + e);
  } else console.log(`✓ ${f} (${n} problemes)`);
}
process.exit(bad ? 1 : 0);
