# Curs per apartat

Cada problema ja té `curs` ("1r"/"2n") pel contingut més alt que necessita. Ara volem saber, **apartat per apartat**,
quins es poden fer amb continguts de 1r, perquè una alumna de 1r pugui practicar aquells apartats encara que
el problema sencer sigui de 2n.

Assignatura: la que t'indiquen. Fitxers: `data/<assig>/*.json` (des de `D:\46354491s\Desktop\Problemes`).
Referència: `tools/CURRICULUM.md`, **Decret 171/2022 (vigent)**.

## Què has de fer

Per a cada problema amb `"curs": "2n"` que tingui `apartats`:
- A cada apartat afegeix `"curs": "1r"|"2n"` i, si és "1r", `"curs_motiu"` (frase curta: quin contingut de 1r fa servir).
- Un apartat és "1r" si es pot **resoldre tot sol** amb continguts de 1r, fent servir les dades de l'enunciat
  i, si cal, el resultat d'un apartat anterior com a dada (encara que aquell apartat sigui de 2n). Mira la
  solució d'aquell apartat (passos amb `"apartat": "<id>"`) per veure què s'aplica de fet.
- Sigues realista: si l'apartat només té sentit entenent un concepte de 2n (p. ex. "energia potencial
  gravitatòria −GMm/r", "flux magnètic", "MHS"), és "2n".

Per als problemes amb `"curs": "1r"`: posa `"curs": "1r"` a tots els apartats (sense motiu).
Els problemes sense apartats (qüestions de test) no es toquen.

Afegeix també a cada problema el camp `"apartats_1r": <nombre d'apartats de 1r>` just després de `curs_motiu`.

## Com modificar

Script Python al teu scratchpad, en una **subcarpeta pròpia** (`curs_apartats_<assig>/`), amb còpia de seguretat de `data/<assig>/`:
`/c/Users/46354491s/AppData/Local/Programs/Python/Python313/python.exe -I -X utf8`. Llegeix cada JSON, canvia
només això, i reescriu amb `json.dumps(d, ensure_ascii=False, indent=2) + "\n"`, mantenint CRLF si en tenia.
No toquis cap altre camp.

Valida amb `node tools/check.js data/<assig>/*.json`.

Respon en 4-6 línies: quants problemes de 2n tenen algun apartat de 1r, quants apartats de 1r en total, i exemples típics.
