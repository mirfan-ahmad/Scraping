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

def scrape_data(url):
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    sleep(1)
    try:
        driver.find_element(By.CSS_SELECTOR, 'button.modal-cookie-only-necessary-button').click()
    except:
        pass
    
    container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.image-container:nth-child(1) > div:nth-child(1)')))
    container.click()
    sleep(2)

    with open('remax-img-links', 'a') as f:
        tag = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__layout > div > main > article > div.modal-wrapper > div > div.modal-content > div > div.gallery-slideshow.collapsed > div.h-10.flex.flex-row-reverse.lg\:flex-row.justify-between.items-center.px-2 > p > span')))
        iter = int(tag.text.split()[-1])
        for i in tqdm(range(iter)):
            try:
                img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.embla__slide:nth-child({i+1}) > img:nth-child(1)')))
            except NoSuchElementException:
                return
            
            link = img.get_attribute('src')
            f.write(link + '\n')

            try:
                btn = driver.find_element(By.CSS_SELECTOR, 'button.gallery-slideshow-btn:nth-child(2)')
                btn.click()
            except NoSuchElementException:
                return

            sleep(0.1)

with open('remax-links.txt', 'r') as f:
    while True:
        link = f.readline()
        if link != '':
            scrape_data(link)
        else:
            break
        