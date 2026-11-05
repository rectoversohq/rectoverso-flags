# Flags source

@~/Dev/RectoVerso/agents/decks.md

Above: the rules every RectoVerso gallery deck follows (`agents/decks.md` in RectoVerso, `~/Dev/RectoVerso` on the owner's Mac). Below: this repository's own.

- **Read first:** README.md, README.fr.md, docs/coverage.md and rectoverso.json; docs/review.md records the reviewed snapshot.
- **Where things are:** source content in source/, vector originals in artwork/svg/, builders in scripts/, checks in scripts/checks/, tests in tests/, guides in docs/.
- **Coverage:** keep all 249 reference records, and account for each exercise that doesn't apply or is held back. Never invent a flag, a capital, artwork, a boundary or a fact. The 39 regional questions are Maps' alone.
- **New exercises** get stable note identities of their own; an existing exercise never becomes a different question. New-card stages are an introduction order, never a scheduler or an entitlement.
- **Every asset** has its exact provenance, license and hash. A flag's proportions and colors are its own, never a style. English and French names, role qualifiers, source notes and docs stay consistent.
- **Search metadata** (RectoVerso search v1) is hidden from studying: only the learner-facing names, values and aliases, never geometry, ids or license text.
- **Before a commit:** scripts/ci.py, then again in a fresh clone. Anki desktop's and RectoVerso's own look are separate checks: a rendering in the backend isn't a visual approval.
