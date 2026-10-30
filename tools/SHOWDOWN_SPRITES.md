# Pokémon Showdown sprites

The project uses a selective importer instead of the ~800 MB `sprites.zip` package.

## Import

From the repository root:

```sh
python3 tools/import_showdown_sprites.py --dry-run
python3 tools/import_showdown_sprites.py
```

Default sets:

- `dex` — current National Dex front sprites
- `dex-shiny` — current National Dex shiny front sprites
- `gen5-back` — static back sprites
- `gen5-back-shiny` — static shiny back sprites
- `pokemonicons-sheet.png` — current Pokémon icons

To select different sets:

```sh
python3 tools/import_showdown_sprites.py --sets gen5 gen5-shiny gen5-back gen5-back-shiny
```

The importer downloads only files actually present in the selected Showdown
folders and places them under `assets/showdown/`.

The sprite source is the Pokémon Showdown/Smogon sprite project. The source
repository states that its code is MIT-licensed, while the sprites themselves
have separate rights. Keep the imported sprite files out of commits/releases
unless you have the necessary rights to redistribute them.
