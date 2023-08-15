# import necessary modules
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from reloading import reloading

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
    with open('dsquare-links.txt', 'a') as f:
        while True:
            try:
                anchor = driver.find_element(By.CSS_SELECTOR, f'div#listing_ajax_container > div:nth-child({i})  > div > div:nth-child(2) > h4 > a')
                driver.execute_script("arguments[0].scrollIntoView();", anchor)
                f.write(anchor.get_attribute('href') + '\n')
                i += 1
            except Exception as e:
                print('Exception:', e)
                return


def scrape_images(link):
    driver.get(link)
    
    section = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#all_wrapper > div > div.container.content_wrapper')))
    section.click()
    
    start = 14
    with open('dsquare-logo-img-links.txt', 'a') as f:
        while True:
            img = driver.find_element(By.CSS_SELECTOR, f'#owl-demo > div.owl-stage-outer > div > div:nth-child({start}) > div > img')
            img_src = img.get_attribute('src')
            
            f.write(img_src + '\n')
            start += 1
    

def main():
    for page_index in tqdm(range(1, 32)):
        driver.get(f'https://www.dsquare.com.mt/advanced-search/page/{page_index}/?search&bedrooms&advanced_contystate&advanced_city&price_low=0&price_max=5500000&filter_search_action%5B0%5D&filter_search_type%5B0%5D&submit=SEARCH%20PROPERTIES&wpestate_regular_search_nonce=24c4d1a524&_wp_http_referer=%2F')
        get_links()


if __name__ == '__main__':
    # main()
    
    @reloading
    with open('dsquare-links.txt', 'r') as f:
        for link in tqdm(f.readlines()):
            scrape_images(link.strip())
