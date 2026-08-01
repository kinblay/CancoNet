# CançoNet — regles del projecte

Joc musical català d'endevinar cançons. PWA d'un sol `index.html`, desplegada a
**canconet.net via GitHub Pages des de la branca `main`** → fer merge a main = publicar EN VIU.

## Regles d'or (per a qualsevol agent o sessió)

1. **Mai es treballa directament a `main`.** Sempre branca + pull request. El merge el fa l'usuari.
2. **Bump de `sw.js` obligatori** quan el canvi afecta el que veu el jugador (`index.html`,
   `manifest.json`, icones): puja `canconet-vNN` → `vNN+1`. El service worker és cache-first;
   sense bump, els jugadors amb la PWA instal·lada NO reben el canvi. Canvis només de
   `.claude/`, `tools/`, `data/` o docs: sense bump.
3. **`id_joc` no es canvia mai** a una cançó existent: és la clau de la telemetria
   (`game_rounds.song_id`) i del rastre històric.
4. **El catàleg NO s'edita a mà dins d'`index.html`.** S'edita `bases/canconet_master.xlsx`
   (fora del repo) i es regenera amb `python tools/build_songs.py` (vegeu `tools/README.md`).
5. **L'any d'una cançó mai surt del `release_date` de Deezer** (és la data de reedició; mesurat
   ~49% d'encert). Font real o es deixa buit — el joc gestiona bé les cançons sense any.
6. **La quarantena és definitiva**: cap cançó del full `BROSSA_quarantena` (a `bases/_arxiu/`)
   torna al catàleg sense decisió explícita de l'usuari.
7. **Supabase**: les claus anon són públiques per disseny; cap secret nou al repo (és públic).
   Els agents només fan `SELECT` a les taules de telemetria; res d'escriptures ni DDL.
8. **Res de dependències noves al joc**: és un `index.html` autònom (vanilla JS). Les eines
   de `tools/` són Python 3 + openpyxl.

## On és cada cosa

| Què | On |
| --- | --- |
| Joc (tot) | `index.html` (~350 KB, arrays `SONGS_CA/ES/EU/INT` inclosos) |
| Full mestre del catàleg | `bases/canconet_master.xlsx` (carpeta germana, NO al repo) |
| Mirall del catàleg en text | `data/songs_*.csv` (al repo — les cerques ràpides, aquí) |
| Eines del pipeline | `tools/` (`build_songs.py`, `find_dzids.py`, `songlib.py`) |
| Agents i skills | `.claude/agents/`, `.claude/skills/` |
| Service worker / versió cache | `sw.js` (línia 1) |

## Entorn local (Windows)

- Python: `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` si no és al PATH.
- GitHub CLI: `%ProgramFiles%\GitHub CLI\gh.exe` (autenticat com a kinblay).
- Node: `%ProgramFiles%\nodejs` (només el fa servir la landing, repo a part).

## El pipeline de cançons noves

`/nova-canco` orquestra: recepcio-canco → analista-deezer → [confirmació humana] →
curador-cataleg → validador → brainstorm-propostes → [l'usuari tria] → publicador → PR.
Detall a `.claude/skills/nova-canco/SKILL.md`.
