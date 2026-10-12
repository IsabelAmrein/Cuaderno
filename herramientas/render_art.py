import pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "content" / "art"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 700, "height": 500})
    import sys; sys.path.insert(0, str(pathlib.Path(__file__).parent)); import art
    for name, fn in (("compass", lambda d: art.compass_scene(d, crop=True)), ("iceberg", art.iceberg_scene)):
        svg = fn(True).replace('class="motif"', 'style="width:680px;display:block"')
        pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
        pg.locator("svg").screenshot(path=str(ART / f"{name}.png"), omit_background=True)
        print("png", name)
    b.close()
