"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data_point():
    """
    Scrapes the main headline from The Daily Pennsylvanian home page.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36"
        )
    }
    # 1. Fetch the webpage
    req = requests.get("https://www.thedp.com", headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    # 2. Parse the HTML
    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        # 3. Locate the "Most Read" section
        most_read_section = soup.find("span", id="mostRead")
        if not most_read_section:
            loguru.logger.error("Could not find the 'mostRead' span.")
            return "failed: mostRead span not found"

        # 4. Find the first row in the "Most Read" section
        rows = most_read_section.find_all("div", class_="row")
        first_row = rows[0] if rows else None
        if not first_row:
            loguru.logger.error("No 'row' div found in the 'mostRead' section.")
            return "failed: row div not found in mostRead section"
        
        # 5. Find the first "most-read-item"
        items = first_row.find_all("div", class_="col-sm-5 most-read-item")
        first_item = items[0] if items else None
        if not first_item:
            loguru.logger.error("No 'most-read-item' div found.")
            return "failed: most-read-item div not found"

        # 6. Extract the headline from the <a> tag
        headline_link = first_item.find("a", class_="frontpage-link standard-link")
        if not headline_link:
            loguru.logger.error("No article link found in the first most-read item.")
            return "failed: article link not found"

        # 7. Get the text of the headline
        headline_text = headline_link.get_text(strip=True)
        return headline_text

    else:
        loguru.logger.error("Request to the website failed.")
        return "failed: request failed"


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point is not None:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
