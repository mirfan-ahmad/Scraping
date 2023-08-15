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

# load links dataset
df = pd.read_csv('anchors.csv')
links = df.iloc[:, -1].to_list()

# write data into text file
def write_data(img_links):
    with open('imgs_links.txt', 'a') as f:
        for img_link in img_links:
            f.write(img_link + '\n')


# scrape the links of images and write into the text file
def scrape(element):
    element.click()
    sleep(2)
    img_links = []
    i = 1
    while True:
        if i == 50:
            write_data(img_links)
            break

        try:
            cs = f'#top > section.master > div:nth-child(7) > div.csgp-modal-container.csgp-modal-dialog.container > div > section > section > div.carousel-theme-light.carousel.has-filmstrip.ng-scope > div > div > div.carousel-inner > div.slide.ng-isolate-scope.active:nth-child({i}) > figure > img'
            img_link = driver.find_element(By.CSS_SELECTOR, cs).get_attribute('src')
            
            if img_link not in img_links:
                img_links.append(img_link)
            else:
                return

            button = driver.find_element(By.CSS_SELECTOR, '#top > section.master > div:nth-child(7) > div.csgp-modal-container.csgp-modal-dialog.container > div > section > section > div.carousel-theme-light.carousel.has-filmstrip.ng-scope > div > div > button.carousel-control.ln-icon-rightnext-hollow')
            button.click()
            i += 1

        except NoSuchElementException:
            i += 1
            button = driver.find_element(By.CSS_SELECTOR, '#top > section.master > div:nth-child(7) > div.csgp-modal-container.csgp-modal-dialog.container > div > section > section > div.carousel-theme-light.carousel.has-filmstrip.ng-scope > div > div > button.carousel-control.ln-icon-rightnext-hollow')
            button.click()
            pass

# loop over the load dataset
def loop_over():
    for link in tqdm(links):
        driver.get(link)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mosaic-profile > div.mosaic-carousel > div.mosaic-tile.photo-maintain-ratio')))
        scrape(element)

if __name__ == '__main__':
    loop_over()
