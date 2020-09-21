import re
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


class InputPage:
    """
    Page Object encapsulates the Input page.
    """
    def __init__(self, driver):
        self.driver = driver
        # Construct By-object members
        self.query_by = {"by":By.NAME, "value":"q"}
        self.search_by = {"by":By.NAME, "value":"btnK"}
        # Loading check
        assert "Google" == self.driver.title, "This's NOT Google homepage."

    def input_query(self, query_content:str):
        input_field = self.driver.find_element(self.query_by["by"], self.query_by["value"])
        input_field.clear()
        input_field.send_keys(query_content)
        self.query_content = query_content
        # Return self for chained calling
        return self

    def click_search_button(self):
        WebDriverWait(self.driver, timeout=3).until(
            lambda dr: dr.find_element(self.search_by["by"],
                                       self.search_by["value"]).is_displayed())
        btn = self.driver.find_element(self.search_by["by"],
                                       self.search_by["value"])
        btn.click()
        # Browser will jump to another page after clicking search button
        return ResultPage(self.driver, self.query_content)


class ResultPage:
    """
    Page Object encapsulates the ResultPage.
    """
    def __init__(self, driver, query):
        self.driver = driver
        self.result_by = {"by": By.ID, "value": "rso"}

        # Both English and Chinese are considered below
        assert re.match("{} - Google (Search|搜索)".format(query), self.driver.title),\
            "Jump to related result page FAILED."

    def get_content(self):
        # Get information
        return self.driver.find_element(self.result_by['by'],
                                        self.result_by['value']).text


class Action:
    """
    Take actions on browser by calling member functions below.
    """
    def __init__(self):
        self.driver = None
        self.query = None
        self.result = None
        print("Welcome to the test. \n"
              "Please make sure Chrome browser is installed.\n"
              "Please keep the system focusing on the browser, do NOT hang it in the background.")
        time.sleep(6)  # Time for taking a look at the info above

    def start_browser(self, name:str="Chrome") ->None:
        if name == "Chrome":
            self.driver = Chrome()
        else:
            raise ValueError("Only Chrome browser is supported for now.")

    def navigate_to_google(self) -> None:
        self.driver.get("https://www.google.com")

    def search_with_google(self, query_content:str) -> None:
        if not query_content:
            raise ValueError("Search query should not be empty.")
        else:
            self.query = query_content
            input_page = InputPage(self.driver)
            result_page = input_page.input_query(query_content).click_search_button()
            self.result = result_page

    def is_searching_valid(self) -> bool:
        return self.query in self.result.get_content()

    def close_browser(self):
        self.driver.quit()


if __name__ == '__main__':
    act = Action()

    # Operations on the browser
    act.start_browser("Chrome")
    act.navigate_to_google()
    act.search_with_google("selenium")

    assert act.is_searching_valid(), "Searching with Google FAILED."

    act.close_browser()