#!/usr/bin/env python3
"""A new mod from the skeleton, with the names of STANDARDS.md filled in.

    python3 new-mod.py "World Radio" [--initials wr]

Creates ../<mod-name>/ beside this repository (World Radio -> world-radio, mod id worldradio, class WorldRadio) and
its README from README-TEMPLATE.md. Then: write the description in fabric.mod.json, draw icon.png, colour
textures/item/guide_book.png (vanilla's book, see STANDARDS.md and make-book-texture.py), give the book its colours and
its recipe a typical ingredient, fill in the README.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BINARY = {'.png', '.jar'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('name', help='display name, e.g. "World Radio"')
    parser.add_argument('--initials', help='prefix of the publishing properties; default: the words\' first letters')
    args = parser.parse_args()
    words = re.findall(r'[A-Za-z0-9]+', args.name)
    names = {
        '__MOD_NAME__': args.name,
        '__MOD_SLUG__': '-'.join(w.lower() for w in words),
        '__MODID__': ''.join(w.lower() for w in words),
        '__CLASS__': ''.join(w[0].upper() + w[1:] for w in words),
        '__INITIALS__': args.initials or ''.join(w[0].lower() for w in words),
    }
    target = ROOT.parent / names['__MOD_SLUG__']
    if target.exists():
        sys.exit('%s exists already' % target)

    def filled(text: str) -> str:
        for placeholder, value in names.items():
            text = text.replace(placeholder, value)
        return text

    for source in sorted((ROOT / 'skeleton').rglob('*')):
        out = target / filled(str(source.relative_to(ROOT / 'skeleton')))
        if source.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix in BINARY:
            shutil.copy2(source, out)
        else:
            out.write_bytes(filled(source.read_text(encoding='utf-8')).encode('utf-8'))
            shutil.copymode(source, out)
    readme = (ROOT / 'README-TEMPLATE.md').read_text(encoding='utf-8')
    readme = readme.replace('{Mod Name}', args.name).replace('{modid}', names['__MODID__']) \
        .replace('{mod-name}', names['__MOD_SLUG__'])
    (target / 'README.md').write_text(readme, encoding='utf-8', newline='\n')
    print('%s: mod id %s, class %s, publishing properties %s.*' % (target, names['__MODID__'], names['__CLASS__'],
                                                                 names['__INITIALS__']))


if __name__ == '__main__':
    main()
