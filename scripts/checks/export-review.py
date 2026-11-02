import argparse, json, re, shutil
from pathlib import Path
from anki.collection import Collection
from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportAnkiPackageOptions

p = argparse.ArgumentParser()
p.add_argument("--output", type=Path, required=True)
p.add_argument("packages", type=Path, nargs="+")
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=False)
items = []
for package in a.packages:
    meta = json.loads(package.with_suffix(".rectoverso.json").read_text())
    folder = a.output / (meta["deckID"] + "-" + meta["language"])
    folder.mkdir()
    col = Collection(str(folder / "collection.anki2"))
    try:
        col.import_anki_package(
            ImportAnkiPackageRequest(
                package_path=str(package),
                options=ImportAnkiPackageOptions(merge_notetypes=True),
            )
        )
        cards = [col.get_card(cid) for cid in col.find_cards("")]
        directions = sorted(
            {
                t.removeprefix("exercise::")
                for c in cards
                for t in c.note().tags
                if t.startswith("exercise::")
            }
        )
        for direction in directions:
            for code in ["ZAF", "NPL", "FRA"]:
                card = next(
                    (
                        c
                        for c in cards
                        if "exercise::" + direction in c.note().tags
                        and "place::" + code in c.note().tags
                    ),
                    None,
                )
                if card is None:
                    continue
                for side, body in [
                    ("question", card.question()),
                    ("answer", card.answer()),
                ]:
                    name = f"{direction}-{code}-{side}.html"
                    (folder / name).write_text(body)
                    for media in re.findall(r'<img src="([^"]+)"', body):
                        shutil.copyfile(Path(col.media.dir()) / media, folder / media)
                    items.append(
                        {
                            "path": str(folder / name),
                            "language": meta["language"],
                            "deck": meta["deckID"],
                            "direction": direction,
                            "code": code,
                            "side": side,
                        }
                    )
    finally:
        col.close()
(a.output / "items.json").write_text(json.dumps(items, indent=2) + "\n")
print(len(items), "backend-rendered sample sides")
