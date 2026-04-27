import os
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs"
)

# Create outputs folder if it does not exist
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# -------------------------------------------------
# Task 1: Class-based Context Manager for Selenium
# -------------------------------------------------

class SeleniumDriver:
    def __enter__(self):

        # Initialize Chrome WebDriver
        self.driver = webdriver.Chrome()

        # Maximize browser window
        self.driver.maximize_window()

        return self.driver

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):

        # Properly close browser session
        if self.driver:
            self.driver.quit()


def get_report_url():
    """
    Generate local file URL for report.html
    """
    report_file = os.path.join(
        BASE_DIR,
        "report.html"
    )
    return (
        "file:///" +
        report_file.replace("\\", "/")
    )

# -------------------------------------------------
# Task 2: Extract Table Data
# -------------------------------------------------
def handle_table_extraction(driver):
    print(
        "Executing Task 2: Table Extraction..."
    )
    try:

        wait = WebDriverWait(
            driver,
            20
        )

        # Wait for full page load
        wait.until(
            lambda d:
            d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        # Buffer for JavaScript-rendered content
        time.sleep(3)

        # -----------------------------------------
        # Locator 1: XPath
        # Find all divs
        # -----------------------------------------

        divs = driver.find_elements(
            By.XPATH,
            "//div"
        )

        header_names = [
            "Facility Type",
            "Visit Date",
            "Average Time Spent"
        ]

        table_container = None

        # Find dashboard section containing table
        for div in divs:

            text = div.text.strip()

            if (
                "Facility Type" in text
                and "Visit Date" in text
                and "Average Time Spent" in text
            ):
                table_container = div
                break

        if not table_container:
            raise Exception(
                "Table container not found"
            )

        # -----------------------------------------
        # Locator 2: Class Name
        # -----------------------------------------

        cells = table_container.find_elements(
            By.CLASS_NAME,
            "cell-text"
        )

        # -----------------------------------------
        # Locator 3: CSS Selector fallback
        # -----------------------------------------

        if not cells:

            cells = table_container.find_elements(
                By.CSS_SELECTOR,
                "div, span"
            )

        values = [
            c.text.strip()
            for c in cells
            if c.text.strip()
        ]

        if not values:
            raise Exception(
                "No table values found"
            )

        print(
            f"Extracted values: {len(values)}"
        )

        # Remove duplicated headers
        values = [
            v for v in values
            if v not in header_names
        ]

        # Convert flat list into rows
        rows = []

        col_count = len(
            header_names
        )

        for i in range(
            0,
            len(values),
            col_count
        ):

            row = values[
                i:i+col_count
            ]

            if len(row) == col_count:
                rows.append(
                    row
                )

        if not rows:
            raise Exception(
                "No rows extracted"
            )

        # Save CSV
        table_csv = os.path.join(
            OUTPUT_DIR,
            "table.csv"
        )

        with open(
            table_csv,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow(
                header_names
            )

            writer.writerows(
                rows
            )

        print(
            f"Table saved: {table_csv}"
        )

    except Exception as e:
        print(
            "Table extraction failed"
        )
        print(
            type(e).__name__
        )
        print(e)

# -------------------------------------------------
# Task 3: Doughnut Chart Interaction
# -------------------------------------------------

def handle_chart_interaction(driver):
    print(
        "Executing Task 3: Doughnut Chart Interaction..."
    )

    try:

        wait = WebDriverWait(
            driver,
            15
        )

        wait.until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "pielayer"
                )
            )
        )

        actions = ActionChains(
            driver
        )

        # Save initial screenshot
        screenshot0 = os.path.join(
            OUTPUT_DIR,
            "screenshot0.png"
        )

        driver.save_screenshot(
            screenshot0
        )

        # Find chart filters
        filters = driver.find_elements(
            By.CLASS_NAME,
            "traces"
        )

        print(
            f"Filters found: {len(filters)}"
        )

        # Iterate through filters
        for i in range(
            len(filters)
        ):

            try:

                # Re-find elements after each click
                filters = driver.find_elements(
                    By.CLASS_NAME,
                    "traces"
                )

                current_filter = filters[i]

                actions.move_to_element(
                    current_filter
                ).click().perform()

                # Wait for chart update
                time.sleep(2)

                # Save screenshot
                screenshot_path = os.path.join(
                    OUTPUT_DIR,
                    f"screenshot{i+1}.png"
                )

                driver.save_screenshot(
                    screenshot_path
                )

                # Extract chart data
                labels = driver.find_elements(
                    By.CSS_SELECTOR,
                    "text.slicetext"
                )

                csv_rows = [
                    [
                        "Facility Type",
                        "Min Average Time Spent"
                    ]
                ]

                for label in labels:

                    tspans = label.find_elements(
                        By.TAG_NAME,
                        "tspan"
                    )

                    if len(
                        tspans
                    ) >= 2:

                        category = (
                            tspans[0]
                            .get_attribute(
                                "textContent"
                            )
                            .strip()
                        )

                        value = (
                            tspans[1]
                            .get_attribute(
                                "textContent"
                            )
                            .strip()
                        )

                        csv_rows.append(
                            [
                                category,
                                value
                            ]
                        )

                # Edge case:
                # all filters unselected
                if len(
                    csv_rows
                ) == 1:

                    csv_rows.append(
                        [
                            "No data",
                            "N/A"
                        ]
                    )

                # Save doughnut CSV
                chart_csv = os.path.join(
                    OUTPUT_DIR,
                    f"doughnut{i}.csv"
                )

                with open(
                    chart_csv,
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    writer = csv.writer(
                        file
                    )

                    writer.writerows(
                        csv_rows
                    )

                print(
                    f"Filter {i+1} processed"
                )

            except Exception as filter_error:

                print(
                    f"Filter {i+1} failed"
                )

                print(
                    filter_error
                )

        print(
            "Chart interaction completed."
        )

    except Exception as e:

        print(
            "Chart interaction failed"
        )

        print(
            type(e).__name__
        )

        print(e)
# -------------------------------------------------
# Main
# -------------------------------------------------
if __name__ == "__main__":

    url = get_report_url()

    with SeleniumDriver() as driver:

        driver.get(
            url
        )

        # Wait until page fully loads
        WebDriverWait(
            driver,
            20
        ).until(
            lambda d:
            d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        handle_table_extraction(
            driver
        )

        handle_chart_interaction(
            driver
        )
