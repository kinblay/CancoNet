# -*- coding: utf-8 -*-
"""
songlib — utilitats compartides per llegir i escriure el cataleg de cancons
de CancoNet que viu dins d'index.html.

No depen de res extern (nomes la biblioteca estandard). openpyxl nomes cal
als scripts que toquen Excel.
"""
import io
import os
import re
import unicodedata

# Ordre en que s'escriuen els camps a index.html (l'ordre historic del fitxer).
FIELD_ORDER = ["id", "dzId", "t", "a", "y", "g", "ai", "dec", "st"]

# Camps morts que ja no s'escriuen mai (vegeu README de tools/).
DEAD_FIELDS = ("seg", "ytId")

LANGS = ["CA", "ES", "EU", "INT"]
ARRAY_OF = {"CA": "SONGS_CA", "ES": "SONGS_ES", "EU": "SONGS_EU", "INT": "SONGS_INT"}


# ---------------------------------------------------------------- rutes

def repo_root():
    """Arrel del repo del joc (la carpeta pare de tools/)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index_path():
    return os.path.join(repo_root(), "index.html")


def bases_dir():
    """Carpeta bases/ del projecte (fora del repo git)."""
    return os.path.join(os.path.dirname(repo_root()), "bases")


def master_path():
    return os.path.join(bases_dir(), "canconet_master.xlsx")


def find_base_file(name):
    """Busca un Excel a bases/ i, si no hi es, a bases/_arxiu/.

    Aixi els fitxers historics es poden arxivar sense trencar les eines.
    Retorna None si no hi es enlloc.
    """
    for folder in (bases_dir(), os.path.join(bases_dir(), "_arxiu")):
        candidate = os.path.join(folder, name)
        if os.path.exists(candidate):
            return candidate
    return None


def read_index():
    with io.open(index_path(), encoding="utf-8") as handle:
        return handle.read()


def write_index(text):
    with io.open(index_path(), "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


# ------------------------------------------------- localitzar els arrays

def find_array(src, name):
    """Retorna (inici, fi) del literal [...] de `const NAME=[...]`.

    `inici` apunta al '[' i `fi` al ']' (inclos), emparellant claudators i
    respectant les cadenes de text.
    """
    marker = src.find(name + "=[")
    if marker < 0:
        marker = src.find(name + " = [")
    if marker < 0:
        raise ValueError("no trobo l'array " + name + " a index.html")
    start = src.find("[", marker)
    depth = 0
    in_str = False
    pos = start
    while pos < len(src):
        ch = src[pos]
        if in_str:
            if ch == "\\":
                pos += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return start, pos
        pos += 1
    raise ValueError("array " + name + " mal tancat")


def split_objects(array_text):
    """Talla `[{...},{...}]` en la llista de textos interiors de cada objecte."""
    out = []
    depth = 0
    in_str = False
    begin = None
    pos = 0
    while pos < len(array_text):
        ch = array_text[pos]
        if in_str:
            if ch == "\\":
                pos += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                begin = pos
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(array_text[begin + 1:pos])
        pos += 1
    return out


def parse_object(body):
    """Converteix el cos d'un objecte JS pla en un dict de Python.

    Els valors imbricats (com `seg:{...}`) es guarden com a text cru; no els
    fem servir enlloc pero aixi no es perden si algu els vol inspeccionar.
    """
    out = {}
    pos = 0
    size = len(body)
    while pos < size:
        colon = body.find(":", pos)
        if colon < 0:
            break
        key = body[pos:colon].strip().strip('"')
        pos = colon + 1
        while pos < size and body[pos] == " ":
            pos += 1
        if pos >= size:
            break
        if body[pos] == '"':
            pos += 1
            buf = []
            while pos < size:
                if body[pos] == "\\":
                    buf.append(body[pos + 1])
                    pos += 2
                    continue
                if body[pos] == '"':
                    break
                buf.append(body[pos])
                pos += 1
            out[key] = "".join(buf)
            pos += 1
        elif body[pos] == "{":
            depth = 0
            begin = pos
            while pos < size:
                if body[pos] == "{":
                    depth += 1
                elif body[pos] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                pos += 1
            out[key] = body[begin:pos + 1]
            pos += 1
        else:
            begin = pos
            while pos < size and body[pos] != ",":
                pos += 1
            raw = body[begin:pos].strip()
            if re.match(r"^-?\d+$", raw):
                out[key] = int(raw)
            elif raw in ("true", "false"):
                out[key] = raw == "true"
            else:
                out[key] = raw
        while pos < size and body[pos] in ", ":
            pos += 1
    return out


def load_songs(src=None):
    """Llegeix index.html i retorna {lang: [dict, ...]} amb l'ordre original."""
    src = src if src is not None else read_index()
    out = {}
    for lang in LANGS:
        start, end = find_array(src, ARRAY_OF[lang])
        out[lang] = [parse_object(body) for body in split_objects(src[start:end + 1])]
    return out


# ------------------------------------------------------------- escriure

def js_string(value):
    text = "" if value is None else str(value)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    text = text.replace("\r", "").replace("\n", " ")
    return '"' + text + '"'


def emit_object(song):
    """Genera el text JS d'una cano, en l'ordre historic i sense camps morts."""
    parts = []
    for key in FIELD_ORDER:
        val = song.get(key)
        if val is None or val == "":
            continue
        if key in ("id", "dzId", "y"):
            parts.append("%s:%d" % (key, int(val)))
        else:
            parts.append("%s:%s" % (key, js_string(val)))
    return "{" + ",".join(parts) + "}"


def emit_array(songs):
    return "[\n" + ",\n".join(emit_object(song) for song in songs) + "\n]"


def replace_arrays(src, songs_by_lang):
    """Torna index.html amb els arrays SONGS_* substituits. No toca res mes.

    Se substitueixen de darrere cap endavant perque els indexs no es moguin.
    """
    spans = []
    for lang in LANGS:
        start, end = find_array(src, ARRAY_OF[lang])
        spans.append((start, end, lang))
    for start, end, lang in sorted(spans, reverse=True):
        src = src[:start] + emit_array(songs_by_lang[lang]) + src[end + 1:]
    return src


# -------------------------------------------------------------- ajudes

def norm(text):
    """Minuscules sense accents ni signes: per comparar titols i artistes."""
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join("".join(ch if ch.isalnum() else " " for ch in text).split())


def decade_label(year):
    """Etiqueta de decada unificada. Nomes es text de pista (`hD`), mai es compara."""
    try:
        year = int(year)
    except (TypeError, ValueError):
        return ""
    if year < 1960:
        return "anys 50"
    base = (year // 10) * 10
    if base < 2000:
        return "anys %d" % (base - 1900)
    return "anys %d" % base


def clean_int(value):
    try:
        num = int(str(value).strip())
        return num if num > 0 else None
    except (TypeError, ValueError):
        return None
