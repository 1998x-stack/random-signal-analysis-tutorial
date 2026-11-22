"""Browser QA for six reviewed textbook chapters, desktop/mobile and controls."""
from pathlib import Path
import argparse
import json
import sys
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="qa/chapter-review")
    args=ap.parse_args()
    dest=ROOT/args.output
    dest.mkdir(parents=True,exist_ok=True)
    issues=[]
    report={}
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for width in (1440,390,360):
            context=browser.new_context(viewport={"width":width,"height":900},
                    device_scale_factor=1, reduced_motion="reduce")
            page=context.new_page()
            console_errors=[]
            page.on("pageerror",lambda e:console_errors.append(str(e)))
            for num in range(1,7):
                uri=(ROOT/"chapters"/f"{num:02}.html").as_uri()
                page.goto(uri, wait_until="load")
                page.screenshot(path=str(dest/f"ch{num:02}-{width}.png"),full_page=True)
                result=page.evaluate("""() => {
                    const q=(sel)=>document.querySelector(sel);
                    const imgs=[...document.images];
                    const math=[...document.querySelectorAll('math')];
                    const broken=imgs.filter(x=>!x.complete||x.naturalWidth===0);
                    const eqWidth=math.filter(x=>x.getBoundingClientRect().width<1);
                    return {
                        overflow: document.documentElement.scrollWidth>innerWidth+1,
                        h1:document.querySelectorAll('h1').length,
                        images:imgs.length,
                        broken:broken.map(x=>x.src),
                        math:math.length,
                        collapsedMath:eqWidth.length,
                        title:document.title
                    }
                }""")
                key=f"{num:02}/{width}"
                report[key]=result
                if result["overflow"]: issues.append(f"{key}: document overflows horizontally")
                if result["h1"] != 1: issues.append(f"{key}: H1 count {result['h1']}")
                if result["broken"]: issues.append(f"{key}: broken images {result['broken']}")
                if result["collapsedMath"]: issues.append(f"{key}: collapsed math {result['collapsedMath']}")
                if console_errors: issues.append(f"{key}: JS errors {console_errors}")
                if num == 4:
                    slider=page.locator("#cheb-k")
                    slider.fill("4")
                    val=page.locator("#cheb-value").inner_text()
                    if "93.75%" not in val: issues.append(f"{key}: Chebyshev demo {val}")
                if num == 5:
                    slider=page.locator("#rayleigh-gamma")
                    slider.fill("0")
                    val=page.locator("#rayleigh-tail").inner_text()
                    if "100.000%" not in val: issues.append(f"{key}: Rayleigh demo {val}")
                if num == 6:
                    slider=page.locator("#process-lag")
                    slider.fill("0")
                    val=page.locator("#process-b").inner_text()
                    if val.strip()!="1": issues.append(f"{key}: process demo {val}")
            context.close()
        browser.close()
    (dest/"report.json").write_text(json.dumps({"results":report,"issues":issues},ensure_ascii=False,indent=2))
    for i in issues: print("FAIL:",i)
    print(f"Browser QA: {len(report)} screenshots; {len(issues)} issues")
    return 1 if issues else 0

if __name__=="__main__":
    sys.exit(main())
