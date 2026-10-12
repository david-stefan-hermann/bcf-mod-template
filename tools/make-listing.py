#!/usr/bin/env python3
"""The Modrinth and CurseForge description of a mod, made from its README.

    python3 make-listing.py <mod folder> [--branch 26.2] [--modrinth]

Writes <mod folder>/docs/listing.md: the README without what only makes sense on GitHub.
- Everything between <!-- listing:skip --> and <!-- listing:end --> is left out, and so are the logo (the platforms
  show the icon themselves) and the section "Building"; "Source" with a link to the repository goes in before
  "Credits" and "License".
- <img> tags become Markdown pictures; pictures and links into the repository become absolute, so they work outside
  GitHub; links to a heading of the page lose the link and keep their text.
The repository is contact.sources of fabric.mod.json, the branch the one checked out unless --branch names it.

--modrinth also sends the text to the mod's Modrinth page. Token and project id are the mod's publishing properties
in ~/.gradle/gradle.properties (<initials>.modrinth.token / .projectId, the names its build.gradle uses). CurseForge
has no interface for the description: paste docs/listing.md into its editor.
"""
import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path


def repository(mod: Path) -> str:
    meta = json.loads((mod / 'src/main/resources/fabric.mod.json').read_text(encoding='utf-8'))
    url = meta.get('contact', {}).get('sources')
    if not url:
        sys.exit('fabric.mod.json has no contact.sources: the listing needs the repository address')
    return url.rstrip('/')


def branch(mod: Path) -> str:
    return subprocess.run(['git', '-C', str(mod), 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True,
                          text=True, check=True).stdout.strip()


def without_section(text: str, heading: str, replacement: str) -> str:
    """Replaces the section "## <heading>" up to the next "## " or the end."""
    return re.sub(r'^## ' + re.escape(heading) + r'\n.*?(?=^## |\Z)', replacement, text, flags=re.S | re.M)


def listing(readme: str, repo: str, branch_name: str) -> str:
    raw = repo.replace('https://github.com/', 'https://raw.githubusercontent.com/') + '/' + branch_name + '/'
    text = re.sub(r'<!-- listing:skip -->.*?<!-- listing:end -->\n?', '', readme, flags=re.S)
    text = re.sub(r'^<img [^>]*icon\.png[^>]*>\n\n?', '', text, flags=re.M)
    text = re.sub(r'<img [^>]*?src="([^"]+)"[^>]*?alt="([^"]*)"[^>]*>', r'![\2](\1)', text)
    text = re.sub(r'^<br clear="[a-z]+">\n\n?', '', text, flags=re.M)
    text = without_section(text, 'Building', '')
    source = '## Source\n\nSource and issues: ' + repo + '\n\n'
    closing = re.search(r'^## (Credits|License)\n', text, flags=re.M)
    text = text[:closing.start()] + source + text[closing.start():] if closing else text.rstrip() + '\n\n' + source

    def link(match: re.Match) -> str:
        bang, label, target = match.groups()
        if re.match(r'[a-z]+:', target):
            return match.group(0)
        if target.startswith('#'):
            return label
        if bang:
            return '![%s](%s%s)' % (label, raw, target)
        if target.startswith('../../'):  # GitHub's own pages of the repository, e.g. ../../releases
            return '[%s](%s/%s)' % (label, repo, target[6:])
        return '[%s](%s/blob/%s/%s)' % (label, repo, branch_name, target)

    text = re.sub(r'(!?)\[([^\]]*)\]\(([^)\s]+)\)', link, text)
    return re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'


def relative_targets(text: str) -> list:
    return [t for t in re.findall(r'\]\(([^)\s]+)\)', text) + re.findall(r'src="([^"]+)"', text)
            if not re.match(r'[a-z]+:', t)]


def send_to_modrinth(mod: Path, text: str) -> None:
    prefix = re.search(r"'(\w+)\.modrinth\.projectId'", (mod / 'build.gradle').read_text(encoding='utf-8'))
    if not prefix:
        sys.exit('build.gradle names no <initials>.modrinth.projectId')
    properties = {}
    for line in (Path.home() / '.gradle/gradle.properties').read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            properties[key.strip()] = value.strip()
    token = properties[prefix.group(1) + '.modrinth.token']
    project = properties[prefix.group(1) + '.modrinth.projectId']
    request = urllib.request.Request('https://api.modrinth.com/v2/project/' + project, method='PATCH',
                                     data=json.dumps({'body': text}).encode('utf-8'),
                                     headers={'Authorization': token, 'Content-Type': 'application/json',
                                              'User-Agent': 'BaconCakeFactory/bcf-mod-template'})
    with urllib.request.urlopen(request) as response:
        print('Modrinth: HTTP', response.status)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('mod', type=Path)
    parser.add_argument('--branch')
    parser.add_argument('--modrinth', action='store_true')
    args = parser.parse_args()
    repo = repository(args.mod)
    text = listing((args.mod / 'README.md').read_text(encoding='utf-8'), repo, args.branch or branch(args.mod))
    left = relative_targets(text)
    if left:
        sys.exit('still relative: ' + ', '.join(left))
    out = args.mod / 'docs/listing.md'
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding='utf-8', newline='\n')
    print('%s: %d lines, %d pictures' % (out, text.count('\n'), text.count('![')))
    if args.modrinth:
        send_to_modrinth(args.mod, text)


if __name__ == '__main__':
    main()
