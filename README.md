# BCF Mod Template

The house rules and the starting point for BaconCakeFactory's Minecraft mods (Fabric).

- [STANDARDS.md](STANDARDS.md): names, branches, versions, releases, what a README and a guide book contain.
- [README-TEMPLATE.md](README-TEMPLATE.md): the README every mod follows.
- `skeleton/`: a mod that builds, with a guide book from
  [bcf-guide-book-lib](https://github.com/david-stefan-hermann/bcf-guide-book-lib).
- `tools/new-mod.py "<Mod Name>"`: copies the skeleton into `../<mod-name>/` with the names filled in.
- `tools/make-listing.py <mod folder>`: writes the mod's `docs/listing.md`, the Modrinth and CurseForge description,
  from its README.

## License

MIT, see [LICENSE](LICENSE). By BaconCakeFactory.
