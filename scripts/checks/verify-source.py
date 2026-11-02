"""Reject broken source coverage, unsafe media and unstable candidate identities."""

import hashlib, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from source_data import ROOT, read, inputs


def verify():
    meta = read("rectoverso.json")
    places = read("source/places.json")
    reference = read("source/iso-reference.json")
    if len(places) != 249 or {p["code"] for p in places} != {
        p["code"] for p in reference["entries"]
    }:
        raise ValueError("249-entry ISO reference differs")
    if set(meta["languages"]) != {"en", "fr"}:
        raise ValueError("Expected English and French")
    credits = {c["file"]: c for c in meta["imageCredits"]}
    if len(credits) != len(meta["imageCredits"]):
        raise ValueError("Duplicate image credit")
    for name, c in credits.items():
        if (
            Path(name).name != name
            or not c.get("source")
            or not c.get("license")
            or not c.get("creator")
            or not c.get("licenseURL")
        ):
            raise ValueError("Missing source or credit")
        if len(c["creator"]) > 180 or "\n" in c["creator"]:
            raise ValueError(
                "Creator must be a concise attribution, not license boilerplate"
            )
        data = (ROOT / "source/media" / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != c["sha256"]:
            raise ValueError("Media digest differs")
    if read("source/continents.json")["assignments"] != {
        p["code"]: p["continents"] for p in places
    }:
        raise ValueError("Whole-place memberships differ from the 249-record source")
    note_ids = set()
    model_ids = set()
    deck_ids = set()
    counts = {}
    for language in meta["languages"]:
        m, notes, models, deck = inputs(language)
        if len(notes) != meta["cards"]:
            raise ValueError("Generated count differs")
        if deck["id"] in deck_ids:
            raise ValueError("Languages share a deck ID")
        deck_ids.add(deck["id"])
        for model in models.values():
            if model["id"] in model_ids:
                raise ValueError("Languages/exercises share a model ID")
            model_ids.add(model["id"])
            if len(set(model["fieldIDs"].values())) != len(model["fields"]):
                raise ValueError("Duplicate field identity")
            if (
                "RectoVerso search"
                in model["templates"][0]["qfmt"] + model["templates"][0]["afmt"]
            ):
                raise ValueError("Search metadata is visible")
        for n in notes:
            if n["guid"] in note_ids:
                raise ValueError("Duplicate note GUID")
            note_ids.add(n["guid"])
            search = json.loads(n["fields"]["RectoVerso search"])
            if search["v"] != 1 or not search["fields"] or len(search["fields"]) > 32:
                raise ValueError("Malformed search contract")
            for f in search["fields"]:
                if not f["name"] or not f["values"] or len(f["name"]) > 80:
                    raise ValueError("Empty search field")
                if any(
                    not s or len(s) > 256 for s in f["values"] + f.get("aliases", [])
                ):
                    raise ValueError("Invalid search value")
            for value in n["fields"].values():
                for image in re.findall(r'<img src="([^"]+)"', value):
                    if image not in credits:
                        raise ValueError("Uncredited image")
        counts[language] = len(notes)
    frozen = read("source/identities.json")
    expected = {
        lang: [n["guid"] for n in inputs(lang)[1]] for lang in meta["languages"]
    }
    if frozen["guids"] != expected:
        raise ValueError("Identity/order differs from frozen candidate roster")
    actual_schema = {}
    for lang in meta["languages"]:
        _, _, types, deck = inputs(lang)
        actual_schema[lang] = {
            "deckID": deck["id"],
            "models": {
                k: {
                    "id": m["id"],
                    "fieldIDs": m["fieldIDs"],
                    "templateIDs": [t["id"] for t in m["templates"]],
                }
                for k, m in types.items()
            },
        }
    if frozen["schema"] != actual_schema:
        raise ValueError("Frozen deck/model/field/template identities differ")
    print(
        json.dumps(
            {
                "isoPlaces": len(places),
                "cards": counts,
                "media": len(credits),
                "identities": len(note_ids),
                "passed": True,
            }
        )
    )
    return True


if __name__ == "__main__":
    verify()
