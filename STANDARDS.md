# Standards for BaconCakeFactory's mods

These hold for every mod of ours. A new mod starts as `tools/new-mod.py "<Mod Name>"`, which fills them in; an
existing mod is brought in line with them at its next release. The examples are World Radio's.

## Names

Everything follows from the display name.

| What | Rule | Example |
|---|---|---|
| Display name | title case, with spaces | `World Radio` |
| Project folder, GitHub repository, Modrinth slug | kebab-case | `world-radio` |
| Mod id, `archives_base_name`, `rootProject.name`, Java package | lower case, no separators | `worldradio` |
| `maven_group` | `de.baconcakefactory.<modid>` | `de.baconcakefactory.worldradio` |
| Jar | `<modid>-<version>.jar` | `worldradio-2.2.0+26.2.jar` |
| Author (`fabric.mod.json`, `LICENSE`, git) | `BaconCakeFactory` | |
| License | MIT, file `LICENSE`, bundled as `LICENSE_<modid>` | |
| `contact.sources` | the GitHub repository | `https://github.com/david-stefan-hermann/world-radio` |
| Publishing properties | `<initials>.modrinth.token`, `.modrinth.projectId`, `.curseforge.token`, `.curseforge.projectId`, in `~/.gradle/gradle.properties` only | `wr.modrinth.token` |
| Guide book | item `guide_book`, texts `<modid>.book.<chapter>.<name>` | `worldradio.book.range.text` |

## Branches

- One branch per Minecraft version, named after it: `26.2`, `26.3`. There is no `main`.
- The default branch is the newest Minecraft version the mod supports.
- A port starts as a new branch from the newest one. A fix that older versions need is cherry-picked onto their
  branches.

## Versions and releases

- `mod_version=<semver>+<minecraft version>`, e.g. `2.2.0+26.2`. The same `<semver>` on two branches is the same
  state of the mod for two Minecraft versions.
- `CHANGELOG.md`: `# Changelog`, then one `## <semver>` section per release, newest first, bullets, the names of
  features in bold. No dates. `./gradlew publishMods` uploads the top section as the release notes.
- The commit of a release: `<semver>: <summary>`. The first commit of a repository:
  `<Mod Name> <semver>: <summary>`. Other commits: a plain sentence, with `README:` or `docs:` in front where it
  fits.
- Tag: `v<semver>+<minecraft version>`, e.g. `v2.2.0+26.2`. Older tags without the Minecraft version stay as they
  are.
- GitHub release: title `<Mod Name> <semver> (Minecraft <minecraft version>)`, the changelog section as text, the
  jar attached.
- Nothing is committed, pushed or published without the owner's go-ahead.

## README and platform description

- The README follows [README-TEMPLATE.md](README-TEMPLATE.md): the same sections in the same order in every mod.
- The chapters in the middle are the guide book's chapters, in the book's order and under the book's titles. The
  README says what the book says and adds what does not fit on a page.
- Pictures live in `docs/` and are linked relatively. The logo is the mod's `icon.png`, 128 wide, on the right.
- The Modrinth and CurseForge description is never written by hand: `python3 ../bcf-mod-template/tools/make-listing.py .`
  writes `docs/listing.md` from the README (committed with it). Whatever is between `<!-- listing:skip -->` and
  `<!-- listing:end -->` stays out of it. CurseForge has no interface for the description: paste the file into its
  editor (Markdown mode). `--modrinth` sends it to Modrinth.

## Guide book

The screen, its layout, the font and the way the pages turn come from
[bcf-guide-book-lib](https://github.com/david-stefan-hermann/bcf-guide-book-lib) and are the same in every mod. A mod
never draws a book screen of its own. What a mod decides:

- **Colours:** one `BookTheme` that fits the mod's other screens, optionally with a panel picture (232 x 230).
- **Chapters,** in this order:
  1. *Getting started* (right-hand tab, the book as icon): what the mod is, in two or three sentences, a quote, then
     the first steps as item lines.
  2. One chapter per thing the mod adds (block, item, tree, ...), left-hand tabs, with the thing as icon and its
     name as title. First page: what it is, a quote, heading *Crafting*, the recipe. Then a page break and heading
     *Use*: how it is used. Pictures where words are not enough.
  3. Topics that span several things (range, finding, ...), right-hand tabs, each with a vanilla or own item as icon.
- **Writing:** short sentences, present tense, what the player does and what then happens. Numbers come from the
  config or the code as text arguments, never typed into the text. No section taller than a page.
- **Languages:** `en_us` and `de_de`, always both.
- **The item:** `guide_book`, stacks to 1, first in the mod's creative tab, given once to every player on their first
  join (`BOOK.giveOnJoin()`), with a shapeless recipe from a book and something typical of the mod.
- **Something a book needs that the library lacks** (a new kind of section, say) is added to the library, for all
  mods.

Checked before a release, in both languages: `./gradlew runClient -PbookShots` writes every page to
`run/screenshots/book_<modid>_<language>_<nr>.png`; the log must show `BOOK PAGES` and neither `BOOK OVERFLOW` nor
`BOOK KEY MISSING`.

### Changing something for all books

The font, line heights and measures are `BookStyle` in bcf-guide-book-lib. Change it there, raise the library's
version, run `./gradlew publishToMavenLocal`, then raise `guide_book_version` in each mod and build it. The pages
break themselves again; look at each mod's book shots. A player's game loads the newest library version that any of
their mods bundles, so within a major version the library stays backwards compatible: a mod built against 1.0 runs
with 1.4. A breaking change is a new library (new mod id and package) instead.
