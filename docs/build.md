# Build, review and update

`python scripts/ci.py --output NEW_EXTERNAL_DIRECTORY` is the single complete source check. Run it with the Python 3.14 environment installed from `requirements.txt`. Do not use an existing output folder; old and failed evidence stays intact.

For one package only:

```sh
python scripts/build.py --language en --out /outside/repo/Flags-en-460.apkg
python scripts/build.py --language fr --out /outside/repo/Drapeaux-fr-460.apkg
```

## Source layout

| Path | Purpose |
|---|---|
| `source/places.json` | Shared named places, applicability, capital roles and provenance |
| `source/languages/` | English/French field names and small interface text |
| `source/continents.json` | Geographic convention, memberships and bilingual search labels |
| `source/curriculum.json` | Exercises and new-card introduction order |
| `source/identities.json` | Frozen candidate GUID, deck/model/field/template identities |
| `source/media/` | Attributed, Anki-compatible PNG files |
| `artwork/svg/` | Original flag vectors |
| `artwork/covers/` | Approved SVG masters for gallery covers |
| `scripts/` | Builder, CI and macOS SVG rendering tool |
| `scripts/checks/`, `tests/` | Source, Anki round-trip and reproducibility checks |

## Regenerate flag media

On macOS, compile `scripts/render-svg.swift` into an external temporary directory. Run `RENDERER NEW_OUTPUT_DIRECTORY 900 artwork/svg/*.svg`; it keeps the SVG aspect ratio. Review every changed image and update its digest in the manifest. Rebuilding packages does not require regenerating unchanged PNGs. Do not replace official flags with decorative approximations.

## Gallery metadata

RectoVerso's gallery reads this deck from `rectoverso.json` and each package's `.rectoverso.json` sidecar, attached to the release with the release's `SHA256SUMS` (the contract: [RectoVerso #690](https://github.com/simonpinkas/RectoVerso/issues/690)). Beside the identity and version: the headline and description in each language, the categories, the creator, the license, the upstream sources, and under each language its `sample`, the GUID of the card the gallery opens as the deck's sample question. A sample is one of that language's cards and shows alone with all its pictures; `scripts/checks/verify-source.py` checks it.

## Gallery covers

Render and check the covers in an external directory.

```sh
python scripts/covers.py --output /outside/repo/covers
python scripts/checks/verify-covers.py --output /outside/repo/covers
```

The SVG masters in `artwork/covers/` use
`rv-flags[-<en|fr>]-cover[-<light|dark>]-<n>.svg` with lowercase names
and numbering from 1. Omit the language for art without words and omit the
appearance for art that serves both light and dark mode. A cover with words
needs a master for every shipped language at the same number and appearance.
Use a 3:2 SVG viewport, outline any lettering, and keep resources inside each
SVG. The renderer checks the PNG dimensions before writing the files. The
three approved masters are shared across both languages and appearances.

The package build renders the masters beside the packages and sidecars as
2,010 × 1,340 PNGs. CI checks names, dimensions, light and dark coverage for
each language, complete localized sets, and ambiguous names. The language
pill's corner (`x ≥ 1608`, `y ≤ 335`) must be within 4 per channel of its
dominant color. CI compares PNG bytes across independent builds and attaches
them as the `flags-covers` artifact. List the files in the deck metadata when
preparing a release.

### Artwork provenance

The approved compositions are © Simon Pinkas, CC BY 4.0. Sunline and
Quartered use motifs drawn from the deck's flag references. The frosted
reveal embeds the exact public-domain `rv-flag-syc.png` from `source/media/`,
SHA-256 `0c8a5c8633aecfc6c8eefcdd53bd0ba2b750cef18f13726af0e27bef9e1185b9`.
The [flag credits](flag-credits.md) and [manifest](../rectoverso.json) record
each source and component license.

| Master | Flag references | SHA-256 |
|---|---|---|
| [rv-flags-cover-1.svg](../artwork/covers/rv-flags-cover-1.svg) | [Brazil](../artwork/svg/rv-flag-bra.svg), [Japan](../artwork/svg/rv-flag-jpn.svg) | `a47340fa8bb83dbc93bf64f12cf1b2bcdc1483c2e3346239b4dbdc9d1cc5e7df` |
| [rv-flags-cover-2.svg](../artwork/covers/rv-flags-cover-2.svg) | [Seychelles](../artwork/svg/rv-flag-syc.svg), [deck image](../source/media/rv-flag-syc.png) | `819df4c48e5864fbfc64f9fed2fd449654227f4131619bd41a5b75d6d493470f` |
| [rv-flags-cover-3.svg](../artwork/covers/rv-flags-cover-3.svg) | [Panama](../artwork/svg/rv-flag-pan.svg), [Canada](../artwork/svg/rv-flag-can.svg) | `fc3438b298646469516488c60daa02f5a1f84ad58ef53d02e84b41c2494bd515` |

## Updating a published deck

1. Branch in this deck repository and attach the PR to a source issue.
2. Edit content, retaining published GUIDs, field IDs and template IDs. Date a new reviewed version using `contentModifiedAt`; never forge a future modification time.
3. Run complete CI from the branch and a clean clone. Test an actual prior release → candidate import with existing progress: import the published predecessor (0.1.0-rc.1 for 0.1.0-rc.2) into a disposable Anki collection, study it, then import the candidate with Anki’s default import and with **Always**. Every note GUID, the studied schedules and the review log must survive. A duplicate import is not misrepresented as a historical upgrade.
4. Review native Anki and RectoVerso cards, both languages/themes, flags with unusual proportions, all capital-role cases, search aliases and post-answer notes.
5. Obtain owner approval for source/release publication. Publish source and the two package assets only after that approval.
6. Update the app’s submodule pointer and catalog through its feature branch and compatibility checks. Deck CI does not deploy an Apple asset pack or start Xcode Cloud by itself.

## Remaining release gates

- Owner editorial/visual review, including the documented holds and disputed-role wording.
- Native Anki desktop and RectoVerso import/study confirmation; backend validation is separate.
- Source review and branch protection: see [the review record](review.md). The hosted workflow exposes the exact **Anki packages** check; require it before merging. A workflow existing in source is not evidence that branch protection is active.
- Publication approval and versioned artifact hashes in the app catalog.

See [validation and reviewer evidence](validation.md) for automated checks and the remaining manual review gates.
