from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time
import csv

url = "https://www.teamblind.com/jobs"

driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get(url)
driver.implicitly_wait(6)

companies_selector = driver.find_element(By.CSS_SELECTOR, ".css-2hgv4a:nth-child(6)")
companies_text = companies_selector.text
companies_selector.click()

popup = WebDriverWait(driver, 25).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".filter-modal-content"))
)
checkboxes = driver.find_elements(By.CSS_SELECTOR, ".css-1qsvuf4")
for checkbox in checkboxes:
    if checkbox.text == "1-50 employees":
        checkbox.click()
    # elif checkbox.text == "51-200 employees":
    #     checkbox.click()
    # elif checkbox.text == "201-500 employees":
    #     checkbox.click()
    else:
        None

apply_button = driver.find_element(By.CSS_SELECTOR, ".css-vfsjml")
apply_button.click()

time.sleep(1)

page_info = driver.find_element(By.CSS_SELECTOR, ".job_page_inactive:last-of-type")
page_count = int(page_info.text)

next_page = driver.find_element(By.CSS_SELECTOR, ".job_pagination_arrow:last-of-type")

links = []
titles = []

page = 1

print(page_count)

for page in range(1, page_count + 1):

    items = driver.find_elements(By.CSS_SELECTOR, ".job_wrapper")

    for item in items:
        item.click()
        item_title = item.find_element(
            By.CSS_SELECTOR, ".job_title p:nth-child(1)"
        ).text
        current_url = driver.current_url
        links.append(current_url)
        titles.append(item_title)
        driver.back()

    time.sleep(4)

    next_page.click()

driver.quit()
now = datetime.now()
filename = f"jobs_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "url"])
    writer.writerows(zip(titles, links))

print(f"Data saved to {filename}")
