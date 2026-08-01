---
name: build-canconet
description: Recepta segura per regenerar el joc des del full mestre i deixar-ho verificat - validacio, build, bump de sw.js i comprovacio al navegador. Invoca-la quan s'hagi editat bases/canconet_master.xlsx a ma i calgui portar els canvis al joc.
---

# /build-canconet — del màster al joc, sense sorpreses

Seqüència fixa. Python: si no és al PATH, `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`.

1. `python tools/build_songs.py --check`
   - Errors > 0 → ATURA'T, mostra'ls i proposa com arreglar-los al màster. No continuïs.
2. `python tools/build_songs.py` (escriu `index.html` + `data/*.csv`).
3. Compara recomptes abans/després per idioma. Qualsevol pèrdua no explicada → alerta vermella i atura.
4. Delega al **validador** la comprovació al navegador (consola neta, menú, una cançó sona).
5. Recorda el **bump de `sw.js`** (`canconet-vNN` → `vNN+1`): els canvis de catàleg SÍ afecten el jugador → sempre bump.
6. Per publicar: brainstorm d'opcions si hi ha res a decidir → **publicador** (branca + PR). El merge, l'usuari.

Sortida: resum amb recomptes, veredicte del validador i, si s'ha publicat, l'URL del PR.
