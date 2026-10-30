#!/usr/bin/env python3
"""Import only the Pokémon Showdown sprite sets needed by this project.

This intentionally does NOT download sprites.zip. It reads the public Showdown
HTML directory indexes and downloads only selected files.

Examples:
  python3 tools/import_showdown_sprites.py --dry-run
  python3 tools/import_showdown_sprites.py
  python3 tools/import_showdown_sprites.py --sets dex dex-shiny gen5-back gen5-back-shiny

Output:
  assets/showdown/<set>/...

The files are third-party/copyrighted sprite assets and are therefore not
committed automatically by this tool.
"""
from __future__ import annotations

import argparse
import html.parser
import os
import re
import ssl
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://play.pokemonshowdown.com/sprites/"
DEFAULT_SETS = ("dex", "dex-shiny", "gen5-back", "gen5-back-shiny")
ICON_FILE = "pokemonicons-sheet.png"


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        for key, value in attrs:
            if key == "href" and value:
                self.hrefs.append(value)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "pokeheartgold-android sprite importer"})
    with urllib.request.urlopen(req, context=ssl.create_default_context()) as r:
        return r.read().decode("utf-8", errors="replace")


def list_files(sprite_set: str) -> list[str]:
    parser = LinkParser()
    parser.feed(fetch_text(BASE + sprite_set + "/"))
    names = []
    for href in parser.hrefs:
        name = href.rsplit("/", 1)[-1]
        if not name or name in ("..", ".") or "?" in name:
            continue
        if not re.search(r"\.(?:gif|png|webp)$", name, re.I):
            continue
        names.append(name)
    return sorted(set(names))


def download(url: str, destination: Path, dry_run: bool) -> None:
    if dry_run:
        print("WOULD DOWNLOAD", url, "->", destination.relative_to(ROOT))
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "pokeheartgold-android sprite importer"})
    with urllib.request.urlopen(req, context=ssl.create_default_context()) as r:
        destination.write_bytes(r.read())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", nargs="+", default=list(DEFAULT_SETS))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--icons", action="store_true", default=True)
    args = ap.parse_args()

    total = 0
    for sprite_set in args.sets:
        files = list_files(sprite_set)
        print(f"{sprite_set}: {len(files)} sprite files found")
        for name in files:
            download(BASE + sprite_set + "/" + name,
                     ROOT / "assets" / "showdown" / sprite_set / name,
                     args.dry_run)
            total += 1

    if args.icons:
        download(BASE + ICON_FILE,
                 ROOT / "assets" / "showdown" / ICON_FILE,
                 args.dry_run)
        total += 1

    print(f"Total selected files: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
