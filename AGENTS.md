# Geography source rules

Read both READMEs, docs/coverage.md and rectoverso.json before editing. This is a local review candidate authorized in the 2026-11-01/02 overnight gallery interview; creation of remote repositories and publication remain on hold. Work on a codex/ feature branch. The owner approves coverage, names, presentation and publication.

- One multilingual repository, with separate English/French Anki artifacts. Source content lives in source/, original vector assets in artwork/svg/, builders in scripts/, checks in scripts/checks/, tests in tests/, and guides in docs/.
- Keep all 249 reference records and account explicitly for inapplicable or held exercises. Do not invent flags, capitals, artwork, boundaries or facts. The 39 regional questions belong only to Maps.
- Preserve published GUIDs and deck/model/field/template IDs. New exercises receive stable separate note identities; never turn an existing exercise into a different question. New-card stages are introduction order, never a new scheduler or entitlement mechanism.
- Every asset needs exact provenance, license and hash. Original flag proportions and colors are not a styling choice. Keep English/French names, role qualifiers, source notes and documentation consistent.
- Optional RectoVerso search v1 metadata is hidden from studying. Only learner-facing name/value/alias fields belong in it. Technical geometry, IDs and license text are not search content.
- Run scripts/ci.py before committing builder/content changes, then repeat it in a fresh clone. Native Anki desktop and RectoVerso visual checks are separate release gates; backend rendering alone is not visual approval.
- Put packages and large evidence outside Git on the external media drive. Every tool accepts output paths; never hard-code a user's drive in source tools. Keep failed evidence.
- Commit named files only. No force push, merge, release, source publication or new remote repository without the owner's explicit approval for that batch. Attach source PRs to a source-repository issue once the remote exists. Document decisions and evidence for the central authored-deck page and app handoff.

Track this candidate in https://github.com/simonpinkas/RectoVerso/issues/648. Source publication and releases await owner review. Central authored-deck documentation is tracked in #647; the app search contract is #646.
