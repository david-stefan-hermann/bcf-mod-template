#!/usr/bin/env python3
"""The guide book's item texture: vanilla's book with its leather in one colour.

    python3 make-book-texture.py <mod folder> <#rrggbb> [--jar <minecraft-client.jar>]

Writes <mod folder>/src/main/resources/assets/<modid>/textures/item/guide_book.png (the mod id from fabric.mod.json).
Vanilla's book keeps its shape and shading; only the leather (cover, spine, back) takes the colour, the pages stay
grey. This is the starting point every mod's book shares: a mod then puts its own mark on the cover (Dyed Resin's
clump, Greek Trees' leaf) or paints the leather in its own pattern (Capture Eggs' book in the egg's colours), in its own
tools script. Never the flat book of earlier skeletons.
"""
import argparse
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

JAR = Path.home() / '.gradle/caches/fabric-loom/26.2/minecraft-client.jar'
MAIN_RED = 0x65  # the red of the vanilla cover's main brown, the colour the given one replaces


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('mod', type=Path, help='the mod folder')
    parser.add_argument('colour', help='the leather colour, e.g. "#1f6b63"')
    parser.add_argument('--jar', type=Path, default=JAR, help='a Minecraft client jar (default: Loom\'s for 26.2)')
    args = parser.parse_args()
    colour = tuple(int(args.colour.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    mod_id = json.loads((args.mod / 'src/main/resources/fabric.mod.json').read_text(encoding='utf-8'))['id']
    with zipfile.ZipFile(args.jar) as jar:
        book = Image.open(io.BytesIO(jar.read('assets/minecraft/textures/item/book.png'))).convert('RGBA')
    pixels = []
    for r, g, b, a in book.getdata():
        if a and max(r, g, b) - min(r, g, b) >= 16:  # the leather; the pages are grey
            f = r / MAIN_RED
            r, g, b = (min(255, round(c * f)) for c in colour)
        pixels.append((r, g, b, a))
    book.putdata(pixels)
    out = args.mod / 'src/main/resources/assets' / mod_id / 'textures/item/guide_book.png'
    book.save(out)
    print(out)


if __name__ == '__main__':
    main()
