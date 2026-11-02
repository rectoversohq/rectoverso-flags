import unittest, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from source_data import inputs, read


class OwnerFeedback(unittest.TestCase):
    def test_geography_has_named_continent_and_region_resources(self):
        for language in ("en", "fr"):
            words = read(f"source/languages/{language}.json")["fields"]
            _, notes, models, _ = inputs(language)
            self.assertIn("region", words)
            for model in models.values():
                back = model["templates"][0]["afmt"]
                self.assertIn("{{" + words["continent"] + "}}", back)
                self.assertIn("{{" + words["region"] + "}}", back)
            for note in notes:
                self.assertTrue(note["fields"][words["continent"]])
                self.assertTrue(note["fields"][words["region"]])
                self.assertNotIn(note["fields"][words["region"]], note["fields"][words["details"]].split("<br>"))

    def test_france_alone_uses_its_tricolor_in_flag_exercises(self):
        territories = {"BLM", "GLP", "GUF", "MAF", "MTQ", "MYT", "NCL", "REU", "SPM", "WLF"}
        exercises = read("source/curriculum.json")["exercises"]
        flag_types = {e["id"] for e in exercises if "flag" in (e["question"], e["answer"])}
        for language in ("en", "fr"):
            notes = inputs(language)[1]
            self.assertFalse([n["guid"] for n in notes if n["code"] in territories and n["exercise"] in flag_types])
            self.assertEqual({n["exercise"] for n in notes if n["code"] == "FRA" and n["exercise"] in flag_types}, flag_types)

    def test_similar_flags_are_not_geographic_riddles(self):
        for language in ("en", "fr"):
            words = read(f"source/languages/{language}.json")["fields"]
            notes = inputs(language)[1]
            for note in notes:
                if note["code"] in {"FRA", "IDN", "MCO", "TCD", "ROU"} and note["exercise"] == "flag-place":
                    self.assertEqual(note["fields"][words["qualifier"]], "", note["guid"])

    def test_retired_identities_stay_retired_and_exclusions_are_documented(self):
        retired = read("source/retired-identities.json")["guids"]
        exceptions = read("source/coverage-exceptions.json")["exceptions"]
        documented = {(e["code"], exercise) for e in exceptions for exercise in e.get("exercises", [])}
        for language in ("en", "fr"):
            active = {n["guid"] for n in inputs(language)[1]}
            self.assertFalse(active.intersection(retired[language]))
            self.assertEqual(len(retired[language]), len(set(retired[language])))
        for place in read("source/places.json"):
            for exercise in place.get("excludedExercises", []):
                self.assertIn((place["code"], exercise), documented)
