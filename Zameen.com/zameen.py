# import necessary modules
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
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


def get_links():
    i = 1
    with open('zameen-links.txt', 'a') as f:
        while True:
            try:
                anchor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'ul.new-projects > li.tile-spacing:nth-child({i}) > a')))
                driver.execute_script("arguments[0].scrollIntoView();", anchor)
                f.write(anchor.get_attribute('href') + '\n')
                i += 1
            except StaleElementReferenceException:
                driver.refresh()
                continue
            except:
                return
    

def scrape_images(link):
    driver.get(link)
    with open('zameen-logo-img-links.txt', 'a') as f:
        section = driver.find_element(By.CSS_SELECTOR, '#project_view_slider')
        section.click()
        sleep(2)
        i = 2
        li = driver.find_element(By.CSS_SELECTOR, '#\#popup-container-photo')
        li.click()
        sleep(1)
        while True:
            try:
                img = driver.find_element(By.XPATH, f'//*[@id="popup-container-photo"]/div[2]/div/div[2]/div/div/div[{i}]/div/img')
                img_src = img.get_attribute('src')
                f.write(img_src + '\n')
                i += 1
            except Exception as e:
                return


def main():
    # Redirecting to the website
    driver.get('https://www.zameen.com/new-projects/search.html')
    for i in tqdm(range(63)):
        get_links()
        
        try:
            next = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination_items > li')[-2]
            next.click()
        except Exception as e:
            print('Exception: ', e)
            return


if __name__ == '__main__':
    # main()
    
    with open('zameen-links.txt', 'r') as f:
        for i in tqdm(range(1303)):
            link = f.readline().split('\n')[0]
            # print(link)
            if link != '':
                scrape_images(link)
