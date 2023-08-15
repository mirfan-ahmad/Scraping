# import necessary modules
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
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


# def get_links():
#     i = 1
#     with open('remax-log-links.txt', 'a') as f:
#         while True:
#             try:
#                 anchor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.search-list > div > div:nth-child({i}) > div > div:nth-child(2) > a')))
#                 driver.execute_script("arguments[0].scrollIntoView();", anchor)
#                 f.write(anchor.get_attribute('href') + '\n')
#                 i += 1
#             except:
#                 try:
#                     next = driver.find_element(By.CSS_SELECTOR, 'li.pagination__next > a')
#                     driver.execute_script("arguments[0].scrollIntoView();", anchor)
#                     next.click()
#                     i = 1
#                 except Exception as e:
#                     print('Exception: ', e)
#                     input('Exception found:')
#                     return


def get_links():
    i = 1
    with open('remax-logo-links.txt', 'a') as f:
        while True:
            try:
                anchor = driver.find_element(By.CSS_SELECTOR, f'div.search-list > div > div:nth-child({i}) > div > div:nth-child(2) > a')
                driver.execute_script("arguments[0].scrollIntoView();", anchor)
                f.write(anchor.get_attribute('href') + '\n')
                i += 1
            except Exception as e:
                print('exception: ', e)
                return
    
    
def main():
    # Redirecting to the website
    for i in range(1, 43):
        url = f'https://www.remax.it/trova/ricerca/vendita/roma?agency_group_id&agency_id&agent_id&bathrooms&energy_class[]=1&energy_class[]=8&lifestyle&order=sell_price-desc&page={i}&price&program&rooms&size&unit_type_id=1&yard_id'
        
        driver.get(url)
        get_links()
    
        try:
            button = driver.find_element(By.CSS_SELECTOR, '#iubenda-cs-banner > div > div > div > div.iubenda-cs-opt-group > div.iubenda-cs-opt-group-consent > button.iubenda-cs-reject-btn.iubenda-cs-btn-primary')
            button.click()
        except:
            pass

def scrape_images(link):
    driver.get(link)
    sleep(2)
    i = 1
    exception = 1
    img_links = {}
    with open('remax-logo-img-links.txt', 'a') as f:    
        while True:
            try:
                img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#__layout > div > div.page-wrapper > div.unit-page > div:nth-child(1) > div > div.l-col-lg--8 > div > div.slider > div > div.slider__swiper.slider__big.swiper-container.swiper-container-initialized.swiper-container-horizontal > div > div:nth-child({i}) > figure > div > picture > img')))
                img_src = img.get_attribute('src')
                
                if i > 2 and img_src == img_links[1]:
                    for key, val in img_links.items():
                        f.write(val + '\n')
                    return
                else:
                    img_links[i] = img_src
                i += 1
                
                button = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div.page-wrapper > div.unit-page > div:nth-child(1) > div > div.l-col-lg--8 > div > div.slider > div > div.slider__next.slider-button.slider-button--right')
                button.click()
                
            except Exception as e:
                # print('Exception: ', e)
                for key, val in img_links.items():
                        f.write(val + '\n')
                return
    
    
if __name__ == '__main__':
    # main()
    with open('remax-logo-links.txt', 'r') as f:
        for i in tqdm(range(738)):
            link = f.readline().split('\n')[0]
            if link != '':
                scrape_images(link)

