# Instruccions per a l'agent que processa un examen

Estàs ajudant a construir una app d'estudi de selectivitat (PAU de Catalunya) per a alumnes de batxillerat.
Processa UN examen (el que t'indiquen al missatge) i genera'n el fitxer de dades.

1. Llegeix l'especificació i segueix-la al peu de la lletra, incloses les particularitats de l'assignatura:
   `D:\46354491s\Desktop\Problemes\tools\ESPECIFICACIO.md`
2. Mira l'exemple de referència (de tecno; mostra l'estil i el detall que volem): `data/tecno/2025-J.json`.
   Si ja hi ha algun fitxer fet de la teva assignatura a `data/<assig>/`, mira'n un també.
3. Fitxers (relatius a `D:\46354491s\Desktop\Problemes`):
   - enunciat `pdfs/<assig>/<ANY>-<J|S>-examen.pdf`, criteris oficials `pdfs/<assig>/<ANY>-<J|S>-solucio.pdf`
   - sortida `data/<assig>/<ANY>-<J|S>.json`, figures a `img/<assig>/<ANY>-<J|S>/`
   - id d'examen `<assig>-<ANY>-<J|S>`; convocatoria `"juny"` (J) o `"setembre"` (S)
   - materia: tecno → segons l'examen; mates → "Matemàtiques"; fisica → "Física"; dibuix → "Dibuix tècnic"
4. Si el PDF conté **diverses sèries**, fes-les totes en el mateix fitxer: `"serie": "3 i 4"` a examen,
   camp `"serie"` a cada problema, i ids amb la sèrie (`mates-2014-J-s3-e2`), imatges `img/.../s3-e2.png`.
5. Entorn: Windows amb Bash POSIX, treballa des de `D:\46354491s\Desktop\Problemes`.
   Python: `/c/Users/46354491s/AppData/Local/Programs/Python/Python313/python.exe` (sempre `-I`).
   Renders temporals en una subcarpeta pròpia del scratchpad amb el nom de l'examen. No toquis fitxers d'altres exàmens.
6. Mira visualment totes les pàgines; inclou TOTS els exercicis i opcions; solucions pas a pas didàctiques,
   verificades (Python/sympy) i contrastades amb l'oficial (discrepàncies a `nota`).
7. Valida amb `node tools/check.js data/<assig>/<ANY>-<J|S>.json` fins que passi, i després
   `python -I tools/crosscheck.py data/<assig>/<ANY>-<J|S>.json` (ha de dir "cap problema sospitós").
8. En acabar, respon en 3-5 línies: nombre de problemes, figures, discrepàncies amb l'oficial i incidències.
