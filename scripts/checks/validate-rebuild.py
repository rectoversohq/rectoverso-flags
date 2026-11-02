"""Check packaged source identity and a real, scheduled independent-rebuild import."""

import argparse
from compression import zstd
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import zipfile
from anki.collection import Collection
from anki.import_export_pb2 import ImportAnkiPackageRequest


def import_package(collection, package):
    collection.import_anki_package(
        ImportAnkiPackageRequest(package_path=str(package.resolve()))
    )
    collection.models._clear_cache()


def inspect(package, folder):
    folder.mkdir()
    # Anki allocates a local deck ID on first import. Compare the IDs encoded in
    # each package, and test local identity separately during an in-place update.
    with zipfile.ZipFile(package) as archive:
        database = folder / "source.sqlite"
        database.write_bytes(zstd.decompress(archive.read("collection.anki21b")))
    with sqlite3.connect(database) as connection:
        source_decks = sorted(
            row[0] for row in connection.execute("select distinct did from cards")
        )
    collection = Collection(str(folder / "collection.anki2"))
    try:
        import_package(collection, package)
        notes = {
            note.guid: (note.mid, note.fields)
            for note in (collection.get_note(nid) for nid in collection.find_notes(""))
        }
        mids = {value[0] for value in notes.values()}
        schemas = {
            model["id"]: {
                "fields": [(field["name"], field["id"]) for field in model["flds"]],
                "templates": [(t["id"], t["qfmt"], t["afmt"]) for t in model["tmpls"]],
                "css": model["css"],
                "mod": model["mod"],
            }
            for model in collection.models.all()
            if model["id"] in mids
        }
        media = {
            file.name: hashlib.sha256(file.read_bytes()).hexdigest()
            for file in Path(collection.media.dir()).iterdir()
            if file.is_file()
        }
        return {
            "notes": notes,
            "schemas": schemas,
            "sourceDeckIDs": source_decks,
            "media": media,
            "count": collection.card_count(),
        }
    finally:
        collection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="rebuild-", dir=args.output.parent
    ) as temporary:
        root = Path(temporary)
        before = inspect(args.first, root / "one")
        after = inspect(args.second, root / "two")
        if before != after:
            raise ValueError(
                "Independent build changed source identities, content, schema or media"
            )
        (root / "upgrade").mkdir()
        collection = Collection(str(root / "upgrade" / "collection.anki2"))
        try:
            import_package(collection, args.first)
            ids = set(collection.find_cards(""))
            card = collection.get_card(min(ids))
            card.type = 2
            card.queue = 2
            card.ivl = 19
            card.due = 37
            card.reps = 6
            collection.update_card(card)
            expected = (
                card.id,
                card.nid,
                card.did,
                card.type,
                card.queue,
                card.ivl,
                card.due,
                card.reps,
            )
            import_package(collection, args.second)
            kept = collection.get_card(card.id)
            actual = (
                kept.id,
                kept.nid,
                kept.did,
                kept.type,
                kept.queue,
                kept.ivl,
                kept.due,
                kept.reps,
            )
            if actual != expected or set(collection.find_cards("")) != ids:
                raise ValueError(
                    "Independent rebuild duplicated cards or changed local identity/progress"
                )
        finally:
            collection.close()
    result = {
        "cards": before["count"],
        "sourceContentAndIdentitiesExact": True,
        "mediaExact": True,
        "inPlaceCardIDsAndProgressPreserved": True,
        "archiveBytesMayDiffer": True,
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
