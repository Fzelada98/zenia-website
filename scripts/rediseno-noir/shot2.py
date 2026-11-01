import sys, time
from playwright.sync_api import sync_playwright
url, out, w = sys.argv[1], sys.argv[2], int(sys.argv[3])
wait = float(sys.argv[4]) if len(sys.argv) > 4 else 0
movil = w < 500
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": w, "height": 844 if movil else 900}, device_scale_factor=2 if movil else 1,
                        is_mobile=movil, has_touch=movil, locale="es-ES")
    pg = ctx.new_page()
    pg.goto(url, wait_until="networkidle", timeout=60000)
    try:
        pg.get_by_role("button", name="Aceptar").first.click(timeout=1500)
    except Exception:
        pass
    time.sleep(wait)
    y, h = 0, pg.evaluate("document.body.scrollHeight")
    while y < h:
        pg.evaluate(f"window.scrollTo(0,{y})"); time.sleep(0.1); y += 500; h = pg.evaluate("document.body.scrollHeight")
    pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.4)
    pg.add_style_tag(content=".nav{position:relative!important} .reveal{opacity:1!important;transform:none!important;transition:none!important} .msg{opacity:1!important;transform:none!important} *{animation-play-state:paused!important}")
    time.sleep(0.3)
    pg.screenshot(path=out, full_page=True)
    print(out, pg.evaluate("document.body.scrollHeight"), "overflowX:", pg.evaluate("document.documentElement.scrollWidth"), "vs", w)
    b.close()
