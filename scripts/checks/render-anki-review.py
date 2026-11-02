"""Exercise real HTML controls in Anki's bundled Qt reviewer, with an isolated profile."""

import argparse, json, time
from pathlib import Path
from PyQt6.QtCore import QTimer, QUrl, QPoint, Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtTest import QTest

p = argparse.ArgumentParser()
p.add_argument("--evidence", type=Path, required=True)
p.add_argument("--web", type=Path, required=True)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=False)
app = QApplication(["geography-native-review"])
profile = QWebEngineProfile()
profile.setCachePath(str(a.output / "cache"))
profile.setPersistentStoragePath(str(a.output / "storage"))
view = QWebEngineView()
page = QWebEnginePage(profile, view)
view.setPage(page)
view.resize(960, 900)
view.show()
items = [
    x | {"theme": theme}
    for x in json.loads((a.evidence / "items.json").read_text())
    for theme in ["light", "dark"]
]
expected = len(items)
results = []
current = None
started = 0
finished = False


def finish(error=None):
    global finished
    if finished:
        return
    finished = True
    report = {
        "pages": len(results),
        "expected": expected,
        "passed": not error
        and len(results) == expected
        and all(r["passed"] for r in results),
        "fatal": error,
        "renderer": "Anki bundled Qt WebEngine reviewer; isolated profile; not a manual desktop study session",
        "results": results,
    }
    (a.output / "review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({k: v for k, v in report.items() if k != "results"}), flush=True)
    app.quit()


def start():
    global current, started
    if not items:
        finish()
        return
    current = items.pop(0)
    started = time.monotonic()
    body = Path(current["path"]).read_text()
    cls = "card nightMode" if current["theme"] == "dark" else "card"
    doc = (
        '<!doctype html><html><head><meta charset="utf-8"><script>window.pycmd=()=>{};</script>'
        + f'<link rel="stylesheet" href="{(a.web/"css/reviewer.css").as_uri()}"><script src="{(a.web/"js/reviewer.js").as_uri()}"></script></head><body class="{cls}" data-review-index="{len(results)}">{body}</body></html>'
    )
    view.setHtml(doc, QUrl.fromLocalFile(str(Path(current["path"]).parent) + "/"))
    QTimer.singleShot(120, poll)


def capture(label):
    stem = "-".join(
        current[k] for k in ["deck", "language", "theme", "direction", "code", "side"]
    )
    view.grab().save(str(a.output / (stem + "-" + label + ".png")))


def complete(data):
    results.append(current | data)
    QTimer.singleShot(0, start)


def poll():
    def ready(value):
        if not value:
            if time.monotonic() - started > 8:
                finish("Load timeout: " + str(current))
            else:
                QTimer.singleShot(50, poll)
            return
        data = json.loads(value)
        data["themeMatches"] = data["background"] == (
            "rgb(23, 27, 24)" if current["theme"] == "dark" else "rgb(248, 247, 242)"
        ) and data["foreground"] == (
            "rgb(238, 239, 232)" if current["theme"] == "dark" else "rgb(40, 40, 32)"
        )
        if current["side"] == "question":
            data["passed"] = (
                data["themeMatches"]
                and data["imagesLoaded"]
                and not data["control"]
                and not data["rawMetadata"]
            )
            capture("front")
            complete(data)
            return
        if not (
            data["control"] == "INPUT"
            and data["type"] == "button"
            and data["hidden"]
            and data["expanded"] == "false"
        ):
            data["passed"] = False
            complete(data)
            return
        capture("closed")

        def clicked():
            def opened(value):
                opened = json.loads(value)
                data["opened"] = opened
                capture("open")
                # Space activates the focused input through native keyboard handling.
                QTest.keyClick(view.focusProxy() or view, Qt.Key.Key_Space)

                def closed():
                    def done(value):
                        data["closed"] = json.loads(value)
                        data["passed"] = (
                            data["themeMatches"]
                            and data["imagesLoaded"]
                            and not data["rawMetadata"]
                            and not opened["hidden"]
                            and opened["expanded"] == "true"
                            and bool(opened["text"])
                            and data["closed"]["hidden"]
                            and data["closed"]["expanded"] == "false"
                        )
                        complete(data)

                    page.runJavaScript(
                        "JSON.stringify({hidden:document.getElementById('rv-details').hidden,expanded:document.querySelector('.details-button').getAttribute('aria-expanded')})",
                        done,
                    )

                QTimer.singleShot(50, closed)

            page.runJavaScript(
                "JSON.stringify({hidden:document.getElementById('rv-details').hidden,expanded:document.querySelector('.details-button').getAttribute('aria-expanded'),text:document.getElementById('rv-details').innerText})",
                opened,
            )

        QTest.mouseClick(
            view.focusProxy() or view,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
            QPoint(round(data["x"]), round(data["y"])),
        )
        QTimer.singleShot(80, clicked)

    page.runJavaScript(
        """(() => {if(document.body?.dataset.reviewIndex!=="""
        + json.dumps(str(len(results)))
        + """||document.readyState!=='complete'||[...document.images].some(i=>!i.complete||!i.naturalWidth))return null;const b=document.querySelector('.details-button'),d=document.getElementById('rv-details');b?.scrollIntoView({block:'center'});const r=b?.getBoundingClientRect();return JSON.stringify({imagesLoaded:true,background:getComputedStyle(document.body).backgroundColor,foreground:getComputedStyle(document.body).color,control:b?.tagName||null,type:b?.type||null,label:b?.value||null,hidden:d?.hidden,expanded:b?.getAttribute('aria-expanded'),x:r?.x+r?.width/2,y:r?.y+r?.height/2,rawMetadata:document.body.innerText.includes('"aliases"')});})()""",
        ready,
    )


QTimer.singleShot(0, start)
QTimer.singleShot(240000, lambda: finish("Watchdog"))
app.exec()
report = json.loads((a.output / "review.json").read_text())
raise SystemExit(0 if report["passed"] else 1)
