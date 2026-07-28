# CançoNet — Manual de marca

Valores extraídos de `index.html` (`:root`) y `manifest.json`.
**Si cambias un token en el código, actualiza este archivo** para que las publicaciones no se desincronicen de la app.

---

## 1. La marca en una frase

Un joc de nit: fondo azul-negro casi teatral, oro que hace de foco y un rojo que solo aparece cuando algo importa. El oro y el rojo son los de la senyera — la identidad es catalana sin decirlo. Morado, naranja y verde son **señales de estado**, no colores de marca.

---

## 2. Paleta

### Núcleo

| Token | Hex | Nombre | Uso |
|---|---|---|---|
| `--gold` | `#D4A017` | Or CançoNet | Primario. Logo "Cançó", puntuaciones, CTA. Texto negro encima. |
| `--red` | `#C1121F` | Roig | Acento. Logo "Net", badge de nivel, botón activo. Nunca fondo grande. |
| `--bg` | `#0d0d1a` | Nit | Fondo de todo. También `background_color` de la PWA. |
| `--card` | `#161e35` | Carta | Tarjetas, modales, toast. |
| `--text` | `#eee` | Text | Texto principal (blanco roto, no `#fff`). |
| `--muted` | `#778` | Muted | Subtítulos, etiquetas, metadatos. Gris azulado. |

### Señales de estado

| Token | Hex | Uso |
|---|---|---|
| `--ok` | `#4caf50` | Respuesta correcta |
| `--err` | `#f44336` | Fallo / tiempo agotado |
| `--purple` | `#7c3aed` | Ronda bonus, modo Autor, retos |
| — | `#f97316` | Exclusivo modo Copa |

### Apoyos (solo dentro de degradados y texto sobre color)

| Hex | Nombre | Dónde |
|---|---|---|
| `#f59e0b` | Ámbar | Fin del degradado dorado |
| `#a855f7` | Morado claro | Botones de ayuda, degradado morado |
| `#c084fc` | Lila | Texto sobre fondo morado |
| `#a78bfa` | Lavanda | Texto badges Autor / Repte |
| `#f87171` | Rojo claro | Texto badge modo Lliure |
| `#22c55e` | Verde subida | Flecha ▲ en el ranking |
| `#f43f5e` | Rosa bajada | Flecha ▼ en el ranking |
| `#94a3b8` | Pizarra | Texto secundario en pantallas de error |
| `#1a1a3e` | Nit alta | Centro del radial del splash |
| `#08080f` | Negre pur | Pantalla de reset / navegador incompatible |

---

## 3. Degradados (cinco, ni uno más)

```css
/* Or → Ámbar — el de marca */
linear-gradient(90deg,#D4A017,#f59e0b)

/* Porpra — Autor / Repte */
linear-gradient(135deg,#a855f7,#c084fc)

/* Copa */
linear-gradient(135deg,#f97316,#ea580c)

/* Splash — fondo de cualquier pieza gráfica */
radial-gradient(ellipse at center,#1a1a3e 0%,#0d0d1a 70%)

/* Senyera — solo en piezas de temática catalana */
linear-gradient(90deg,rgba(241,196,15,.18) 0%,rgba(231,76,60,.18) 50%,rgba(241,196,15,.18) 100%)
```

Carta oscura para tarjetas destacadas: `linear-gradient(135deg,#161e35,#0d0d1a)` con borde `1px solid rgba(212,160,23,.3)`.

---

## 4. Logo

Una palabra partida en dos colores: **Cançó** en oro `#D4A017` + **Net** en rojo `#C1121F`.

- Peso **900**, tracking negativo.
- Cuanto más grande, más negativo: 6.5rem → `-4px`; 3.5rem → `-2px`.
- Aire libre mínimo alrededor: la altura de la "C".
- Nunca todo del mismo color, ni con espacio entre las mitades, ni sin cedilla.

Grafías incorrectas: `Canconet`, `CanzoNet`, `Cançonet`, `CANÇONET`.

---

## 5. Tipografía

La web usa `system-ui, sans-serif` — sin fuente de pago ni CDN. Para piezas gráficas, el equivalente más fiel es **SF Pro / Segoe UI / Roboto**; si necesitas una descargable, **Inter Black (900)** mantiene el carácter.

El contraste de la marca es de **peso**, no de familia.

