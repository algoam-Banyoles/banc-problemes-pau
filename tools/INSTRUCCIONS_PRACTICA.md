# Problemes de pràctica de Física de 1r (mecànica)

Volem problemes **originals** de pràctica per a una alumna de 1r de batxillerat (Física i Química, Decret 171/2022),
amb el mateix format i qualitat que els problemes de selectivitat de l'app. No són de selectivitat: s'han de veure
com a problemes de pràctica, però amb l'estil, el context realista i el nivell d'un examen.

Llegeix abans:
- `tools/ESPECIFICACIO.md` (format JSON, estil de les solucions pas a pas, LaTeX).
- `tools/CURRICULUM.md` (què és de 1r).
- Un exemple: `data/tecno/2025-J.json` (estil i nivell de detall de les solucions).

## Bloc

T'indiquen el bloc al missatge. Fes **10 problemes amb apartats** (2-4 apartats cadascun, dificultat variada:
3 de dificultat 1, 4 de dificultat 2, 3 de dificultat 3) i **4 qüestions de test** (4 opcions, una correcta, amb
distractors que corresponguin a errors típics). Contextos variats i reals (esport, trànsit, Catalunya, enginyeria,
vida quotidiana). Res que necessiti continguts de 2n (gravitació universal, camps, MHS, ones...).

## Fitxer de sortida

`data/fisica1/practica-<bloc>.json`:

```json
{
  "examen": {
    "id": "fisica1-practica-<bloc>",
    "assignatura": "fisica1",
    "materia": "Problemes de pràctica · Física de 1r",
    "practica": true,
    "any": 2026,
    "convocatoria": "practica",
    "serie": null,
    "pdf_examen": null,
    "pdf_solucio": null,
    "estructura": "Problemes originals de pràctica (no són de selectivitat), bloc: <nom del bloc>."
  },
  "problemes": [ ... ]
}
```

Cada problema segueix el format de l'especificació, amb aquests valors:
- `id`: `fisica1-<bloc>-NN` (01, 02...). `exercici`: el número NN. `questio`: null. `opcio`: null. `punts`: 2.5 (test: 0.5).
- `tema`: un d'aquests ids: `cinematica`, `dinamica`, `energia-mecanica`, `moment-lineal`, `estatica`, `calor`.
  `temes_secundaris`: altres d'aquesta llista si cal.
- `conceptes`: 3-8, en minúscula, reutilitza aquests noms quan escaigui: MRU, MRUA, caiguda lliure, tir parabòlic,
  tir horitzontal, MCU, MCUA, velocitat angular, acceleració centrípeta, lleis de Newton, diagrama de cos lliure,
  força de fregament, pla inclinat, tensió d'una corda, politja, força centrípeta, treball, potència, rendiment,
  energia cinètica, energia potencial gravitatòria, energia potencial elàstica, conservació de l'energia mecànica,
  treball de les forces no conservatives, impuls, moment lineal, conservació del moment lineal, xocs, moment d'una força,
  equilibri del sòlid rígid, calor específica, canvi d'estat, equilibri tèrmic, gràfica v-t, gràfica x-t.
- `curs`: "1r", `curs_motiu`: frase curta, `apartats_1r`: nombre d'apartats; cada apartat amb `"curs": "1r"`.
- `pagines`: [], `figures`: [] (o figures si en fas, vegeu més avall).
- `solucio`: com a l'especificació: "Dades i incògnites", passos per apartat amb el per què, fórmula, substitució
  i resultat amb unitats; `resultats`; `nota` amb errors típics.
- Usa g = 9,8 m/s² (digues-ho a l'enunciat). Decimals amb coma.

**Verifica tots els números amb Python** abans d'escriure'ls. Les respostes de test han de ser inequívoques.

## Figures (opcional, recomanat per a pla inclinat, politges, tir parabòlic, gràfiques)

Pots generar figures senzilles amb matplotlib (`python -m pip install matplotlib` si no hi és) a
`img/fisica1/<bloc>/NN.png` (fons blanc, línies negres, etiquetes llegibles, ~800 px d'ample). Comprova-les amb Read.
Format a `figures`: `[{"src": "img/fisica1/<bloc>/NN.png", "peu": "..."}]`.

## Com treballar

Python: `/c/Users/46354491s/AppData/Local/Programs/Python/Python313/python.exe -I -X utf8`. Scripts i temporals
en una subcarpeta pròpia del scratchpad (`practica-<bloc>/`). Genera el JSON amb un script (`json.dumps(...,
ensure_ascii=False, indent=2)`), així eviten errors d'escapament de LaTeX.

Valida amb `node tools/check.js data/fisica1/practica-<bloc>.json` fins que passi.
Respon en 4-6 línies: llista de problemes (títol curt) i incidències.
