from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, TimeoutException
from time import sleep
from tqdm import tqdm


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-data-dir=/home/umair/Desktop/irfan/Scraping/')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
Service = Service('/home/umair/Desktop/irfan/chromedriver_linux64/chromedriver')
# Service = Service('/home/umair/Desktop/irfan/Scrapping/chromedriver linux64/chromedriver')


driver = Chrome(service=Service)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
driver.get('https://architizer.com/image-search/popular-images')
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.column-block:nth-child(1)')))


def scroll():
    ind = 25
    iterations = 1
    for i in tqdm(range(400)):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.column:nth-child({ind})')))
        except TimeoutException:
            input('time out exception should I start again?')
        except Exception as e:
            ind -= 12
            print('Exception Raised: ', e)
            print('Grid Finished')
            break
        ind += 12
        iterations += 1
    return ind


def scrape(ind):
    index = 1
    images_links = []
    driver.execute_script("window.scrollTo(0, 0);")
    try:
        sleep(5)
        img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.column-block:nth child({index})')))
        img.click()
        sleep(5)
        for i in tqdm(range(ind)):
            link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-iCfLBT'))).get_attribute('src')
            images_links.append(link)
            prev_button = driver.find_element(By.CSS_SELECTOR, 'a.sc-iqsfdx:nth-child(2)')
            prev_button.click()
            index += 1
    except NoSuchElementException:
        print('Images Completed')
        return images_links
    except NoSuchWindowException:
        print('No window found')
        return images_links
    except TimeoutException:
        print('Time out exception occured: server error / internet issue')
        return images_links
    except Exception as e:
        print('Exception:', e)
        print('completed')
        return images_links
    except:
        return images_links
    return images_links


ind = scroll()

images_links = scrape(ind)

with open('links.txt', 'w') as f:
    for link in tqdm(images_links):
        f.write(f'{link}\n')