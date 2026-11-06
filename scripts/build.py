"""Build a self-contained Anki package from the checked-in source. No downloads."""

import argparse, hashlib, json, shutil, tempfile
from datetime import datetime
from pathlib import Path
from anki.collection import Collection, ExportAnkiPackageOptions
from anki.decks import DeckId
from covers import render_covers
from source_data import ROOT, inputs


def build(language, out):
    meta, notes, models, deck = inputs(language)
    out = out.resolve()
    if (
        out.is_relative_to(ROOT)
        or out.exists()
        or out.with_suffix(".rectoverso.json").exists()
    ):
        raise ValueError("Use a new package outside the checkout")
    if out.name != meta["package"]["file"]:
        raise ValueError("Artifact name differs")
    out.parent.mkdir(parents=True, exist_ok=True)
    if len(notes) != meta["cards"] or len({n["guid"] for n in notes}) != len(notes):
        raise ValueError("Card count or note identities differ")
    render_covers(out.parent)
    with tempfile.TemporaryDirectory(prefix="anki-build-", dir=out.parent) as temp:
        col = Collection(str(Path(temp) / "collection.anki2"))
        try:
            added = {}
            for key, model in models.items():
                nt = col.models.new(model["name"])
                for name in model["fields"]:
                    field = col.models.new_field(name)
                    field["id"] = model["fieldIDs"][name]
                    col.models.add_field(nt, field)
                for template in model["templates"]:
                    entry = col.models.new_template(template["name"])
                    entry.update(template)
                    col.models.add_template(nt, entry)
                nt.update(
                    id=model["id"],
                    css=model["css"],
                    mod=int(
                        datetime.fromisoformat(
                            meta["contentModifiedAt"].replace("Z", "+00:00")
                        ).timestamp()
                    ),
                )
                col.models.update(nt)
                added[key] = nt
            entry = col.decks.new_deck_legacy(False)
            entry.update(id=deck["id"], name=deck["name"], desc=deck["description"])
            col.decks.update(entry)
            for source in notes:
                note = col.new_note(added[source["model"]])
                note.guid = source["guid"]
                note.tags = source["tags"]
                for key, value in source["fields"].items():
                    note[key] = value
                col.add_note(note, DeckId(deck["id"]))
            for credit in meta["imageCredits"]:
                name = credit["file"]
                if Path(name).name != name:
                    raise ValueError("Media path is not a basename")
                shutil.copyfile(
                    ROOT / "source/media" / name, Path(col.media.dir()) / name
                )
            if col.card_count() != meta["cards"]:
                raise ValueError("Anki generated unexpected cards")
            col.db.execute(
                "update notes set mod = ?",
                int(
                    datetime.fromisoformat(
                        meta["contentModifiedAt"].replace("Z", "+00:00")
                    ).timestamp()
                ),
            )
            col.export_anki_package(
                out_path=str(out),
                options=ExportAnkiPackageOptions(
                    with_scheduling=False, with_media=True
                ),
                limit=None,
            )
        finally:
            col.close()
    meta["package"] = meta["package"] | {
        "bytes": out.stat().st_size,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }
    out.with_suffix(".rectoverso.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "language": language,
                "cards": len(notes),
                "file": out.name,
                "bytes": out.stat().st_size,
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--language", required=True, choices=["en", "fr"])
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    build(a.language, a.out)
