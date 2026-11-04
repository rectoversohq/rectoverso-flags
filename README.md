# Flags

Recognize a flag. Recall it from a place name.

[Français](README.fr.md) · [Coverage and sources](docs/coverage.md) · [Build and update](docs/build.md)

**Prerelease 0.1.0-rc.2.** [Download the English/French Anki packages](https://github.com/rectoversohq/rectoverso-flags/releases/tag/v0.1.0-rc.2).

| | |
|---|---|
| Languages | English · Français — two packages from one shared source |
| Cards | 460 per language |
| Reference | 249 ISO countries and territories; only applicable exercises |
| Exercises | flag → place, place → flag |
| Media | 240 attributed images |
| License | CC BY 4.0, with original asset licenses retained |

Flags retain their real proportions. France alone uses its shared national tricolor in flag exercises. Similar flags are studied from their faithful artwork, without geographic riddles. Continent and region fields support discovery without cluttering the question. In Anki, **Explore** opens a short answer note. In RectoVerso, compatible importers expose that note after confirmation; app import and native visual review remain separate checks.

Answer context uses separately labeled **Continent** and **Region** fields. See [owner feedback and update semantics](docs/coverage.md#owner-feedback-and-context-labels).

## Get the source

The complete candidate is reviewed in [source issue #1](https://github.com/rectoversohq/rectoverso-flags/issues/1). Clone the tagged source to reproduce this prerelease:

```sh
git clone --branch v0.1.0-rc.2 https://github.com/rectoversohq/rectoverso-flags.git
cd rectoverso-flags
```

See [source review and validation status](docs/review.md).

## Build for Anki

Use Python 3.14 and the pinned Anki backend. No account, API key or paid service is needed. Tracked PNG assets are sufficient to build; macOS WebKit is needed only to regenerate them from SVG.

```sh
python3.14 -m venv /path/outside-the-repo/anki-venv
/path/outside-the-repo/anki-venv/bin/python -m pip install -r requirements.txt
/path/outside-the-repo/anki-venv/bin/python scripts/ci.py --output /path/outside-the-repo/first-build
```

The output must be a **new directory outside this checkout**. CI builds each language twice, checks semantic reproducibility, imports every card into Anki, renders both sides, performs a real study action, and verifies media plus progress through export/reimport. Reports and failed logs remain beside the packages.

Open `packages/Flags-en-460.apkg` or `packages/Drapeaux-fr-460.apkg` in Anki. Choose the language you want; these are independent study collections, not a language toggle applied to existing progress.

## Edit and update

Create a source-repository feature branch. Edit the shared records or language files, keep stable identities, and run the same CI command into a new output directory. Before a release, review the [explicit exceptions](docs/coverage.md), both languages, light/dark presentation and native app behavior. A passing build is not permission to publish.

Small, attributable corrections belong here; app rendering, search and entitlement changes belong in the app repository. See [the source layout and release checklist](docs/build.md).

## Credit

Learner names follow the reviewed Maps roster. The flag source register draws on Ultimate Geography 5.3 (public domain); additional territory artwork has individually recorded sources. Included flag artwork is public domain or CC0, with concise [per-file credits](docs/flag-credits.md) and full provenance in `rectoverso.json`. New authored material © Simon Pinkas. Read [NOTICE](NOTICE.md) and [LICENSE](LICENSE.md) for the actual boundaries of each license.
