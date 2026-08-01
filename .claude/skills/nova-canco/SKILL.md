---
name: nova-canco
description: Pipeline complet per afegir cançons noves a CançoNet. Donada una o més cançons ("Artista - Títol"), orquestra els agents especialitzats per ordre - recepció, anàlisi Deezer, curació, validació, brainstorm de publicació i publicador - amb els punts de control humans. Invoca-la quan l'usuari vulgui afegir cançons al joc.
---

# /nova-canco — afegir cançons al catàleg

Ets l'orquestrador. NO facis la feina tu: delega cada pas al seu agent i vigila els punts de control. Si l'usuari passa diverses cançons, processa-les en lot (cada pas per a totes, no el pipeline sencer per a cadascuna).

## Pipeline

1. **recepcio-canco** — passa-li la llista tal qual. Les REBUTJADES/JA EXISTENTS es reporten i cauen. Els DUBTES es pregunten a l'usuari ara.
2. **analista-deezer** — per a les acceptades. Les que surtin DUBTE o NO TROBAT van al full `PENDENTS_DZID` (que ho anoti el curador) i es reporten: NO segueixen el pipeline.
3. **⛔ PUNT DE CONTROL HUMÀ** — mostra a l'usuari la taula: cançó, dzId, confiança, avisos (versió castellana? live?). Que confirmi abans d'escriure res al màster.
4. **curador-cataleg** — escriu les confirmades al màster (metadades + any amb fonts).
5. **validador** — checklist complet. Si NO APTE: reporta, desfés si cal, i atura.
6. **brainstorm-propostes** — SEMPRE abans de publicar: opcions de com empaquetar-ho (un PR, agrupar amb altres pendents, missatge de versió...). Presenta-les a l'usuari.
7. **⛔ PUNT DE CONTROL HUMÀ** — l'usuari tria opció.
8. **publicador** — executa l'opció triada i retorna l'URL del PR.

## Recorda

- El merge del PR el fa SEMPRE l'usuari a GitHub. El pipeline acaba a l'URL del PR.
- Si alguna cosa falla a mig camí, deixa-ho tot en un estat net (res a mig escriure al màster) i explica on ha quedat.
- Resum final: taula de cançons afegides / pendents / rebutjades + enllaç al PR.
