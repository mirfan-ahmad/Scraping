# import necessary modules
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
from time import sleep
from tqdm import tqdm

# Initialize the instance of chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-data-dir=/home/umair/Desktop/irfan/Scraping/')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
Service = Service('/home/umair/Desktop/irfan/chromedriver_linux64/chromedriver')

# initialize the driver
driver = Chrome(service=Service)
driver.maximize_window()
wait = WebDriverWait(driver, 10)


def get_links(url, iteration):
    driver.get(url)
    sleep(1)
    driver.find_element(By.CSS_SELECTOR, 'button.modal-cookie-only-necessary-button').click()
    with open('remax-links.txt', 'a') as f:
        for i in range(iteration):
            sleep(5)
            anchor = driver.find_elements(By.CSS_SELECTOR, 'div.card-slideshow-image-container > a')        
            for a in anchor:
                f.write(a.get_attribute('href') + '\n')
            driver.execute_script("arguments[0].scrollIntoView();", anchor[-1])
            try:
                driver.find_element(By.CSS_SELECTOR, 'li[data-test="pagination-next"]').click()
            except:
                return

get_links('https://www.remax.com/homes-for-sale/ca/san-francisco/city/0607592790', 81)
get_links('https://www.remax.com/homes-for-sale/ca/lancaster/city/0640130', 226)
get_links('https://www.remax.com/homes-for-sale/ca/san-diego/city/0666000', 110)
get_links('https://www.remax.com/homes-for-sale/ca/bakersfield/city/0603526', 82)
get_links('https://www.remax.com/homes-for-sale/ca/palmdale/city/0655156', 83)
get_links('https://www.remax.com/homes-for-sale/ca/apple-valley/city/0602364', 74)
get_links('https://www.remax.com/homes-for-sale/ca/long-beach/city/0643000', 52)
get_links('https://www.remax.com/homes-for-sale/ca/hemet/city/0633182', 70)
get_links('https://www.remax.com/homes-for-sale/ca/victorville/city/0682590', 63)

