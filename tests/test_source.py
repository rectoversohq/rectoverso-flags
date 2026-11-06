import json, re, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from source_data import inputs, read


class SourceContract(unittest.TestCase):
    def test_coverage_accounts_for_every_reference_place(self):
        places = read("source/places.json")
        self.assertEqual(len(places), 249)
        omitted = {
            (e["code"], e["kind"])
            for e in read("source/coverage-exceptions.json")["exceptions"]
        }
        exercises = read("source/curriculum.json")["exercises"]
        keys = {x[k] for x in exercises for k in ("question", "answer")}
        for p in places:
            if "flag" in keys and not p.get("flag"):
                self.assertIn((p["code"], "flag"), omitted)
            if "capital" in keys and not p["capitals"]:
                self.assertIn((p["code"], "capital"), omitted)

    def test_primary_answers_are_not_post_answer_resources(self):
        for lang in ("en", "fr"):
            m, notes, models, d = inputs(lang)
            words = read("source/languages/" + lang + ".json")["fields"]
            exercise = {e["id"]: e for e in read("source/curriculum.json")["exercises"]}
            for n in notes:
                e = exercise[n["exercise"]]
                self.assertTrue(n["fields"][words[e["question"]]])
                self.assertTrue(n["fields"][words[e["answer"]]])
                template = models[n["model"]]["templates"][0]
                self.assertIn('id="rv-details" hidden', template["afmt"])
                self.assertNotIn(
                    "RectoVerso search", template["qfmt"] + template["afmt"]
                )
                self.assertEqual(
                    bool(n["fields"]["RectoVerso place"]), e["question"] == "map"
                )

    def test_multi_continent_and_cross_language_aliases(self):
        for lang in ("en", "fr"):
            notes = inputs(lang)[1]
            n = next(n for n in notes if n["code"] == "RUS")
            fields = json.loads(n["fields"]["RectoVerso search"])["fields"]
            c = fields[0]
            self.assertEqual(set(c["aliases"]), {"Europe", "Asia", "Asie"})
            self.assertEqual(len(c["values"]), 2)

    def test_multiple_capital_roles_are_individually_qualified(self):
        for p in read("source/places.json"):
            if len(p["capitals"]) > 1:
                self.assertEqual(
                    len({c["role"]["en"] for c in p["capitals"]}), len(p["capitals"])
                )

    def test_continents_describe_whole_places_not_maps_core_questions(self):
        places = {p["code"]: p for p in read("source/places.json")}
        for code, expected in {
            "FRA": ["EU"],
            "PRT": ["EU"],
            "COL": ["SA", "NA"],
            "VEN": ["SA", "NA"],
            "ESP": ["EU", "AF"],
        }.items():
            self.assertEqual(places[code]["continents"], expected)
        for code, expected in {
            "AUS": ["OC"],
            "NZL": ["OC"],
            "ZAF": ["AF"],
            "SHN": ["AF"],
        }.items():
            self.assertEqual(places[code]["continents"], expected)

    def test_french_text_follows_french_typography(self):
        # RectoVerso's French: a narrow no-break space (U+202F) before ; : ! ? and inside « »,
        # never an ordinary space and never none. A URL's colon is not punctuation.
        mark = re.compile(r"(?<!\u202f)[;:!?](?!//)|«(?!\u202f)|(?<!\u202f)»")
        _, notes, _, deck = inputs("fr")
        texts = [deck["description"], deck["name"]]
        for note in notes:
            for name, value in note["fields"].items():
                if "<img" in value:
                    continue
                if name == "RectoVerso search":
                    for field in json.loads(value)["fields"]:
                        texts += [field["name"], *field["values"], *field["aliases"]]
                else:
                    texts.append(value)
        meta = read("rectoverso.json")
        texts += [meta[k]["fr"] for k in ("title", "subject", "headline", "description")]

        def strings(value):
            if isinstance(value, dict):
                return [s for v in value.values() for s in strings(v)]
            if isinstance(value, list):
                return [s for v in value for s in strings(v)]
            return [value] if isinstance(value, str) else []

        texts += strings(read("source/languages/fr.json"))
        for path in ("source/places.json", "source/coverage-exceptions.json"):
            def french(value):
                if isinstance(value, dict):
                    return [s for k, v in value.items() for s in ([v] if k == "fr" and isinstance(v, str) else french(v))]
                if isinstance(value, list):
                    return [s for v in value for s in french(v)]
                return []
            texts += french(read(path))
        for text in texts:
            self.assertNotRegex(text, mark)
        continents = {n["fields"]["Continent"] for n in notes}
        self.assertIn("Europe\u202f; Asie", continents)
        english = {n["fields"]["Continent"] for n in inputs("en")[1]}
        self.assertIn("Europe; Asia", english)

    def test_private_material_never_claims_blanket_cc(self):
        m = read("rectoverso.json")
        self.assertEqual(m["license"].startswith("LicenseRef"), m["proOnly"])


if __name__ == "__main__":
    unittest.main()
