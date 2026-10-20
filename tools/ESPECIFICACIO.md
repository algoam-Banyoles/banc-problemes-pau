# Especificació: extracció de problemes de selectivitat

Objectiu: per a un examen (PDF d'enunciat + PDF de criteris de correcció oficials), generar UN fitxer JSON
amb tots els problemes, preparats per a una app d'estudi per a alumnes de batxillerat (16-18 anys).
Tot el text en **català**.

## Eines (executa sempre des de l'arrel `D:\46354491s\Desktop\Problemes`)

```
PY=/c/Users/46354491s/AppData/Local/Programs/Python/Python313/python.exe
$PY -I tools/pdftools.py text PDF [PAG]              # text amb coordenades de blocs (punts PDF)
$PY -I tools/pdftools.py render PDF PAG OUT.png      # pàgina sencera, per MIRAR-LA amb l'eina Read
$PY -I tools/pdftools.py figs PDF PAG                # caixes candidates de figures (imatges + vectors)
$PY -I tools/pdftools.py crop PDF PAG x0 y0 x1 y1 OUT.png   # retalla una figura
$PY -I tools/pdftools.py lines PDF PAG [x0 y0 x1 y1]      # segments i corbes vectorials (mesurar dibuixos)
$PY -I tools/sheet.py img/<assig>/<examen> OUT.png   # full de contactes de totes les teves figures (per revisar-les)
node tools/check.js data/<assig>/<id>.json           # VALIDADOR: cal que passi sense errors
```

Guarda els renders temporals al scratchpad (no a la carpeta del projecte), **dins d'una subcarpeta pròpia amb el nom
del teu examen** (p. ex. `scratchpad/fisica-2019-J/`): hi ha altres agents treballant en paral·lel i els noms es trepitgen.
Si `pdftools text` dona error de codificació, posa `PYTHONIOENCODING=utf-8` davant.

**Mira sempre visualment cada pàgina** amb render + Read: el text extret perd fórmules, exponents,
toleràncies, taules i dades dins de figures. El text és només una ajuda per copiar.

## Figures

- Retalla cada figura/esquema/gràfica/taula-imatge necessària per entendre el problema amb `crop`.
  Usa `figs` per trobar les coordenades i deixa ~6 punts de marge. Comprova el retall amb Read:
  no ha de tallar etiquetes ni incloure text de l'enunciat, números de pàgina ni caixes de correcció.
- Si les opcions d'una qüestió de test són dibuixos, retalla-les juntes en una figura.
- Taules senzilles de dades: millor transcriure-les en Markdown que retallar-les.
- Nom: `img/<assig>/<examen>/<id-curt>.png`, p. ex. `img/tecno/2025-J/e3.png`, `img/tecno/2025-J/e1-q5.png`
  (afegeix `-2`, `-3` si n'hi ha més d'una). Si la solució oficial té un esquema útil (p. ex. un circuit de
  portes lògiques), també el pots retallar (`e2-sol.png`) i posar-lo dins d'un pas de la solució.

## Format JSON (`data/<assig>/<examen>.json`)

```json
{
  "examen": {
    "id": "tecno-2025-J",
    "assignatura": "tecno",
    "materia": "Tecnologia i Enginyeria",
    "any": 2025,
    "convocatoria": "juny",
    "serie": "1",
    "pdf_examen": "pdfs/tecno/2025-J-examen.pdf",
    "pdf_solucio": "pdfs/tecno/2025-J-solucio.pdf",
    "estructura": "4 exercicis obligatoris de 2,5 punts. A l'exercici 1 cal respondre 5 de les 8 qüestions."
  },
  "problemes": [
    {
      "id": "tecno-2025-J-e1-q2",
      "exercici": 1,
      "questio": 2,
      "opcio": null,
      "tipus": "test",
      "punts": 0.5,
      "titol": "Consum de propà per cicle en un motor de 4 temps",
      "tema": "termica",
      "temes_secundaris": [],
      "conceptes": ["motor de quatre temps", "cicle termodinàmic", "consum horari"],
      "dificultat": 2,
      "pagines": [2],
      "enunciat": "Un motor de propà líquid consumeix $7{,}5\\ \\text{kg/h}$ quan funciona a $2\\,500\\ \\text{min}^{-1}$. ...",
      "figures": [],
      "opcions": {"a": "20 g", "b": "10 g", "c": "100 g", "d": "200 g"},
      "apartats": [],
      "solucio": {
        "resposta": "b",
        "passos": [
          {"apartat": null, "titol": "Què ens demanen", "cos": "..."},
          {"apartat": null, "titol": "Cicles per minut en un motor de 4 temps", "cos": "..."}
        ],
        "resultats": [{"apartat": null, "valor": "$m = 10\\ \\text{g}$ → resposta **b**"}],
        "nota": ""
      }
    }
  ]
}
```

### Camps

- `id`: `<examen-id>-e<exercici>[-q<questio>][-<opcio en minúscula>]`. Únic. Ex: `tecno-2016-J-e3-a` (exercici 3, opció A).
- `exercici`: número tal com surt a l'examen. `questio`: número de la qüestió de test (o `null`).
- `opcio`: `"A"`/`"B"` si l'examen té optativitat per opcions (OPCIÓ A / OPCIÓ B), si no `null`.
  Si l'examen diu "escolliu N exercicis d'entre M", posa `opcio: null` i explica-ho a `estructura`.
- `tipus`: `"test"` (qüestió d'opció múltiple) o `"problema"` (tota la resta, inclosos exercicis teòrics/oberts).
- **Cada qüestió de test és un element separat.** Un exercici amb apartats a), b), c)… és UN element amb `apartats`.
- `punts`: puntuació de l'element.
- `titol`: curt i descriptiu del què va el problema (NO "Exercici 3"). Útil per cercar.
- `tema`: UN d'aquests identificadors (el principal):

