def test_main_navigation(playwright):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch()
    context = browser.new_context()

    # Start tracing before creating / navigating a page.
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto("https://playwright.dev")

    # Stop tracing and export it into a zip archive.
    context.tracing.stop(path="trace.zip")
