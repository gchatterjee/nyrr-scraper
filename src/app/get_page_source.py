from tempfile import mkdtemp
from selenium import webdriver

import logging

logger = logging.getLogger("nyrr-scraper")


def get_page_source() -> str:
    logger.debug("creating selenium driver...")
    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/chrome/chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome("/opt/chromedriver", options=options)
    logger.debug("created selenium driver!")

    logger.debug("retrieving page...")
    driver.get("https://www.nyrr.org/fullraceyearindex")
    driver.set_page_load_timeout(30)
    logger.debug("retrieved page!")

    html = driver.page_source

    logger.debug("quitting selenium driver...")
    driver.quit()
    logger.debug("quit selenium driver!")

    return html
