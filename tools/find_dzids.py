# -*- coding: utf-8 -*-
"""
find_dzids — busca a l'API publica de Deezer els identificadors que falten.

Us:
    python tools/find_dzids.py                # busca les pendents del full CA de r7
    python tools/find_dzids.py --limit 10     # nomes les 10 primeres (proves)

Escriu les propostes a tools/dzid_proposals.json. NO toca mai el cataleg:
les propostes les valida una persona des del full PENDENTS_DZID del master.

Fa servir els titols amb accents i apostrofs tal com estan al full, que es el
que dona millors resultats a Deezer.
"""
import argparse
import difflib
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import songlib

API = "https://api.deezer.com/"
UA = {"User-Agent": "canconet-dzid-finder/1.0"}

# Llindars de confianca: per sobre d'ALTA es pot aplicar sense mirar-ho;
# entre DUBTE i ALTA cal validacio humana; per sota es descarta.
ALTA = 0.86
DUBTE = 0.62


def api_get(path):
    request = urllib.request.Request(API + path, headers=UA)
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.loads(response.read().decode("utf-8", "replace"))


def search(query, limit=8):
    try:
        return api_get("search?limit=%d&q=%s" % (limit, urllib.parse.quote(query))).get("data", [])
    except Exception:
        return []


_catalog_cache = {}


def artist_catalog(artist):
    """Totes les pistes que Deezer associa a un artista (cerca estricta + top)."""
    if artist in _catalog_cache:
        return _catalog_cache[artist]
    tracks = search('artist:"%s"' % artist, limit=100)
    time.sleep(0.25)
    found = search(artist, limit=1)
    if found:
        artist_id = (found[0].get("artist") or {}).get("id")
        if artist_id:
            time.sleep(0.25)
            try:
                tracks += api_get("artist/%s/top?limit=100" % artist_id).get("data", [])
            except Exception:
                pass
    _catalog_cache[artist] = tracks
    return tracks


def score_hit(artist, title, hit):
    hit_artist = ((hit.get("artist") or {}).get("name")) or ""
    ratio_artist = difflib.SequenceMatcher(None, songlib.norm(artist), songlib.norm(hit_artist)).ratio()
    ratio_title = difflib.SequenceMatcher(None, songlib.norm(title), songlib.norm(hit.get("title"))).ratio()
    return (ratio_artist * 0.45) + (ratio_title * 0.55)


def best_match(artist, title):
    """Dues passades: cerca directa i, si no convenc, el cataleg de l'artista."""
    best, score = None, 0.0
    for hit in search("%s %s" % (artist, title)):
        value = score_hit(artist, title, hit)
        if value > score:
            best, score = hit, value
    if score < ALTA:
        for hit in artist_catalog(artist):
            value = score_hit(artist, title, hit)
            if value > score:
                best, score = hit, value
    return best, score


def pending_rows():
    """Files del full CA de r7 que encara no tenen dzId."""
    import openpyxl
    source = songlib.find_base_file("canconet_base_idiomes_r7.xlsx")
    book = openpyxl.load_workbook(source, read_only=True, data_only=True)
    rows = []
    for row in book["CA"].iter_rows(min_row=2, values_only=True):
        if row and any(cell is not None for cell in row) and songlib.clean_int(row[0]) is None:
            rows.append({"artista": row[1], "canco": row[2], "any": row[3], "estil": row[4]})
    book.close()
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="nomes N files (proves)")
    args = parser.parse_args()

    rows = pending_rows()
    if args.limit:
        rows = rows[:args.limit]
    print("cancons pendents de dzId:", len(rows))

    proposals = []
    for row in rows:
        artist, title = row["artista"], row["canco"]
        hit, score = best_match(artist, title)
        if hit and score >= ALTA:
            estat = "ALTA"
        elif hit and score >= DUBTE:
            estat = "DUBTE"
        else:
            estat = "NO TROBAT"
        proposals.append({
            "artista": artist,
            "canco": title,
            "any": row["any"],
            "estil": row["estil"],
            "estat": estat,
            "confianca": round(score * 100),
            "dzId": (hit or {}).get("id") if estat != "NO TROBAT" else None,
            "deezer_artista": ((hit or {}).get("artist") or {}).get("name") if hit else None,
            "deezer_titol": (hit or {}).get("title") if hit else None,
        })
        print("  %-9s %3d%%  %-24s %-30s %s" % (
            estat, round(score * 100), str(artist)[:24], str(title)[:30],
            (hit or {}).get("id") or ""))
        time.sleep(0.2)

    destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dzid_proposals.json")
    with io.open(destination, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(proposals, ensure_ascii=False, indent=1))

    counts = {}
    for item in proposals:
        counts[item["estat"]] = counts.get(item["estat"], 0) + 1
    print("")
    print("resum:", counts)
    print("escrit a", destination)


if __name__ == "__main__":
    main()
