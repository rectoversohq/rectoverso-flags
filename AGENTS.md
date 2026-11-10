# Flags: rules for agents

**Read `kit/AGENTS.md` first.** The deck kit ([rectoverso-deck-kit](https://github.com/rectoversohq/rectoverso-deck-kit), a submodule at `kit/`: `git submodule update --init kit`) holds what every deck follows: the deck contract, its check, and the rules for authoring, covers, languages, versions and releases. This file adds only this deck's own rules and checks.

## This deck
- **Flags** (« Drapeaux »), `rectoversohq/rectoverso-flags`, public. GUID prefix `rv-flags`; languages English and French; license CC BY 4.0. Asks each place's flag, and the place of each flag.
- **Our own material here is CC BY 4.0, © Simon Pinkas** (never another name or a company).
- **The deck's own issues are in this repository;** the app's side of the deck (its pin, the catalog, the gallery) is an issue in simonpinkas/RectoVerso.

## This repository
- **Read first:** README.md, README.fr.md, docs/coverage.md and rectoverso.json; docs/review.md records the reviewed snapshot, docs/build.md how the deck is built, docs/flag-credits.md each flag's source, docs/validation.md the checks' evidence, docs/decisions.md the dated decisions.
- **Where things are:** source content in source/, the flags' vector originals in artwork/svg/, builders in scripts/ (build.py, render-svg.swift, source_data.py, ci.py), checks in scripts/checks/, tests in tests/, guides in docs/.
- **Before a commit:** `python scripts/ci.py --output <a new folder outside the repository>`, then again in a fresh clone.

## This deck's content
- **Coverage:** keep all 249 reference records (every place with an ISO 3166-1 code), and account in docs/coverage.md for each exercise that doesn't apply or is held back. The 39 regional questions are Maps' alone.
- **Never invent** a flag, a capital, artwork, a boundary or a fact. A flag's proportions and colors are its own, never a style.
- **Continents** agree with Maps' `continents.json` place by place; a difference is the owner's call.
- **Every flag** keeps its exact source, license and hash in docs/flag-credits.md and `imageCredits`.

## This deck's checks
- `python3 kit/check.py --rectoverso`: the deck contract, as RectoVerso's gallery takes a deck, by the kit pinned here (`kit/docs/check.md` explains each refusal). The workflow runs it first.
- `scripts/ci.py --output <folder>` builds both languages, checks the source (verify-source.py), the packages in Anki (validate-anki.py), a rebuild's identities (validate-rebuild.py) and Anki's rendering for review; tests in tests/.
- Anki desktop's look and RectoVerso's own are separate checks: a rendering in Anki's backend isn't a visual approval.

## This deck's covers
- **No covers yet:** the app shows placeholders until this deck releases its own. Build them as `kit/docs/covers.md` says, as Capitals' do (rectoversohq/rectoverso-capitals: scripts/covers.py, scripts/checks/verify-covers.py, tests/test_covers.py), once the owner has the designs.
- **PNG** for drawn art (a JPEG only for a photograph); small files (they ship inside the app's download: aim under 400 KB).
- **Accurate:** whatever real place, flag, element, name or shape a cover shows is right, checked against the deck's own sources.
- **Masters** in artwork/covers/, SVG, named as their PNGs (`.svg`), with lettering outlined (or a pinned, embedded font) so every render is identical; no external resource.
- **scripts/covers.py** renders every master to its PNG at 2010 × 1340, called by scripts/build.py, into the build's output folder, never into the repository (nothing rendered is committed). Two independent builds give the same bytes.
- **scripts/checks/verify-covers.py,** run by the deck's CI, refuses a wrong size or name, a language without a light and a dark cover, a worded cover missing in a language, an ambiguous set, and anything but background in the top-trailing corner the gallery keeps for the language's pill (within 4 per channel of the corner's dominant color). Its tests in tests/.
- **A new or changed cover** is shown to the owner as rendered PNGs, light and dark, every language, before it's merged.

## The kit
- **Pinned at `kit/`, at a tag.** Moving it is a pull request of its own, with the check run again (`kit/docs/versioning.md`). Never edit a file under `kit/` from here.
- **A new field, value or form** is a change to the kit, made there first (`kit/CONTRIBUTING.md`): this deck never uses one alone.
