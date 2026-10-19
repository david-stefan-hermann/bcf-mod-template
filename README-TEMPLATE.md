# {Mod Name}

<img src="src/main/resources/assets/{modid}/icon.png" alt="{Mod Name} logo: {what it shows}" width="128" align="right">

{What it is} for Minecraft {26.2} (Fabric). {Three to six sentences: what the mod adds and how the parts work
together, the main things in **bold**.} Everything is in its own creative tab, *{Mod Name}*.

![{What the picture shows}](docs/{overview}.png)

## Download

Get `{modid}-<version>.jar` from [CurseForge](https://www.curseforge.com/minecraft/mc-mods/{mod-name}) or the
[GitHub releases](../../releases) and put it into `mods/` on the client and the server, next to Fabric API. Requires Minecraft {26.2}, Fabric Loader {0.19.3}+ and Java 25.

## The guide book

The **{Mod Name} Guide** is a book with a chapter for {every ...}, with the recipes and pictures, in English and
German. Craft it from a book and {an item}, or take it from the creative tab. Right-click opens it, E or Escape closes it;
{the blocks'} tabs are on the left, the topics' on the right.

This page follows the book chapter by chapter and adds the details that do not fit on its pages.

![The guide book open on the {chapter} chapter](docs/book.png)

<!-- listing:skip -->
| Chapter | |
|---|---|
| [Getting Started](#getting-started) | {the first steps} |
| [{Thing}](#{thing}) | {what it is for} |
| [{Topic}](#{topic}) | {what it explains} |

Not in the book: [Config](#config), [Commands](#commands), [Building](#building).
<!-- listing:end -->

## Getting Started

{The book's first chapter: what the mod is, then the first steps as a numbered list.}

## {Thing}

{One section per chapter of the book, in the book's order, under the book's title. What it is, in one or two
sentences.}

> *"{The chapter's quote.}"*

**Crafting** – {the recipe in words}:

```
I L I      I = iron ingot, L = lightning rod
C R C      C = copper ingot, R = block of redstone
I I I
```

**Use**

- {What the player does and what then happens.}

## {Topic}

{The book's topic chapters, the same way, with what does not fit on a page.}

## Config

`config/{modid}.json`:

```json
{}
```

{What each entry does and who reads it, server or client. Leave the section out if there is no config.}

## Commands

- `/{modid} ...` – {what it does}. {Leave the section out if there are no commands.}

<!-- listing:skip -->
## Building

Java 25, `./gradlew build` → `build/libs/{modid}-<version>.jar`. Needs
[bcf-guide-book-lib](https://github.com/david-stefan-hermann/bcf-guide-book-lib) in the local Maven repository first:
`./gradlew publishToMavenLocal` in a checkout of it.

{Test tools, generated art, where the guide book's content lives.}
<!-- listing:end -->

## Credits

- {Libraries, data sources, people.} {Leave the section out if there is nothing to credit.}

## License

MIT, see [LICENSE](LICENSE). By BaconCakeFactory.
