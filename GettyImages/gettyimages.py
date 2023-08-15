# import necessary modules
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tqdm import tqdm
from time import sleep


# Initialize the instance of Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--user-data-dir=/home/umar/Desktop/irfan/Scraping/')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
service = Service('/home/umair/Desktop/irfan/chromedriver_linux64/chromedriver')

# initialize the driver
driver = Chrome(service=service)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

def get_links():
    with open('getty-images.txt', 'a') as f:
        for i in tqdm(range(1, 101)):
            url = f'https://www.gettyimages.com/photos/person-in-house?assettype=image&page={i}&phrase=person%20in%20house&sort=mostpopular&license=rf,rm'
            driver.get(url)

            div_index = 1
            while True:
                
                if div_index == 31:
                    div_index += 1
                    continue
                
                try:
                    img_src = driver.find_element(By.CSS_SELECTOR, f"body > div.content_wrapper > section > div > main > div > div > div:nth-child(4) > div.CUAucfZwr8YyEhr4USsh > div.zF13TZBfnku4pwItorUU > div:nth-child({div_index}) >  article > a > figure > picture > img")
                    driver.execute_script('arguments[0].scrollIntoView(true);', img_src)
                    f.write(img_src.get_attribute('src') + '\n')

                except Exception as e:
                    break
                
                div_index += 1


if __name__ == "__main__":
    get_links()
