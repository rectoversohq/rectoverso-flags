"""Compose one language's ordinary Anki cards from shared, attributed geography."""

import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    path = (ROOT / path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("Source path leaves repository")
    return json.loads(path.read_text())


def stable_id(value):
    return int.from_bytes(
        hashlib.sha256(value.encode()).digest()[:8], "big", signed=True
    )


def inputs(language):
    meta = read("rectoverso.json")
    artifact = meta["languages"][language]
    words = read(f"source/languages/{language}.json")
    places = read("source/places.json")
    curriculum = read("source/curriculum.json")
    types = {}
    notes = []
    names = words["fields"]
    style = (ROOT / "source/style.css").read_text()
    for index, exercise in enumerate(curriculum["exercises"]):
        key, question, answer = exercise["id"], exercise["question"], exercise["answer"]
        model_id = meta["identityBase"] + (100 if language == "fr" else 0) + index
        field_names = list(names.values())

        def tag(k):
            return "{{" + names[k] + "}}"

        front = (
            '<main class="question"><div class="eyebrow">'
            + words["exercises"][key]
            + "</div>"
        )
        front += '<div class="primary ' + question + '">' + tag(question) + "</div>"
        front += (
            "{{#"
            + names["qualifier"]
            + '}}<p class="qualifier">'
            + tag("qualifier")
            + "</p>{{/"
            + names["qualifier"]
            + "}}</main>"
        )
        back = (
            '{{FrontSide}}<hr id="answer"><main class="answer"><div class="primary '
            + answer
            + '">'
            + tag(answer)
            + "</div>"
        )
        # The input is a genuine optional-context button. Its value labels the control
        # without adding literal button text to the answer's content. RectoVerso's
        # existing onclick/hidden-field convention retains the field as a resource.
        back += (
            '<section class="context"><input type="button" class="details-button" value="'
            + html.escape(words["detailsButton"], quote=True)
            + '" onclick="var d=document.getElementById(\'rv-details\');d.hidden=!d.hidden;this.setAttribute(\'aria-expanded\',!d.hidden)" aria-expanded="false" aria-controls="rv-details"><div id="rv-details" hidden>'
            + "".join(
                "{{#" + names[field] + "}}<p><strong>"
                + html.escape(names[field]) + "</strong><br>" + tag(field)
                + "</p>{{/" + names[field] + "}}"
                for field in ("continent", "region", "details")
            )
            + "</div></section></main>"
        )
        types[key] = {
            "id": model_id,
            "name": meta["id"] + " · " + language + " · " + key,
            "fields": field_names,
            "fieldIDs": {
                n: stable_id(f'{meta["id"]}/{language}/{key}/field/{n}')
                for n in field_names
            },
            "templates": [
                {
                    "name": words["exercises"][key],
                    "id": stable_id(f'{meta["id"]}/{language}/{key}/template'),
                    "qfmt": front,
                    "afmt": back,
                }
            ],
            "css": style,
        }
    labels = read("source/continents.json")["labels"]
    sorted_places = sorted(
        places, key=lambda p: (p["continents"][0], p["name"][language], p["code"])
    )
    # The stage is only the order of new cards. Reviews remain Anki/RectoVerso's scheduler's.
    for exercise in sorted(
        curriculum["exercises"], key=lambda e: (e["stage"], e["order"])
    ):
        key, question, answer = exercise["id"], exercise["question"], exercise["answer"]
        for place in sorted_places:
            needs_flag = "flag" in (question, answer)
            needs_capital = "capital" in (question, answer)
            needs_map = "map" in (question, answer)
            if key in place.get("excludedExercises", []):
                continue
            if needs_flag and not place.get("flag"):
                continue
            if needs_map and not place.get("map"):
                continue
            capitals = place.get("capitals", []) if needs_capital else [None]
            for capital in capitals:
                parts = [labels[c][language] for c in place["continents"]]
                details = []
                if meta.get("proOnly"):
                    if capital:
                        details.append(
                            capital["name"][language]
                            + " — "
                            + capital["role"][language]
                        )
                    elif place.get("capitals"):
                        details.append(
                            place["capitals"][0]["name"][language]
                            + " — "
                            + place["capitals"][0]["role"][language]
                        )
                    if place.get("fact"):
                        details.append(place["fact"][language])
                elif capital and capital.get("note"):
                    details.append(capital["note"][language])
                qualifier = []
                if needs_flag and question == "flag" and place.get("flagQualifier"):
                    qualifier.append(place["flagQualifier"][language])
                if capital and (len(place["capitals"]) > 1 or capital.get("qualified")):
                    qualifier.append(capital["role"][language])
                if capital and question == "capital" and capital.get("ambiguous"):
                    qualifier.append(place["region"][language])
                search = [
                    {
                        "name": "Continent",
                        "values": parts,
                        "aliases": sorted(
                            {
                                labels[c][l]
                                for c in place["continents"]
                                for l in ("en", "fr")
                            }
                        ),
                    },
                    {
                        "name": words["region"],
                        "values": [place["region"][language]],
                        "aliases": sorted(set(place["region"].values())),
                    },
                    {
                        "name": names["place"],
                        "values": [place["name"][language]],
                        "aliases": sorted(set(place["name"].values())),
                    },
                ]
                if capital:
                    search.append(
                        {
                            "name": names["capital"],
                            "values": [capital["name"][language]],
                            "aliases": sorted(set(capital["name"].values())),
                        }
                    )

                def image(key):
                    media = place.get(key)
                    return (
                        '<img src="'
                        + html.escape(media["file"], quote=True)
                        + '" alt="'
                        + html.escape(words["imageAlt"][key], quote=True)
                        + '">'
                        if media
                        else ""
                    )

                values = {
                    "place": place["name"][language],
                    "capital": capital["name"][language] if capital else "",
                    "flag": image("flag"),
                    "map": image("map"),
                    "qualifier": " · ".join(qualifier),
                    "details": "<br>".join(
                        html.escape(x) for x in dict.fromkeys(details) if x
                    ),
                    # French takes a narrow no-break space before the semicolon (RectoVerso's French typography).
                    "continent": ("\u202f; " if language == "fr" else "; ").join(parts),
                    "region": place["region"][language],
                    "search": json.dumps(
                        {"v": 1, "fields": search},
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    "placeData": place["map"]["place"] if question == "map" else "",
                }
                suffix = "-" + capital["id"] if capital else ""
                notes.append(
                    {
                        "guid": f'{meta["guidPrefix"]}-{language}-{place["code"].lower()}-{key}{suffix}',
                        "model": key,
                        "fields": {names[k]: v for k, v in values.items()},
                        "tags": [
                            f"language::{language}",
                            f"exercise::{key}",
                            f'stage::{exercise["stage"]}',
                            f'place::{place["code"]}',
                        ],
                        "code": place["code"],
                        "exercise": key,
                        "stage": exercise["stage"],
                    }
                )
    deck = {
        "id": meta["identityBase"] + 1000 + (1 if language == "fr" else 0),
        "name": meta["title"][language],
        "description": words["description"],
    }
    localized = dict(meta)
    localized.pop("languages")
    localized.update(
        id=artifact["id"],
        deckID=meta["id"],
        language=language,
        package=artifact["package"],
        sample=artifact["sample"],
    )
    return localized, notes, types, deck
