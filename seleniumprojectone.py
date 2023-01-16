from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options , not sure if this needs to be used.
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd, time

# 1. Constants - We need to always do this
website = 'https://www.audible.com/search'
options = webdriver.ChromeOptions()
options.headless = True                   # Headless mode disables the browser from opening. Damn cool!
# options.add_argument('window-size=1920x1080')     # Add this for headlessmode, to get needed data
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(website)
# driver.maximize_window()

# 2. Pagination Nation
pagination = driver.find_element(By.XPATH, '//ul[contains(@class,"pagingElements")]')
last_page = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(last_page[-2].text)
print(f"last page is {last_page}")

for i in range(1, last_page+1):
# 3. Get the container for all the audible results
    # Explicit wait here: Wait until the element is located up to 5 sec
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,'adbl-impression-container ')))
    print("Container loaded.")
    # container = driver.find_element(By.CLASS_NAME,'adbl-impression-container ')
    books = container.find_elements(By.XPATH,'./li') # Just another way to get them individually
    title = [x.text for x in container.find_elements(By.XPATH, ".//h3[contains(@class, 'bc-heading')]")] # Remember to always add dots to determine that it is the current context!
    author_name = [x.text for x in container.find_elements(By.XPATH, './/li[contains(@class,"authorLabel")]')]
    run_time = [x.text for x in container.find_elements(By.XPATH, './/li[contains(@class,"runtimeLabel")]')]
    format = pd.DataFrame([title,author_name,run_time]).transpose()
    format.columns = ['title','author_name','run_time']
    format.to_csv(f"out_proj1/{i}books_headless.csv", index=False)
    print(f"Saving to out_proj1/{i}books_headless.csv")
    # Lets click the next button!
    try:
        next_button = driver.find_element(By.XPATH, '//span[contains(@class,"nextButton")]')
        next_button.click()
        print(f"Moving to next page... ({i+1})")
    except Exception as e:
        print("Error: {e}")
        continue

# Remember to quit it dude
x = input("Enter to quit...")
driver.quit()