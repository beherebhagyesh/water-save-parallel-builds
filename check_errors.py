from playwright.sync_api import sync_playwright

errors = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type in ("error","warning") else None)
    page.on("pageerror", lambda err: errors.append(f"[PAGEERROR] {err}"))
    page.goto('http://localhost:36900', timeout=15000)
    page.wait_for_timeout(3000)
    print("=== Console errors ===")
    for e in errors:
        print(e)
    print("=== Page title:", page.title())
    print("=== Body innerHTML length:", len(page.locator("body").inner_html()))
    browser.close()