| id | tema |
|---|---|
| `estatica` | Estàtica i estructures (forces, moments, reaccions, equilibri, bigues, cables) |
| `resistencia` | Resistència de materials (tensió, deformació, mòdul de Young, coeficient de seguretat, assaig de tracció) |
| `materials` | Materials i propietats (classificació, assaigs, duresa, tractaments, reciclatge) |
| `mecanismes` | Mecanismes i transmissions (engranatges, politges, cargol-femella, relació de transmissió, parell) |
| `mecanica` | Cinemàtica, treball, energia i potència mecànica (velocitats, fregament, rendiment mecànic) |
| `termica` | Màquines tèrmiques i motors (combustió, cicles, calor, bomba de calor, frigorífiques) |
| `energia` | Energia i recursos (fonts, centrals, consum, factura, impacte ambiental, combustibles) |
| `circuits` | Circuits elèctrics (corrent continu i altern, Ohm, Kirchhoff, potència, resistències) |
| `maquines-electriques` | Màquines elèctriques (motors CC/CA, generadors, transformadors) |
| `electronica` | Electrònica (díodes, transistors, condensadors, sensors, amplificadors) |
| `digital` | Sistemes digitals (lògica, taules de veritat, portes, Karnaugh, codificació) |
| `control` | Control i automatització (llaç obert/tancat, diagrames de blocs, sensors, autòmats, robòtica) |
| `pneumatica` | Pneumàtica i oleohidràulica (cilindres, vàlvules, pressió, cabal) |
| `fabricacio` | Fabricació, metrologia i toleràncies (ajustos, mesura, processos de fabricació) |
| `programacio` | Programació i algorismes |
| `disseny` | Disseny, representació gràfica i projecte tecnològic |
| `economia` | Costos, pressupostos i economia del producte |

La taula anterior és per a **tecno**. Per a les altres assignatures, usa aquests ids:

**mates** (Matemàtiques):

| id | tema |
|---|---|
| `matrius` | Matrius i determinants (operacions, inversa, rang, equacions matricials) |
| `sistemes` | Sistemes d'equacions lineals (discussió amb paràmetres, Rouché, Cramer, Gauss) |
| `geometria` | Geometria a l'espai (vectors, rectes, plans, posicions relatives, distàncies, angles, àrees i volums) |
| `funcions` | Funcions: límits, continuïtat i estudi (dominis, asímptotes, gràfiques) |
| `derivades` | Derivades i aplicacions (recta tangent, monotonia, extrems, Rolle, Bolzano, valor mitjà) |
| `optimitzacio` | Problemes d'optimització |
| `integrals` | Integrals (primitives, integral definida, àrees) |
| `probabilitat` | Probabilitat (Bayes, probabilitat total, combinatòria) |
| `estadistica` | Estadística i distribucions (binomial, normal) |

**fisica** (Física):

