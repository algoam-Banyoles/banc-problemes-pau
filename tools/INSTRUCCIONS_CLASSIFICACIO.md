# Revisió de la classificació múltiple (temes i conceptes)

Objectiu: que cada problema es pugui trobar per **tots** els continguts que treballa, i que les etiquetes
siguin uniformes entre exàmens (perquè funcionin com a filtres a l'app).

Treballes sobre UNA assignatura (`data/<assig>/*.json`, des de `D:\46354491s\Desktop\Problemes`).
Llista de temes vàlids: `tools/ESPECIFICACIO.md` (taula de l'assignatura). Currículum: `tools/CURRICULUM.md`.

## 1. Vocabulari controlat

Llegeix tots els `conceptes` actuals de l'assignatura i crea `tools/vocabulari/<assig>.json`:

```json
{ "<tema_id>": ["concepte canònic", "..."], "...": [] }
```

- 40-90 conceptes en total, agrupats sota el tema on encaixen millor (cada concepte en un sol tema).
- En minúscula, en català, en singular, curts i reconeixibles per un alumne ("relació de transmissió",
  "regla de Barrow", "abatiment", "efecte fotoelèctric"). Sigles en majúscula: MRU, MRUA, MCU, MHS, CC, CA.
- Unifica sinònims i variants (escala/escales, "funció lògica"/"funció booleana"...).
- Han de ser prou concrets per servir de filtre (no "càlcul" ni "problema"), però no tan concrets que només
  surtin en un problema. Un concepte hauria de sortir com a mínim a 2 problemes.
- **Conserva** aquestes etiquetes si són de la teva assignatura: MRU, MRUA, MCU, caiguda lliure, tir parabòlic.

## 2. Revisió problema per problema

Per a cada problema, mirant enunciat, apartats i **la solució** (què s'aplica de fet):

- `tema`: el tema principal (el que pesa més).
- `temes_secundaris`: **tots** els altres temes de la taula que es fan servir en algun apartat o pas de la
  solució. Un problema amb diversos apartats sol tocar més d'un tema; no te'n deixis cap. No hi repeteixis `tema`.
- `conceptes`: 3-8 conceptes **del vocabulari**, tots els que el problema exercita realment (incloent-hi
  els d'apartats concrets i les eines que s'han de saber fer servir: p. ex. "diagrama de cos lliure",
  "conservació de l'energia", "regla de Cramer").

No toquis cap altre camp (ni enunciats, ni solucions, ni `curs`, ni `dificultat`).

## 3. Com modificar

Script Python al teu scratchpad (`/c/Users/46354491s/AppData/Local/Programs/Python/Python313/python.exe -I -X utf8`):
llegeix cada JSON, canvia només `tema`, `temes_secundaris` i `conceptes`, i reescriu amb
`json.dumps(d, ensure_ascii=False, indent=2) + "\n"` mantenint CRLF si el fitxer en tenia.
Fes primer una còpia de seguretat de `data/<assig>/` al scratchpad.

Comprova al final:
- `node tools/check.js data/<assig>/*.json` passa.
- Tots els `conceptes` de tots els problemes són al vocabulari i cada concepte del vocabulari s'usa almenys 2 cops
  (o elimina'l del vocabulari).

Respon en 5-8 línies: mida del vocabulari, quants problemes tenien només un tema abans i ara, mitjana de
conceptes per problema, i els casos dubtosos.
