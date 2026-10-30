# Asset preparation plan

This phase prepares and audits assets before changing gameplay code.

## Existing content discovered in this repository

- HGSS Pokémon graphics are under `files/poketool/pokegra/pokegra/`.
  The current tree contains numbered graphics folders through National Dex
  #493. These are game-native Nitro resources and include front/back artwork.
- Item metadata and icon resources are under
  `files/itemtool/itemdata/`, including `item_data.csv` and the
  `item_icon/` Nitro graphics resource set.
- The existing berry gameplay code is present in `src/berry_*.c` and
  `include/berry_*.h`; the inventory did not find a standalone berry image
  directory.

## Target asset scope

1. Pokémon #001–#1025, including alternate/regional forms where applicable:
   front/back, normal/shiny, party/box icons, and form identifiers.
2. Items: metadata plus inventory/menu icons for every item in the target data set.
3. Berries: metadata, berry plant/field graphics where needed, and bag icons.
4. Battle/UI: type, status, move-category, ability and other interface icons
   only where the game actually displays them.
5. Preserve existing HGSS-native resources when they remain suitable. Do not
   replace the original graphics wholesale with unrelated modern artwork.

## Import policy

- Never download a full sprite archive.
- Use an explicit allowlist/manifest and deduplicate by stable species/form/item ID.
- Keep source, license/attribution, dimensions, and destination path in the catalog.
- Do not commit ROM-derived assets or third-party artwork automatically.
- Run the inventory script after extracting the user's own legally obtained ROM
  assets: `python3 tools/asset_inventory.py`.

## Current limitation

The previous Showdown importer enumerated every file in four broad directories.
That is too permissive for this project and should not be run again until it is
replaced with a manifest-driven importer. This plan deliberately records the
current baseline first; it does not claim that all 1,025 species or all modern
items have already been imported.
