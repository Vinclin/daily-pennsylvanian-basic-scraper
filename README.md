# Daily Pennsylvanian Multimedia Headline Scraper

This script scrapes the headline from the [Daily Pennsylvanian Multimedia page](https://www.thedp.com/multimedia) and saves it to a JSON file that tracks headlines over time.

## Overview

Originally, the scraper targeted the main headline section on the homepage. However, after evaluating different strategies to obtain a more engaging headline, the scraping rule was updated to focus on the Multimedia page. This page features the latest video or photo story, which is often more visually engaging and timely.

## Modifications

### New Scraping Rule

- **Target Page:**  
  The script now navigates to the Multimedia page at [https://www.thedp.com/multimedia](https://www.thedp.com/multimedia).

- **Headline Selection:**  
  The scraper searches for the first `<a>` element with the class `"media-headline"`, which is assumed to contain the headline of the latest video or photo story. This decision was made after analyzing the multimedia section’s HTML structure, where visual stories are prominently featured.

- **Error Handling:**  
  If the multimedia headline is not found, the script logs an error and returns a failure message. This ensures that any changes in the website’s HTML structure or unexpected issues are captured in the logs.

- **Improved Request Handling:**  
  A custom `User-Agent` header is added to mimic a real browser, helping to avoid HTTP errors that can occur when websites block non-browser requests.

### Updated Code Snippet

Below is the updated implementation of the `scrape_data_point()` function:

```python
def scrape_data_point():
    """
    Scrapes the headline of the latest video or photo story from The Daily Pennsylvanian Multimedia page.
    
    Returns:
        str: The headline text if found, otherwise an error message.
    """
    url = "https://www.thedp.com/multimedia"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.93 Safari/537.36"
        )
    }
    req = requests.get(url, headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    if not req.ok:
        loguru.logger.error("Failed to retrieve the multimedia page")
        return "failed: request error"
    
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    # Attempt to locate the latest multimedia headline
    target_element = soup.find("a", class_="media-headline")
    if target_element and target_element.text.strip():
        data_point = target_element.text.strip()
        loguru.logger.info(f"Data point: {data_point}")
        return data_point
    else:
        loguru.logger.error("Failed to find multimedia headline")
        return "failed: multimedia headline not found"
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
