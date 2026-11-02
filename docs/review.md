# Source review

## Current publication

The owner approved this source and package release. The reproducible prerelease is [0.1.0-rc.1](https://github.com/rectoversohq/rectoverso-flags/releases/tag/v0.1.0-rc.1). Its English/French assets and SHA-256 manifest identify the exact bytes; earlier validation and source provenance below remain historical evidence. Subsequent changes still require their own checks and publication approval.

The deck is CC BY 4.0, with component licenses retained. This source release does not deploy app asset packs or change the app source pin.


The owner approved creating this repository and pushing this candidate for source review. The [source issue](https://github.com/rectoversohq/rectoverso-flags/issues/1) tracks the first PR against a README-only main branch. Merges, version tags and package releases remain separate owner decisions. The source is public; no packaged deck release is published.

## Provenance of this branch

The initial source commit is an exact Git-tree snapshot of the previously tested local candidate `41c3e2123cf063ada201eb83e4e841a9274609cf` (tree `e11c766b9d1b70659818b0e4bd5cf4b001d49985`). Its original local branch and history remain intact. The following setup commit updates repository/build instructions; it does not change learning content, images, identities, templates or package-generation code. Source history was inspected for packaged decks, font binaries, credentials and inappropriate private content before pushing. Build output and evidence stay outside source Git.

The manifest describes the frozen reviewed package candidate, including its recorded local status; it does not announce a release. Regenerated archives may have different timestamp-dependent bytes. Use the sidecars from the actual build.

## Checks and next steps

- [Anki packages](https://github.com/rectoversohq/rectoverso-flags/actions) runs from this branch and its PR. Inspect the actual check result at the PR head; this page does not infer success from workflow presence.
- Local source/native-backend and independent clean-clone checks are recorded with the source PR. [Validation](validation.md) distinguishes backend, bundled reviewer, manual desktop and app evidence.
- Native Anki desktop review remains a release gate. Existing app integration evidence is tracked in [the app task](https://github.com/simonpinkas/RectoVerso/issues/648).
- Require a PR, resolved conversations and the exact **Anki packages** check for main; branch protection is a repository setting, not part of the source files.
- After editorial/native approval, obtain the owner’s go for a versioned bilingual package release.
- The app will pin one multilingual source submodule to an approved tag. Source CI itself neither starts Xcode Cloud nor deploys an Apple asset pack.

## En français

Le propriétaire a autorisé le dépôt et l’envoi des sources pour revue. Le premier commit de sources reproduit exactement l’arbre du candidat testé indiqué ci-dessus ; son historique local d’origine est conservé. Les modifications de mise en place concernent la documentation, sans changer les cartes, médias, identités ni générateurs. Vérifier le résultat réel d’**Anki packages** sur la pull request. La revue Anki Desktop, l’approbation éditoriale et la publication restent des étapes distinctes. Aucun paquet n’est publié à ce stade.

## Owner phone feedback

Answer context now exposes **Continent** and **Region** as separate English/French resources. Existing continent memberships and search aliases are unchanged. The new Region field is appended; existing deck/model/template/field identities remain intact. The shared French national tricolor is used only for France in every flag exercise. The ten affected territories keep their ISO records and any applicable non-flag exercises. The four geographic riddles for Indonesia/Monaco and Chad/Romania are removed, with faithful flag artwork unchanged.

The current candidate has **460 cards per language**. Source regression tests and complete bilingual `scripts/ci.py` pass in the working source. Anki renders every direction label; this does not prove its native RectoVerso visibility. Updates from both exact earlier language packages preserve every existing note ID and a genuinely studied card's schedule while applying the Region field. Retired test cards remain after ordinary Anki update; [coverage](coverage.md) documents the explicit cleanup/replacement boundary. No personal collection was opened.

Fresh-clone and hosted results for the final commit are recorded on [source PR #2](https://github.com/rectoversohq/rectoverso-flags/pull/2). The separate app presentation issue is [#655](https://github.com/simonpinkas/RectoVerso/issues/655); the source cannot prove that native layout repair. App/content tracking remains [#648](https://github.com/simonpinkas/RectoVerso/issues/648). No merge, package release or catalog change is included.
