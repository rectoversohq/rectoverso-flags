"""Check native Anki rendering, media, real study and export/reimport for both languages."""

import argparse, hashlib, json, re, tempfile
from pathlib import Path
from anki.collection import Collection, ExportAnkiPackageOptions
from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportAnkiPackageOptions


def import_package(col, path):
    col.import_anki_package(
        ImportAnkiPackageRequest(
            package_path=str(path.resolve()),
            options=ImportAnkiPackageOptions(
                with_scheduling=True,
                merge_notetypes=True,
                update_notes=1,
                update_notetypes=1,
            ),
        )
    )
    col.models._clear_cache()


def check(package, output):
    meta = json.loads(package.with_suffix(".rectoverso.json").read_text())
    count = meta["cards"]
    with tempfile.TemporaryDirectory(prefix="native-anki-", dir=output) as temporary:
        root = Path(temporary)
        (root / "a").mkdir()
        (root / "b").mkdir()
        col = Collection(str(root / "a/collection.anki2"))
        try:
            import_package(col, package)
            ids = col.find_cards("")
            guids = set()
            directions = {}
            if len(ids) != count:
                raise ValueError("Card count differs")
            for cid in ids:
                card = col.get_card(cid)
                guids.add(card.note().guid)
                q, a = card.question(), card.answer()
                note = card.note()
                if card.template()["name"] not in q:
                    raise ValueError("Exercise direction missing from rendered question")
                direction = next(
                    t.removeprefix("exercise::")
                    for t in note.tags
                    if t.startswith("exercise::")
                )
                question_kind, answer_kind = direction.split("-")
                has_place = bool(note["RectoVerso place"])
                if has_place != (question_kind == "map"):
                    raise ValueError("Live-map metadata on a non-map question")
                has_question_image = bool(re.search(r"<img\b", q))
                after_answer = a.split('<hr id="answer">', 1)[1]
                has_answer_image = bool(
                    re.search(
                        r"<img\b", after_answer.split('<section class="context">', 1)[0]
                    )
                )
                if has_question_image != (question_kind in ("flag", "map")):
                    raise ValueError("Question image kind differs from exercise")
                if has_answer_image != (answer_kind in ("flag", "map")):
                    raise ValueError("Answer image kind differs from exercise")
                row = directions.setdefault(
                    direction,
                    {
                        "cards": 0,
                        "questionImage": has_question_image,
                        "answerImage": has_answer_image,
                        "liveMapQuestion": has_place,
                    },
                )
                row["cards"] += 1
                if not q.strip() or "<hr" not in a:
                    raise ValueError("Empty rendered side")
                answer = a.split("<hr", 1)[1]
                if not (
                    re.search(r"<img\b", answer)
                    or re.sub("<[^>]*>", "", answer).strip()
                ):
                    raise ValueError("Empty answer")
                if any(
                    t in q + a for t in ['"outline"', '"aliases"', "RectoVerso search"]
                ):
                    raise ValueError("Technical metadata exposed")
            media = col.media.check()
            if media.missing:
                raise ValueError("Missing media: " + str(media.missing))
            if len(guids) != count:
                raise ValueError("Duplicate note identities")
            card = col.get_card(ids[0])
            col.decks.select(card.did)
            col.sched.reset()
            studied = col.sched.getCard()
            if studied is None:
                raise ValueError("No card offered for study")
            col.sched.answerCard(studied, 3)
            before = col.get_card(studied.id)
            state = (
                before.id,
                before.nid,
                before.type,
                before.queue,
                before.due,
                before.reps,
                before.ivl,
            )
            import_package(col, package)
            kept = col.get_card(studied.id)
            if (
                kept.id,
                kept.nid,
                kept.type,
                kept.queue,
                kept.due,
                kept.reps,
                kept.ivl,
            ) != state:
                raise ValueError("Repeat import changed studied progress")
            notes = {
                col.get_note(nid).guid: tuple(col.get_note(nid).fields)
                for nid in col.find_notes("")
            }
            col.export_anki_package(
                out_path=str(root / "roundtrip.apkg"),
                options=ExportAnkiPackageOptions(with_scheduling=True, with_media=True),
                limit=None,
            )
            media_hashes = {
                p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in Path(col.media.dir()).iterdir()
                if p.is_file()
            }
        finally:
            col.close()
        other = Collection(str(root / "b/collection.anki2"))
        try:
            import_package(other, root / "roundtrip.apkg")
            actual = {
                other.get_note(nid).guid: tuple(other.get_note(nid).fields)
                for nid in other.find_notes("")
            }
            if (
                actual != notes
                or other.card_count() != count
                or other.media.check().missing
            ):
                raise ValueError("Export/reimport changed notes or media")
            actual_media = {
                p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                for p in Path(other.media.dir()).iterdir()
                if p.is_file()
            }
            if actual_media != media_hashes:
                raise ValueError("Media bytes changed through export")
            kept = other.get_card(state[0])
            if (
                kept.id,
                kept.nid,
                kept.type,
                kept.queue,
                kept.due,
                kept.reps,
                kept.ivl,
            ) != state:
                raise ValueError("Export/reimport lost study state")
        finally:
            other.close()
    result = {
        "package": package.name,
        "cards": count,
        "renderedSides": count * 2,
        "missingMedia": 0,
        "uniqueGUIDs": len(guids),
        "realStudyPreserved": True,
        "exportReimportFieldsAndMediaExact": True,
        "nativeDesktopVisualReview": "separate gate",
        "exerciseDirections": directions,
    }
    print(json.dumps(result), flush=True)
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("packages", type=Path, nargs="+")
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    results = [check(x, a.output) for x in a.packages]
    (a.output / "anki-validation.json").write_text(json.dumps(results, indent=2) + "\n")
