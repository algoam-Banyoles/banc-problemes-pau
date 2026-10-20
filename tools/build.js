// Ajunta tots els data/<assig>/*.json en data.js (l'app el carrega amb <script>, funciona obrint index.html directament)
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "data");
const examens = [];
const problemes = [];

for (const assig of fs.readdirSync(DATA)) {
  const dir = path.join(DATA, assig);
  if (!fs.statSync(dir).isDirectory()) continue;
  for (const f of fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort()) {
    const d = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
    examens.push(d.examen);
    for (const p of d.problemes) problemes.push({ ...p, examen: d.examen.id });
  }
}

const out = `window.SELE = ${JSON.stringify({ generat: new Date().toISOString().slice(0, 10), examens, problemes })};\n`;
fs.writeFileSync(path.join(ROOT, "data.js"), out);
console.log(`data.js: ${examens.length} exàmens, ${problemes.length} problemes`);
