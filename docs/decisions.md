# Decisions

## 2026-11-04 — Publication preparation for 0.1.0-rc.2

The owner asked for this preparation before releasing 0.1.0-rc.2. The Anki deck description, which still read “Local review candidate; not published”, now describes the published deck in English and French, with its license and where its credits and sources are. The READMEs, NOTICE and review page point to 0.1.0-rc.2, and the update guide names 0.1.0-rc.1 as the published predecessor to test from. Cards, notes, identities and pictures are unchanged; `contentModifiedAt` stays, since no card changed.

## 2026-11-04 — Gallery copy

The owner approved the gallery copy: the headline "Know a place by its flag, and a flag by its place." / « Reconnaître un lieu à son drapeau, et un drapeau à son lieu. » and the description that names its 230 flags (in `rectoverso.json`). It replaces the first draft, whose headline was ambiguous and whose description read as every place's flag.

## 2026-11-02 — Owner phone feedback

Answer context now exposes **Continent** and **Region** as separate English/French resources. Existing continent memberships and search aliases are unchanged. The new Region field is appended; existing deck/model/template/field identities remain intact. The shared French national tricolor is used only for France in every flag exercise. The ten affected territories keep their ISO records and any applicable non-flag exercises. The four geographic riddles for Indonesia/Monaco and Chad/Romania are removed, with faithful flag artwork unchanged.

The source remains a review candidate. Existing images, attribution, licenses and unaffected GUIDs remain intact. Where exercises are removed, their GUIDs are recorded separately and never reassigned. Updating an existing test collection does not delete retired cards; validation explicitly checks that limitation instead of claiming a clean replacement. Native app task visibility is tracked independently in [#655](https://github.com/simonpinkas/RectoVerso/issues/655).

## 2026-11-02 — Owner-authorized prerelease

The owner approved releasing all authored decks. Publish this reviewed bilingual candidate as 0.1.0-rc.1 after exact-head checks. This publication-only change updates package status and download/build instructions without changing note content, identities or artwork. Preserve the existing CC BY 4.0 license and original component rights. App pin/catalog delivery remains separate.

## 2026-11-03 — Gallery metadata and sample question (candidate 0.1.0-rc.2)

RectoVerso's gallery reads every deck from one metadata layout ([#690](https://github.com/simonpinkas/RectoVerso/issues/690)). `rectoverso.json` adds a headline and a description in English and French, the `geography` category, the creator and the upstream sources, and under each language the `sample`: the GUID of the one card the gallery opens as the deck's sample question. The sample is proposed; the owner chooses it. Each language's sidecar carries it. Note content, identities and artwork are unchanged; only the release metadata and the version (0.1.0-rc.2, unreleased) change. Release and app pin wait for the owner.
