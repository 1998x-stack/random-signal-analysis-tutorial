#!/usr/bin/env python3
"""Check canonical chapters, compatibility routes, SVGs, and local links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.h1 = 0
        self.math = 0
        self.cards = 0
        self.img_alt = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "math": self.math += 1
        if tag == "a" and "href" in a:
            self.links.append(("href", a["href"]))
            if "chapter-card" in a.get("class", "").split(): self.cards += 1
        if tag in ("img", "script", "link") and ("src" in a or "href" in a):
            self.links.append(("src", a.get("src", a.get("href"))))
        if tag == "img": self.img_alt.append(a.get("alt", ""))
        if "id" in a:
            if a["id"] in self.ids:
                ERRORS.append(f"duplicate id: {a['id']}")
            self.ids.add(a["id"])

def report(msg):
    ERRORS.append(msg)

def read(path):
    try:
        return (ROOT/path).read_text(encoding="utf-8")
    except FileNotFoundError:
        report(f"missing file: {path}")
        return ""

def parse(path):
    scan = Scan()
    scan.feed(read(path))
    for kind, href in scan.links:
        if not href or href.startswith(("#", "mailto:", "data:")): continue
        split = urlsplit(href)
        if split.scheme in ("https", "http"): continue
        if split.scheme:
            report(f"{path}: unsupported scheme {href}")
            continue
        if split.path:
            target = (ROOT/path).parent / unquote(split.path)
            if not target.is_file():
                report(f"{path}: broken local link {href}")
        if split.fragment:
            if split.path and (ROOT/path).parent.joinpath(split.path).suffix == ".html":
                target = ((ROOT/path).parent / unquote(split.path)).resolve()
                if target.exists():
                    other = Scan()
                    other.feed(target.read_text(encoding="utf-8"))
                    if unquote(split.fragment) not in other.ids:
                        report(f"{path}: missing anchor {href}")
            elif not split.path and unquote(split.fragment) not in scan.ids:
                report(f"{path}: missing anchor {href}")
    return scan

def main():
    data = json.loads(read(Path("courses.json")))
    chapters = data.get("chapters", [])
    if len(chapters) != 28: report("courses.json must have exactly 28 chapters")
    if [c.get("num") for c in chapters] != [f"{i:02}" for i in range(1,29)]:
        report("course numbers must cover 01 to 28 in order")
    for i, chapter in enumerate(chapters, 1):
        expected = f"chapters/{i:02}.html"
        if chapter.get("file") != expected:
            report(f"courses.json: expected {expected}")
        page = Path(expected)
        if i <= 6:
            scan = parse(page)
            if scan.h1 != 1: report(f"{page}: require one H1")
            if scan.math < 5: report(f"{page}: need multiple native MathML formulas")
            if i >= 4 and len(scan.img_alt) < 4: report(f"{page}: expected at least 4 explanatory images")
            if any(not alt.strip() for alt in scan.img_alt):
                report(f"{page}: image missing alt text")
        else:
            # Legacy chapters are checked for path integrity but not yet marked reviewed.
            if not (ROOT/page).is_file(): report(f"missing {page}")
        shim = read(Path(f"{i:02}.html"))
        if f"chapters/{i:02}.html" not in shim:
            report(f"root legacy path {i:02}.html lacks redirect")
    home = parse(Path("index.html"))
    if home.h1 != 1: report("index must have one H1")
    if home.cards != 28: report(f"index has {home.cards} static chapter cards, expected 28")
    parse(Path("chapters/index.html"))
    svgs = list((ROOT/"assets/svg").glob("*.svg"))
    if len(svgs) < 21: report("expected 21 original figures")
    for path in svgs:
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            namespace = "{http://www.w3.org/2000/svg}"
            if root.tag != namespace+"svg" or not root.attrib.get("viewBox"):
                report(f"{path}: invalid standalone SVG or missing viewBox")
            if root.find(namespace+"title") is None or root.find(namespace+"desc") is None:
                report(f"{path}: missing accessible title or desc")
            ids = [elem.attrib["id"] for elem in root.iter() if "id" in elem.attrib]
            if len(ids) != len(set(ids)): report(f"{path}: duplicate SVG ids")
        except ET.ParseError as exc:
            report(f"{path}: SVG parse error {exc}")
    if ERRORS:
        for err in ERRORS: print("ERROR:", err)
        print(f"FAILED: {len(ERRORS)} problems")
        return 1
    print(f"OK: {len(chapters)} chapters, 28 redirects, {home.cards} static cards, {len(svgs)} SVGs")
    return 0

if __name__ == "__main__":
    sys.exit(main())
