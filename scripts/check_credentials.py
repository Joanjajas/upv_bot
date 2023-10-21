import sys

from playwright.sync_api import sync_playwright


UPV_LOGIN_URL = "https://intranet.upv.es/"


def main():
    username = sys.argv[1]
    password = sys.argv[2]

    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    # Set default timeout to 5 seconds
    page.set_default_timeout(5000)

    check_credentials(page, username, password)


def check_credentials(page, username, password):
    try:
        # Navigate to login page
        page.goto(UPV_LOGIN_URL)

        # Fill login form and submit
        form = page.locator("form[name='alumno']")
        form.locator("input[name='dni']").fill(username)
        form.locator("input[name='clau']").fill(password)
        form.locator("input[type='submit']").click()

        # Check if login was successful
        assert page.title() == "Mi UPV"

    except AssertionError:
        exit(1)

    except Exception as err:
        print(err)
        exit(1)


if __name__ == "__main__":
    with sync_playwright() as playwright:
        main()
