# Validation and review status

The source CI command builds both languages twice, imports every card with Anki's native backend, renders both sides, studies one card and preserves its scheduling state through repeated import and export/reimport. Independent rebuilds compare semantic source identities, models, fields and media; allocated local IDs are compared only within the same receiving collection.

The app importer is a separate gate. An early candidate exposed the text label of its supplementary-context `<button>` as an image answer. The template now uses a genuine accessible `<input type="button">`: its `value` is the control label, while its `onclick`, `aria-controls` and `aria-expanded` preserve the existing hidden-field resource convention. No content is hidden by a CSS workaround. App checks must assert exact intended text answers and genuine image answers for every exercise direction.

## Bundled Anki reviewer

These optional tools export actual backend-rendered samples for South Africa, Nepal and France, then use Anki's bundled Qt WebEngine to check light/dark pages. They test real mouse activation, keyboard closure, visible details, ARIA state, media and computed theme colors. Screenshots are evidence for the reviewer engine; this is **not** a completed manual Anki desktop study/edit session.

```sh
python scripts/checks/export-review.py --output /new/evidence/html /packages/english.apkg /packages/french.apkg
python scripts/checks/render-anki-review.py --evidence /new/evidence/html --web /path/to/anki/web --output /new/evidence/render
```

The second command requires the Python/PyQt6 environment bundled with the installed Anki application; its `web` directory contains `css/reviewer.css` and `js/reviewer.js`. It creates its own application and ephemeral web profile, and never opens a personal Anki collection. Keep output outside this source repository. Private Geography packages, rendered HTML and screenshots must stay in private evidence directories.

Native RectoVerso presentation, a manual Anki study/edit review, editorial acceptance and owner publication approval remain separate gates. Failing evidence is retained and superseded by named later runs, never silently overwritten.