| id | tema |
|---|---|
| `mecanica` | Cinemàtica, dinàmica i energia mecànica |
| `gravitacio` | Camp gravitatori (satèl·lits, òrbites, energia potencial gravitatòria) |
| `camp-electric` | Camp elèctric (càrregues, potencial, condensadors) |
| `camp-magnetic` | Camp magnètic (forces sobre càrregues i corrents, espectròmetre) |
| `induccio` | Inducció electromagnètica (Faraday, Lenz, alternadors, transformadors) |
| `oscillacions` | Moviment harmònic simple i oscil·ladors |
| `ones` | Ones mecàniques i so (equació d'ona, interferències, ones estacionàries, intensitat sonora, Doppler) |
| `optica` | Òptica (reflexió, refracció, lents, miralls, ones electromagnètiques) |
| `relativitat` | Física relativista |
| `quantica` | Física quàntica (efecte fotoelèctric, de Broglie, espectres, làser) |
| `nuclear` | Física nuclear i de partícules (desintegració, període de semidesintegració, fissió, fusió) |

**dibuix** (Dibuix tècnic):

| id | tema |
|---|---|
| `geometria-plana` | Geometria plana (traçats, polígons, arc capaç, tangències i enllaços, escales) |
| `transformacions` | Transformacions geomètriques (homologia, afinitat, inversió, simetries, girs) |
| `corbes` | Corbes tècniques i còniques (el·lipse, paràbola, hipèrbola, ovals) |
| `diedric` | Sistema dièdric (punts, rectes, plans, interseccions, abatiments, girs, canvis de pla, vertaderes magnituds) |
| `cossos` | Cossos i superfícies en dièdric (poliedres, seccions planes, desenvolupaments) |
| `axonometria` | Sistemes axonomètrics (isomètric, dimètric, cavaller, militar) |
| `conica` | Perspectiva cònica |
| `normalitzacio` | Normalització i croquis (vistes, acotació, talls, escales) |

- `temes_secundaris`: altres ids de la taula si el problema en toca més d'un.
- `conceptes`: 2-6 etiquetes lliures en minúscula (p. ex. "relació de transmissió", "rendiment", "potència elèctrica").
  Reutilitza noms habituals perquè les cerques funcionin entre exàmens.
- `dificultat`: 1 (directe, una fórmula), 2 (diversos passos), 3 (cal raonar/encadenar molt).
- `pagines`: pàgines del PDF d'enunciat on surt.
- `enunciat`: text complet de l'enunciat (introducció/dades comunes), fidel a l'original, en Markdown + LaTeX.
  Per a problemes amb apartats, aquí NOMÉS la part comuna; cada apartat va a `apartats`. Si no hi ha part comuna, deixa-ho buit (`""`).
- `apartats`: `[{"id": "a", "enunciat": "La potència mecànica necessària per a elevar el cotxe, $P_\\text{mec}$.", "punts": 0.5}]`.
  Inclou la frase "Determineu:" / "Responeu:" a l'enunciat comú si hi és.
- `opcions` (només test): diccionari lletra → text (Markdown/LaTeX). Si les opcions són una figura, posa `"(vegeu la figura)"`.
  Als problemes que no són de test: `"opcions": {}` i `"solucio": {"resposta": null, ...}`.
- `figures`: llista d'objectes `{"src": "img/tecno/2025-J/e3.png", "peu": "Esquema de l'elevador"}` (mai strings sols).
- Imatges dins d'un pas de la solució: sintaxi Markdown `![descripció](img/tecno/2025-J/e2-sol.png)`.

Exemple de referència ja fet i revisat: `data/tecno/2025-J.json`. Mira'l abans de començar per copiar-ne l'estil i el nivell de detall.

### Solució (`solucio`) — el més important

Ha de ser **pas a pas**, com la faria un bon professor a la pissarra per a un alumne que no sap fer-la:

1. Primer pas (si hi ha càlculs): **"Dades i incògnites"** — llista les dades amb unitats (passades al SI si cal) i què es busca.
2. Per cada apartat, un o més passos amb `apartat` = "a", "b"… Cada pas:
   - `titol`: què fem en aquest pas (p. ex. "Potència mecànica a partir de l'energia potencial").
   - `cos`: 1-2 frases de **per què** (quina idea física/tècnica s'aplica), després la **fórmula general**,
     la **substitució amb números i unitats**, i el **resultat** destacat en negreta amb unitats.
     Usa `$$...$$` per a les equacions importants.
3. Per a qüestions de test: explica el raonament o el càlcul que porta a la resposta correcta i, breument,
   per què les altres són incorrectes o quin error típic porta a cada una (si és evident).
4. Per a lògica digital: taula de veritat en Markdown, funció canònica, simplificació (Karnaugh o àlgebra, explicada),
   i descripció del circuit de portes (o figura retallada de la solució oficial). Les barres de negació de la solució
   oficial costen de llegir: fes un `crop` ampliat de la fórmula per llegir-la bé, i usa `\\bar{x}` o `\\overline{xy}`.
5. `resultats`: resum dels resultats finals per apartat (per autocomprovar-se).
6. `nota`: opcional. Consells, errors típics, o **discrepàncies amb la solució oficial**.

**Els resultats han de coincidir amb els criteris de correcció oficials** (PDF de solució). Fes tu els càlculs
(pots usar Python per verificar números) i compara. Si l'oficial té un error clar, posa la teva solució
correcta i explica la discrepància a `nota`. Si l'oficial no dona la resposta d'alguna cosa, resol-la tu.
Usa `g = 9,807 m/s²` si l'examen o la solució oficial ho fa així (mira-ho), i el mateix arrodoniment.

### Particularitats per assignatura

- **Mates**: les solucions oficials són força completes. Igualment, redacta el pas a pas pensant en l'alumne:
  digues quin mètode fas servir i per què (p. ex. "com que la matriu depèn d'un paràmetre, estudiem quan el
  determinant és zero"), fes els càlculs intermedis complets (determinants, derivades, integrals per parts…) i
  interpreta el resultat. Si l'oficial dona diversos mètodes, tria'n el més clar i esmenta l'altre a `nota`.
  Verifica amb Python (pots fer servir `sympy` si està instal·lat; si no, `pip install sympy`).
- **Física**: dades amb unitats SI, fórmula general → substitució → resultat amb unitats i xifres significatives
  raonables. Explica els conceptes (p. ex. "la força gravitatòria fa de força centrípeta"). Si cal un esquema
  (forces, camps, raigs), retalla'l de l'oficial si n'hi ha. Usa les constants que dona l'examen.
  En els exàmens antics hi ha una part comuna i una part optativa (opció A / opció B): inclou-les totes.
- **Dibuix tècnic**: cada exercici és una construcció gràfica sobre un dibuix donat.
  - `figures`: retalla el dibuix donat de l'enunciat (la làmina amb les dades), sencer i llegible.
  - `tipus`: `"problema"`.
  - `solucio.passos`: el **procediment de construcció** ordenat, com un professor explicant-lo a la pissarra:
    quina construcció geomètrica fas a cada pas i per què (p. ex. "el centre de l'arc tangent a les dues rectes
    és a la bisectriu de l'angle que formen, perquè equidista de totes dues"), quins punts determines, i com ho
    comproves. Usa els noms de punts/rectes de l'enunciat (`a-a′`, `r-r′`, LT...).
  - L'últim pas ha de ser "Resultat final" amb la imatge de la solució oficial retallada:
    `![Solució oficial](img/dibuix/2025-J/1A-sol.png)`. Si l'oficial té més d'una làmina per exercici, posa-les totes.
  - `resultats`: una frase per apartat del que s'obté (p. ex. "Aresta de l'octaedre: 4,2 cm").
  - Si a un exercici hi ha opcions A i B, són dos elements diferents (`opcio: "A"` i `"B"`).
  - Per citar mides reals al pas a pas, mesura sobre el PDF: 1 punt PDF = 0,3528 mm (les coordenades de
    `pdftools text`/`figs` són en punts). Comprova-les amb les cotes de l'enunciat.
  - Axonometria: fes un `crop` ampliat de les vistes per interpretar bé el sòlid. Al pas a pas, digues les
    mides del prisma envolupant, en quin ordre es construeixen els volums i les coordenades (x, y, z) dels
    vèrtexs clau mesurades a les vistes, a l'escala i amb els coeficients de reducció de la terna demanada.
  - A la imatge de la solució oficial pots deixar fora el regle graduat.
  - Els perfils de vegades venen girats 90°: comprova-ho i avisa-ho a la solució.
  - La disposició de les vistes varia d'un examen a l'altre: identifica-les per les referències (a, a′, a″),
    no per la posició a la làmina.
  - `figs` no detecta bé les làmines vectorials: retalla a mà a partir del render (punts = píxels del render / 1,5).
  - Per llegir detalls d'una làmina escanejada, `crop` d'una zona petita ja fa zoom (2,5×).
  - Noms de figures: `1A.png` (làmina de dades del dibuix 1, opció A), `1A-sol.png` (solució oficial).
  - **Obre amb Read TOTS els retalls** abans d'acabar (no n'hi ha prou de mirar-ne uns quants).

### Format del text

- Markdown + LaTeX (KaTeX): `$...$` en línia, `$$...$$` en bloc. **Al JSON, les barres invertides es dupliquen** (`\\frac`).
- Decimals amb coma com a l'examen: dins de LaTeX escriu `7{,}5` (amb claus, perquè no quedi espai).
- Unitats en LaTeX amb `\\text{}`: `$1491\\ \\text{W}$`. Fora de LaTeX també pots escriure-les en text normal.
- El símbol € no funciona dins de LaTeX: escriu-lo fora de les fórmules (`$12{,}5$ €`) o `\\text{euros}` dins.
  El punt volat (·) tampoc: dins de LaTeX usa `\\cdot`.
- Multiplicació: `\\cdot`. Subíndexs de paraules: `P_\\text{mec}`.
- Taules: Markdown amb `|`. Llistes amb `- `. Salts de paràgraf amb `\n\n`.
- No posis HTML.

### Validació

Al final executa `node tools/check.js data/<assig>/<examen>.json` i corregeix fins que no doni errors
(comprova JSON, camps obligatoris, temes vàlids, que les figures existeixin i que totes les fórmules KaTeX compilin).
