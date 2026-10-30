#!/usr/bin/env python3
"""Audit the asset baseline for the expanded HeartGold project.

This script only inventories files already present in the checkout. It does not
download or redistribute game assets.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POKEGRA = ROOT / "files/poketool/pokegra/pokegra"
ITEM_ICONS = ROOT / "files/itemtool/itemdata/item_icon"
ITEM_DATA = ROOT / "files/itemtool/itemdata/item_data.csv"
REPORT = ROOT / "assets/catalog/asset-audit.json"


def main() -> int:
    present: dict[int, dict[str, list[str]]] = {}
    if POKEGRA.exists():
        for path in POKEGRA.glob("[0-9][0-9][0-9][0-9]/**/*"):
            if not path.is_file() or path.suffix.lower() != ".png":
                continue
            match = re.search(r"/(\d{4})/", path.as_posix())
            if not match:
                continue
            species_id = int(match.group(1))
            rel = path.relative_to(ROOT).as_posix()
            slot = "back" if "back" in path.parts else "front" if "front" in path.parts else "other"
            present.setdefault(species_id, {}).setdefault(slot, []).append(rel)

    valid_species = sorted(i for i in present if 1 <= i <= 493)
    missing_hgss_ids = [i for i in range(1, 494) if i not in present]
    item_icon_files = sorted(
        p.relative_to(ROOT).as_posix()
        for p in ITEM_ICONS.glob("*")
        if p.is_file() and p.suffix.upper() in {".NCGR", ".NCLR", ".NCER", ".NANR"}
    ) if ITEM_ICONS.exists() else []

    report = {
        "scope": "local checkout inventory only; not a complete asset compatibility test",
        "pokemon": {
            "target_species": 1025,
            "species_with_existing_hgss_sprite_folders": len(valid_species),
            "existing_species_ids": valid_species,
            "missing_species_ids_1_to_493": missing_hgss_ids,
            "species_494_to_1025_to_import": list(range(494, 1026)),
            "sprite_files_by_species": present,
        },
        "items": {
            "item_data_csv_present": ITEM_DATA.exists(),
            "existing_item_icon_resource_file_count": len(item_icon_files),
            "icon_resource_files": item_icon_files,
            "note": "HGSS item icons are Nitro graphics resources, not ready-to-use PNGs.",
        },
        "berries": {
            "note": "No standalone berry image directory was detected by this audit. Berry data/graphics must be mapped from existing HGSS resources or sourced as a separate compatible icon set."
        },
        "next_assets_to_map": [
            "Pokémon front/back normal and shiny sprites for species 494-1025 and alternate forms",
            "Pokémon party/box icons for all species and forms",
            "item icons and item metadata beyond the HGSS item table",
            "berry icons and berry metadata",
            "type icons, status icons, move-category icons, and any required UI assets",
        ],
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Pokémon species folders found: {len(valid_species)} / 493")
    print(f"Missing HGSS species IDs: {len(missing_hgss_ids)}")
    print(f"Item graphics resource files found: {len(item_icon_files)}")
    print(f"Report written to {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
