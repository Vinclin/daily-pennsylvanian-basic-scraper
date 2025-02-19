# Daily Pennsylvanian Headline Scraper

This script scrapes a headline from [The Daily Pennsylvanian website](https://www.thedp.com) and saves it to a JSON file that tracks headlines over time.

## Overview

Originally, the scraper targeted the main headline from the homepage. However, after evaluating different strategies for finding a more engaging headline, the scraping rule was updated. The new approach now targets the **"Most Read"** section on the homepage, which typically highlights the top trending article.

## Modifications

### New Scraping Rule

- **Target Section:**  
  The scraper now looks for the "Most Read" section by searching for a `<section>` element with an `id` of `"most-read"`. This section is expected to contain a list of articles ranked by popularity.

- **Headline Selection:**  
  From the "Most Read" section, the script extracts the first `<a>` element, which represents the #1 most read article. This article is assumed to be more relevant or interesting to readers compared to the main headline.

- **Fallback Mechanism:**  
  If the "Most Read" section is not found—perhaps due to changes in the website's HTML structure—the scraper logs a warning and falls back to the original method of extracting the main headline (using the `"frontpage-link"` CSS class).

- **Improved Request Handling:**  
  To help avoid HTTP 403 errors that can occur when the website blocks non-browser requests, a custom `User-Agent` header has been added to mimic a real browser.

### Updated Code Snippet

```python
def scrape_data_point():
    """
    Scrapes the #1 most read article headline from The Daily Pennsylvanian home page.
    
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
    req = requests.get("https://www.thedp.com", headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        # Attempt to locate the "Most Read" section
        most_read_section = soup.find("section", {"id": "most-read"})
        if most_read_section:
            # Get the first <a> tag within the section as the top most read headline
            target_element = most_read_section.find("a")
            loguru.logger.info("Found Most Read section.")
        else:
            loguru.logger.warning("Most Read section not found; falling back to main headline.")
            target_element = soup.find("a", class_="frontpage-link")
        data_point = "" if target_element is None else target_element.text.strip()
        loguru.logger.info(f"Data point: {data_point}")
        return data_point
    else:
        loguru.logger.error("Failed to retrieve the page; non-OK status.")
        return ""
  ```

## Setting Up a Local Development

It is recommended to use a version manager, and virtual environments and environment managers for local development of Python projects.

**asdf** is a version manager that allows you to easily install and manage multiple versions of languages and runtimes like Python. This is useful so you can upgrade/downgrade Python versions without interfering with your system Python.

**Pipenv** creates a **virtual environment** for your project to isolate its dependencies from other projects. This allows you to install packages safely without impacting globally installed packages that other tools or apps may rely on. The virtual env also allows reproducibility of builds across different systems.

Below we detail how to setup these environments to develop this template scrape project locally.

### Setting Up a Python Environment

Once you have installed `asdf`, you can install the Python plugin with:

```bash
asdf plugin add python
```

Then you can install the latest version of Python with:

```bash
asdf install python latest
```

After that, you can first install `pipenv` with:

```bash
pip install pipenv
```

### Installing Project Dependencies

Then you can install the dependencies with:

```bash
pipenv install --dev
```

This will create a virtual environment and install the dependencies from the `Pipfile`. The `--dev` flag will also install the development dependencies, which includes `ipykernel` for Jupyter Notebook support.

### Running the Script

You can then run the script to try it out with:

```bash
pipenv run python script.py
```

## Data Storage and Logging

### Data File

Scraped headlines are stored in data/daily_pennsylvanian_headlines.json. The file tracks headlines over time, with each entry timestamped.

### Logs

All operations are logged to scrape.log, providing a detailed runtime trace useful for troubleshooting and auditing.

## Conclusion

This update enhances the scraper by:

- Focusing on the most-read article to provide more engaging content.
- Implementing a fallback mechanism in case the “Most Read” section is absent.
- Improving request handling by adding a custom User-Agent header.

## Licensing

This software is distributed under the terms of the MIT License. You have the freedom to use, modify, distribute, and sell it for any purpose. However, you must include the original copyright notice and the permission notice found in the LICENSE file in all copies or substantial portions of the software.

You can [read more about the MIT license](https://choosealicense.com/licenses/mit/), and [compare different open-source licenses at `choosealicense.com`](https://choosealicense.com/licenses/).

## Some Ethical Guidelines to Consider

Web scraping is a powerful tool for gathering data, and its [legality has been upheld](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn).

But it is important to use it responsibly and ethically. Here are some guidelines to consider:

1. Review the website's Terms of Service and [`robots.txt`](https://en.wikipedia.org/wiki/robots.txt) file to understand allowances and restrictions for automated scraping before starting.

2. Avoid scraping copyrighted content verbatim without permission. Summarizing is safer. Use data judiciously under "fair use" principles.

3. Do not enable illegal or fraudulent uses of scraped data, and be mindful of security and privacy.

4. Check that your scraping activity does not overload or harm the website's servers. Scale activity gradually.

5. Reflect on whether scraping could unintentionally reveal private user or organizational information from the site.

6. Consider if scraped data could negatively impact the website's value or business model.

7. Assess if decisions made using the data could contribute to bias, discrimination or unfair profiling.

8. Validate quality of scraped data, and recognize limitations in ensuring relevance and accuracy inherent with web data.  

9. Document your scraping process thoroughly for replicability, transparency and accountability.

10. Continuously re-evaluate your scraping program against applicable laws and ethical principles.
