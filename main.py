import getopt, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options

# First, gets the desired search param from command line arguments. Defaults to "how to use selenium" for demonstration purposes.
short_commands = "hs:"
long_commands = ["help", "search="]
query = "how to use selenium"
try:
    arguments, _ = getopt.getopt(sys.argv[1:], short_commands, long_commands)
except getopt.error as err:
    print (str(err))
    sys.exit()
for argument, value in arguments:
    if argument in ("-h", "--help"):
        print (" Use the -s or --search argument to customize your search. \n Example: \n py main.py -s \"how to tie a tie\"")
        sys.exit()
    elif argument in ("-s", "--search"):
        query = value

driver_options = Options()
driver_options.add_argument("--headless")
driver = webdriver.Chrome(options=driver_options)
driver.get("https://www.google.com/")
search = driver.find_element_by_name("q")
search.send_keys(query)
search.send_keys(Keys.RETURN)
try:
    WebDriverWait(driver, 2).until(
        expected_conditions.presence_of_element_located((By.ID, "fsl"))
    )
finally:
    # Gets elements with a search result (yuRUbf) that aren't children of the "people also ask" element (cUnQKe)
    results = driver.find_elements_by_xpath("""
        //*[
            @class='yuRUbf' 
            and not(
                ancestor::*[
                    contains(@class, 'cUnQKe')
                ]
            )
        ]""")
    breakline = "------------------"
    for result in results:
        print(breakline)
        # Class LC20lb is where the title text is stored
        print(result.find_element(By.CLASS_NAME, "LC20lb").text)
        print(result.find_element(By.TAG_NAME, "a").get_attribute('href'))
    print(breakline)
driver.quit()