# tools/ — del full de càlcul al joc

Aquestes eines fan que el catàleg de cançons s'editi **en un sol lloc**
(`bases/canconet_master.xlsx`) i arribi al joc sense tocar l'`index.html` a mà.

Cal Python 3 i `openpyxl` (`pip install openpyxl`).

## Ús habitual

```bash
python tools/build_songs.py --check   # comprova el màster i informa
python tools/build_songs.py           # regenera index.html + data/*.csv
```

`build_songs.py` només reescriu els arrays `SONGS_CA/ES/EU/INT`. La resta de
l'`index.html` (el joc en si) no es toca mai.

S'atura i no publica si troba: `id_joc` repetit, `dzId` repetit dins d'un idioma,
files sense `dzId`/títol/artista, o cançons que tornen de la quarantena.

Després d'un build, **puja la versió de la memòria cau a `sw.js`** o els jugadors
seguiran amb la versió antiga (el *service worker* serveix de la memòria cau).

## Les altres eines

| Eina | Què fa |
| --- | --- |
| `find_dzids.py` | busca a l'API pública de Deezer els `dzId` que falten i deixa les propostes a `dzid_proposals.json` amb un % de confiança. Mai toca el catàleg. |
| `make_master.py` | refà `canconet_master.xlsx` des de zero a partir de les fonts històriques de `bases/_arxiu/` i de l'`index.html` actual. Normalment **no cal** tornar-lo a executar. |
| `songlib.py` | llibreria compartida: llegeix i escriu els arrays de cançons. |

## `data/*.csv`

Cada build hi deixa una còpia del catàleg en CSV. Serveix per veure al *pull request*
exactament quines cançons canvien (l'Excel és binari i no es pot comparar) i com a còpia
de seguretat en text pla.

## Detalls que expliquen decisions del codi

- **Cançons sense any**: n'hi ha moltes (el full les té com a `N/D`). Els nivells 3 i 7
  pregunten l'any; si la cançó no en té, `getAnswerMode` canvia a una altra pregunta.
  Abans sortia un únic botó que deia `undefined` i el jugador hi perdia una vida.
- **No omplim l'any des de Deezer**: es va provar i només encerta la meitat de les vegades
  (retorna la data de la reedició: *L'Empordà* de 1989 hi surt com a 2014). En un joc
  d'endevinar l'any, una dada dolenta és pitjor que no tenir-ne.
- **`seg` i `ytId` no s'escriuen**: `seg` el llegia només `getSegBounds`, que no es cridava
  des d'enlloc (la reproducció fa servir `DZ_SEGS`, finestres fixes per nivell), i YouTube
  es va retirar. Eren 78 KB morts dins de l'`index.html`.