| Rol | Tamaño | Peso | Notas |
|---|---|---|---|
| Logo grande | 6.5rem | 900 | tracking `-4px` |
| Logo app | 3.5rem | 900 | tracking `-2px` |
| Título de pantalla | 1.5rem | 900 | — |
| Puntuación | 2.2–3.2rem | 900 | color oro |
| Etiqueta | .72rem | 700 | MAYÚS + `letter-spacing:1px` |
| Cuerpo | 1–1.05rem | 600 | — |
| Metadatos | .72–.88rem | 600 | color muted |

Solo las etiquetas pequeñas van en mayúsculas. Los títulos, nunca.

---

## 6. Formas

| Radio | Uso |
|---|---|
| `99px` | Píldoras: badges, barras de progreso, chips |
| `22px` | Tarjeta de modo (pantalla de idioma) |
| `14px` | Carta, botón principal, toast |
| `12px` | Input, zona, tabs |
| `10px` | Chip, hint box |
| `50%` | Botón de play, dots de progreso |

### Botones

| Clase | Fondo | Texto |
|---|---|---|
| `.btn-gold` | `#D4A017` | `#000` |
| `.btn-red` | `#C1121F` | `#fff` |
| `.btn-purple` | `#7c3aed` | `#fff` |
| `.btn-ghost` | `rgba(255,255,255,.07)` | `#eee` |
| `.btn-outline` | transparente, borde `#778` | `#778` |

**Un solo botón oro por pantalla** — es la acción principal.

### Badges de modo

Patrón fijo: fondo del color al 20–30 % de opacidad, texto en la versión clara de ese color.

| Modo | Fondo | Texto |
|---|---|---|
| Diària | `rgba(212,160,23,.2)` | `#D4A017` |
| Lliure | `rgba(193,18,31,.2)` | `#f87171` |
| Autor | `rgba(124,58,237,.3)` | `#a78bfa` |
| Copa | `rgba(249,115,22,.3)` | `#f97316` |
| Repte | `rgba(124,58,237,.2)` | `#a78bfa` |

---

## 7. Redes sociales

Fondo siempre el radial del splash. Oro solo en el dato que debe leerse primero — la puntuación **o** el logo, no ambos al mismo tamaño.

### Formatos que ya usa la app (cópialos tal cual)

Resultado diario:

```
🎵 CançoNet #142
🟩🟩🟨🟩⬛🟩
🏆 8.420 pts
🔥 Ratxa de 5
📅 #12 avui ▲3
📍 Girona
https://canconet.net
```

Reto:

```
⚔️ Repte CançoNet!
Marta: 9.100 pts
Jordi: 7.640 pts
🎵 https://canconet.net
```

### Vocabulario de emoji

`🎵 🎶 🎸 🎹 🎺 🏆 ⚔️ 🔥 📍 📅 🥇 🥈 🥉`

Notas musicales = marca · trofeo = puntuación · espadas = reto · llama = racha · chincheta = zona.
No hay set de iconografía propio y no hace falta inventarlo.

### Reglas

- Cierra siempre con `canconet.net` en línea propia.
- El idioma de la pieza sigue al idioma del modo: català (ca), español (es), inglés (eu / int).
- Formatos: 1:1 para feed, 9:16 para stories.

---

## 8. Sí y no

**Sí**
- Fondo oscuro siempre — la marca no tiene versión clara.
- Un único acento por pieza: oro *o* el color del modo.
- Texto negro sobre oro; blanco sobre rojo y morado.
- Números grandes en peso 900: la puntuación es el protagonista.
- Píldoras de 99px para etiquetas y estados.
- Marco senyera solo en piezas de temática catalana.

**No**
- Logo sobre foto sin capa oscura detrás.
- Oro sobre rojo o rojo sobre oro — no hay contraste.
- Morado o naranja como color de marca: pertenecen a un modo.
- Degradados nuevos fuera de los cinco de arriba.
- Fondo blanco o gris neutro.
- Serif, condensadas o manuscritas.

---

## 9. Ficha rápida

| Campo | Valor |
|---|---|
| Nombre | CançoNet |
| Dominio | canconet.net |
| Tagline (ca) | 🎵 Endevina la cançó |
| Descripción PWA | Endevina la cançó catalana |
| Theme color | `#D4A017` |
| Background color | `#0d0d1a` |
| Idiomas | català (ca) · español (es) · europe (eu) · international (int) |
