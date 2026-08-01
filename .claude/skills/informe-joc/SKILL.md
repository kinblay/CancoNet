---
name: informe-joc
description: Informe de com es juga de veritat a canconet.net - cancons mes fallades, retencio, abandonament, modes mes jugats - a partir de la telemetria de Supabase. Invoca-la quan l'usuari vulgui saber com va el joc o decidir si escalar el projecte.
---

# /informe-joc — què diuen les dades

Delega l'anàlisi a l'agent **telemetria** (només lectura sobre Supabase) i demana-li el paquet estàndard:

1. Salut general: partides i jugadors únics (14 dies), tendència.
2. Cançons més difícils i més fàcils (creuades amb títol/artista des de `data/*.csv`).
3. On s'abandona (per nivell) i % de compleció per mode.
4. Modes i idiomes: què es juga i què no.

Presenta a l'usuari els titulars accionables primer i tanca SEMPRE amb un bloc de **decisions suggerides** (p. ex.: "aquestes 3 cançons fallen massa → revisar-les amb el curador", "ningú juga el mode X → repensar-lo o treure'l del menú").

Context important: la telemetria es va activar el juliol de 2026 — amb poc volum, marca les conclusions com a provisionals. Si les taules són buides, l'informe és exactament això: "encara no hi ha dades; les cachés dels jugadors s'estan actualitzant" (no cal inventar res).
