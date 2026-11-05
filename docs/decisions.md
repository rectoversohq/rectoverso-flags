# Decisions

## 2026-11-05 — Publication preparation for 0.1.0-rc.3

The owner asked for this preparation before releasing 0.1.0-rc.3. `rectoverso.json`'s version, tag and release address, the READMEs (English and French) and the review page point to 0.1.0-rc.3, and the update guide names 0.1.0-rc.2 as the published predecessor to test from. `contentModifiedAt` moves to a time after the France change, the last content change. The Anki deck descriptions already describe the published deck and are unchanged.

## 2026-11-05 — The French docs (0.1.0-rc.3)

The French README, the review page's French section and the French quotations of this page take RectoVerso's French typography, as the notes did in 0.1.0-rc.2 and as Maps 0.3.0-rc.3 did for its docs (the owner, for Maps: "Maps' French docs and READMEs are fixed in rc.3"): a narrow no-break space (U+202F) before « ; » and « : » and inside « », and « deck » for « jeu » (« dépôt du deck »). The apostrophes were already curly. Typography only: no card, package or meaning changes.

## 2026-11-05 — France in Europe only (0.1.0-rc.3)

The owner (2026-11-05), for Pro Geography 0.2.0-rc.2: "France: Europe only in Geography, matching Maps' core France. Drop North America from France's continents." Maps 0.3.0-rc.3 gives France Europe and asks Clipperton, which has no ISO 3166-1 code of its own, as a question of its own (North America). Flags 0.1.0-rc.2 gave France Europe + North America, for Clipperton, and so disagreed with Maps; the owner asked for Flags to follow in 0.1.0-rc.3 ([#5](https://github.com/rectoversohq/rectoverso-flags/issues/5)).

- **France** (`FRA`) is Europe only in `source/continents.json` and `source/places.json`. UN M49 and GeoNames classify France, as a whole, in Europe. Clipperton, a French atoll in the North Pacific, adds no continent: an exception to whole-place membership, said in the convention, the `scope` note and [coverage](coverage.md). The island rule no longer names Clipperton.
- France's two notes per language (`rv-flags-en-fra-flag-place` and `rv-flags-en-fra-place-flag`, and their French twins) show **Continent** Europe, and their search metadata no longer lists North America or Amérique du Nord. No other note's content changes, and no identity changes.
- Every other place's continents agree with Maps 0.3.0-rc.3's `continents.json`; France was the one difference.

`contentModifiedAt` moves to this revision, so Anki's default import applies the new text.

## 2026-11-05 — The Canary Islands in Europe; French typography (0.1.0-rc.2)

The owner's answers on this rc.2 (2026-11-05):
- "The Canary Islands go with Europe in the island rule, following the sources as with Madeira." Spain's reason becomes Ceuta, Melilla and the plazas de soberanía on the North African coast; Spain stays Europe + Africa, and no card changes from this (`continents.json`'s `islands` and `transcontinental` notes, [coverage](coverage.md)). The rule keeps "Otherwise, island location is not inherited from the administering state": the Atlantic islands now follow the sources' classification of Portugal and Spain, and the sentence still holds for every other island.
- French typography: "a narrow no-break space (U+202F) before « ; » in the French Continent field, and anywhere else the French cards or deck text have a plain space before « ; : ! ? » or inside « »", following RectoVerso's French rules and Maps 0.3.0-rc.3. `scripts/source_data.py` joins French continents with a narrow no-break space before the semicolon (`\u202f; `); English keeps `; `. 28 French notes change, the two exercises of the 14 places with more than one continent (« Afrique ; Antarctique », « Europe ; Asie »…); the reasons in `source/coverage-exceptions.json` take the same space. A source test holds the rule for every French field, search value, deck text and French source string.

`contentModifiedAt` moves to this revision, so Anki's default import applies the new text. No identity changes.

## 2026-11-05 — Portugal in Europe; Amsterdam and Saint Paul in Africa (0.1.0-rc.2)

The owner's answers for Maps 0.3.0-rc.3 ([rectoverso-maps PR #10](https://github.com/rectoversohq/rectoverso-maps/pull/10)): "Madeira → Europe, not Africa. Follow the sources." and "Amsterdam and Saint Paul → Africa, as UN M49 has it, not Antarctica. This replaces the 2 November call for those two islands." The owner (2026-11-05): Flags follows in its unpublished 0.1.0-rc.2, not in a later release.

- **Portugal** (`PRT`) is Europe alone in `source/continents.json` and `source/places.json`: UN M49, GeoNames and the CIA World Factbook classify Portugal in Europe, and no source assigns Madeira to Africa. Its two notes per language (`rv-flags-en-prt-flag-place` and `rv-flags-en-prt-place-flag`, and their French twins) show **Continent** Europe, and their search metadata no longer lists Africa or Afrique. No other note's content changes, and no identity changes. The island rule puts Madeira with the Azores in Europe; the Madeira tourism board's reference, now a dead link, goes.
- **French Southern Territories** (`ATF`) keep Africa + Antarctica. Only the text changes: Amsterdam and Saint Paul move to ATF's African group in `taxonomyReview`, with the IPEV reference and [coverage](coverage.md) to match.
- **Spain** (`ESP`) stays Europe + Africa: Ceuta, Melilla and the plazas de soberanía lie on the North African coast. An independent check found no source that assigns the Canary Islands to Africa; the island rule's Canary text is unchanged and waits for the owner.

`contentModifiedAt` moves to this revision, so Anki's default import updates the Portugal notes. The sources read are kept with the release evidence outside Git.

## 2026-11-04 — Publication preparation for 0.1.0-rc.2

The owner asked for this preparation before releasing 0.1.0-rc.2. The Anki deck description, which still read “Local review candidate; not published”, now describes the published deck in English and French, with its license and where its credits and sources are. The READMEs, NOTICE and review page point to 0.1.0-rc.2, and the update guide names 0.1.0-rc.1 as the published predecessor to test from. Cards, notes, identities and pictures are unchanged; `contentModifiedAt` stays, since no card changed.

## 2026-11-04 — Gallery copy

The owner approved the gallery copy: the headline "Know a place by its flag, and a flag by its place." / « Reconnaître un lieu à son drapeau, et un drapeau à son lieu. » and the description that names its 230 flags (in `rectoverso.json`). It replaces the first draft, whose headline was ambiguous and whose description read as every place's flag.

## 2026-11-02 — Owner phone feedback

Answer context now exposes **Continent** and **Region** as separate English/French resources. Existing continent memberships and search aliases are unchanged. The new Region field is appended; existing deck/model/template/field identities remain intact. The shared French national tricolor is used only for France in every flag exercise. The ten affected territories keep their ISO records and any applicable non-flag exercises. The four geographic riddles for Indonesia/Monaco and Chad/Romania are removed, with faithful flag artwork unchanged.

The source remains a review candidate. Existing images, attribution, licenses and unaffected GUIDs remain intact. Where exercises are removed, their GUIDs are recorded separately and never reassigned. Updating an existing test collection does not delete retired cards; validation explicitly checks that limitation instead of claiming a clean replacement. Native app task visibility is tracked independently in [#655](https://github.com/simonpinkas/RectoVerso/issues/655).

## 2026-11-02 — Owner-authorized prerelease

The owner approved releasing all authored decks. Publish this reviewed bilingual candidate as 0.1.0-rc.1 after exact-head checks. This publication-only change updates package status and download/build instructions without changing note content, identities or artwork. Preserve the existing CC BY 4.0 license and original component rights. App pin/catalog delivery remains separate.

## 2026-11-03 — Gallery metadata and sample question (candidate 0.1.0-rc.2)

RectoVerso's gallery reads every deck from one metadata layout ([#690](https://github.com/simonpinkas/RectoVerso/issues/690)). `rectoverso.json` adds a headline and a description in English and French, the `geography` category, the creator and the upstream sources, and under each language the `sample`: the GUID of the one card the gallery opens as the deck's sample question. The sample is proposed; the owner chooses it. Each language's sidecar carries it. Note content, identities and artwork are unchanged; only the release metadata and the version (0.1.0-rc.2, unreleased) change. Release and app pin wait for the owner.
