"""One command for source, bilingual build, native Anki and independent rebuild checks."""

import argparse, json, os, platform, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
out = a.output.resolve()
if out.is_relative_to(ROOT) or out.exists():
    p.error("Use a new output directory outside the checkout")
out.mkdir(parents=True)
(out / "tmp").mkdir()
env = os.environ | {"TMPDIR": str(out / "tmp"), "PYTHONDONTWRITEBYTECODE": "1"}
report = {
    "passed": False,
    "python": sys.version,
    "platform": platform.platform(),
    "steps": [],
}
try:
    report["commit"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    report["workingTreeDirty"] = bool(
        subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT)
    )

    def run(name, *command):
        with (out / (name + ".log")).open("w") as f:
            r = subprocess.run(
                command, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT
            )
        report["steps"].append({"name": name, "exitCode": r.returncode})
        if r.returncode:
            raise RuntimeError(name + " failed; see " + str(out / (name + ".log")))
        print(name + ": passed", flush=True)

    run("source", sys.executable, "scripts/checks/verify-source.py")
    run("tests", sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v")
    meta = json.loads((ROOT / "rectoverso.json").read_text())
    for folder in ("packages", "rebuilt"):
        (out / folder).mkdir()
        for lang, data in meta["languages"].items():
            run(
                folder + "-" + lang,
                sys.executable,
                "scripts/build.py",
                "--language",
                lang,
                "--out",
                str(out / folder / data["package"]["file"]),
            )
    run(
        "covers",
        sys.executable,
        "scripts/checks/verify-covers.py",
        "--output",
        str(out / "packages"),
        "--compare",
        str(out / "rebuilt"),
    )
    run(
        "anki",
        sys.executable,
        "scripts/checks/validate-anki.py",
        "--output",
        str(out / "anki"),
        *[
            str(out / "packages" / d["package"]["file"])
            for d in meta["languages"].values()
        ]
    )
    for lang, data in meta["languages"].items():
        run(
            "rebuild-" + lang,
            sys.executable,
            "scripts/checks/validate-rebuild.py",
            str(out / "packages" / data["package"]["file"]),
            str(out / "rebuilt" / data["package"]["file"]),
            str(out / ("rebuild-" + lang + ".json")),
        )
    report["passed"] = True
finally:
    (out / "ci.json").write_text(json.dumps(report, indent=2) + "\n")
