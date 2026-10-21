import pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "content" / "art"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 700, "height": 500})
    import sys; sys.path.insert(0, str(pathlib.Path(__file__).parent)); import art
    for name, fn in (("compass", lambda d: art.compass_scene(d, crop=True)), ("iceberg", art.iceberg_scene), ("bins", lambda d: art.bins_scene(d, crop=True)), ("casa", art.casa_scene)):
        svg = fn(True).replace('class="motif"', 'style="width:680px;display:block"')
        pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
        pg.locator("svg").screenshot(path=str(ART / f"{name}.png"), omit_background=True)
        print("png", name)
    import importlib.util
    spec = importlib.util.spec_from_file_location("build", ROOT / "build.py"); build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
    ejemplo = [{"title": "", "url": "#"}] * 3
    svg = f'<svg viewBox="0 0 680 330" style="width:680px;display:block">{build.rumbo_svg(ejemplo, "es")}</svg>'
    pg.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
    pg.locator("svg").screenshot(path=str(ART / "rumbo.png"), omit_background=True)
    (ART / "rumbo.svg").write_text('<svg class="motif" viewBox="0 0 680 330" aria-hidden="true" focusable="false">' + build.rumbo_svg(ejemplo, "es", links=False) + "</svg>", encoding="utf-8")
    print("png y svg rumbo")
    b.close()
