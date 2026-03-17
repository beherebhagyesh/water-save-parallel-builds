"""Run full pipeline audit: load sample → run analysis → screenshot every tab with data."""
from playwright.sync_api import sync_playwright
import time

BASE = "http://localhost:36900"
OUT  = "prototypes/audit"

import os
os.makedirs(OUT, exist_ok=True)

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1360, "height": 900})
    page.on("console", lambda m: errors.append(f"[{m.type}] {m.text}") if m.type in ("error","warning") else None)
    page.on("pageerror", lambda e: errors.append(f"[PAGEERROR] {e}"))

    page.goto(BASE)
    page.wait_for_load_state("networkidle", timeout=60000)
    page.screenshot(path=f"{OUT}/00_initial.png")

    # --- Tab 0: Load sample parcel ---
    print("Loading sample parcel...")
    page.get_by_role("button", name="Load sample").click()
    page.wait_for_timeout(1000)
    page.screenshot(path=f"{OUT}/01_sample_loaded.png")

    # --- Run analysis ---
    print("Running analysis...")
    page.get_by_role("button", name="RUN ANALYSIS").click()
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/02_running.png")

    # Wait up to 90s for run to complete (look for Results tab becoming active or status change)
    print("Waiting for completion (up to 90s)...")
    for i in range(90):
        time.sleep(1)
        body = page.locator("body").inner_html()
        if "View full Results" in body or "No analysis run yet" not in body:
            # Check if we're seeing results or still loading
            status_els = page.locator(".material-symbols-outlined").all()
            # Look for "check_circle" or any sign of completion
            txt = page.locator("main").inner_text()
            if "View full Results" in txt or "Last Run" in txt:
                print(f"  Run completed at {i+1}s")
                break
            # Also check if status message changed
            try:
                status = page.locator("text=/RUNNING|elapsed/").count()
                if status == 0 and i > 10:
                    print(f"  Status cleared at {i+1}s, may be done")
                    break
            except:
                pass

    page.wait_for_timeout(2000)
    page.screenshot(path=f"{OUT}/03_after_run.png")

    # --- Navigate to Results tab ---
    print("Screenshotting Results tab...")
    page.locator("button").filter(has_text="Results").click()
    page.wait_for_timeout(1500)
    page.screenshot(path=f"{OUT}/04_results_top.png")
    # Scroll down to see more
    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/04_results_scroll.png")
    page.evaluate("window.scrollTo(0, 0)")

    # --- Field Conditions tab ---
    print("Screenshotting Field Conditions tab...")
    page.locator("button").filter(has_text="Field Conditions").click()
    page.wait_for_timeout(3000)  # Wait for API calls
    page.screenshot(path=f"{OUT}/05_field_top.png")
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/05_field_scroll.png")
    page.evaluate("window.scrollTo(0, 0)")

    # --- Economics tab ---
    print("Screenshotting Economics tab...")
    page.locator("button").filter(has_text="Economics").click()
    page.wait_for_timeout(2000)
    page.screenshot(path=f"{OUT}/06_econ_top.png")
    page.evaluate("window.scrollTo(0, 600)")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/06_econ_scroll.png")
    page.evaluate("window.scrollTo(0, 0)")

    # --- 3D Viewer tab ---
    print("Screenshotting 3D Viewer tab...")
    page.locator("button").filter(has_text="3D Viewer").click()
    page.wait_for_timeout(4000)  # 3D scene loads slower
    page.screenshot(path=f"{OUT}/07_3d_top.png")
    page.evaluate("window.scrollTo(0, 500)")
    page.wait_for_timeout(500)
    page.screenshot(path=f"{OUT}/07_3d_scroll.png")
    page.evaluate("window.scrollTo(0, 0)")

    # --- System tab ---
    print("Screenshotting System tab...")
    page.locator("button").filter(has_text="System").click()
    page.wait_for_timeout(1000)
    page.screenshot(path=f"{OUT}/08_system.png")

    browser.close()

print("\n=== Console errors ===")
for e in errors:
    print(e)
print(f"\nScreenshots saved to {OUT}/")
