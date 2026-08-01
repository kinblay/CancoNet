---
name: informe-cataleg
description: Radiografia de l'estat del cataleg de cancons - recomptes per idioma, pendents de dzId, cancons sense any o estil, i proposta priortizada de que completar. Invoca-la quan l'usuari pregunti com esta el cataleg o que falta per fer.
---

# /informe-cataleg — com està el catàleg

Fonts: `data/songs_*.csv` (estat del joc), `bases/canconet_master.xlsx` (full `PENDENTS_DZID`) i `python tools/build_songs.py --check` (validació en viu).

Construeix l'informe amb:

1. **Recomptes**: cançons per idioma i total; quantes són jugables (dzId).
2. **Forats**: sense any (i per tant sense pregunta d'any ni bonus dècada), sense `st` (invisibles al filtre del mode lliure) — llista curta amb les més rellevants.
3. **PENDENTS_DZID**: quantes esperen validació humana, les 5 amb més confiança (dzId proposat + % + què diu Deezer) com a "victòries fàcils".
4. **Qualitat**: avisos del `--check`, duplicats potencials, cançons marcades amb dubtes a `Notes` (p. ex. versions en castellà detectades per l'analista).
5. **Proposta priorizada**: 3-5 accions concretes ordenades per impacte/esforç ("validar aquests 5 dzId = +5 cançons jugables en 10 minuts").

Format: titulars primer, taules després, proposta al final. En català, curt.
