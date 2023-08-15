from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import json
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
Service = Service('/home/umair/Desktop/irfan/chromedriver_linux64/chromedriver')
driver = Chrome(service=Service)
driver.maximize_window()

wait = WebDriverWait(driver, 10)
driver.get('https://developers.google.com/earth-engine/datasets/catalog')
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#datasets-table > ul > li:nth-child(1) > div > table > tbody > tr:nth-child(1) > td > a')))

web_links = []
for i in tqdm(range(1, 599)):
    anchor = driver.find_element(By.CSS_SELECTOR, f'#datasets-table > ul > li:nth-child({i}) > div > table > tbody > tr:nth-child(1) > td > a')
    web_links.append(anchor.get_attribute('href'))


for link in tqdm(web_links):
    driver.get(link)
    grid = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#gc-wrapper > main > devsite-content > article > div.devsite-article-body.clearfix > div > div.ee-container > dl')))
    name = driver.find_element(By.CSS_SELECTOR, '#gc-wrapper > main > devsite-content > article > h1').text
    
    os.mkdir('Earth_Engine_Datasets/' + name)
    try:
        with open('Earth_Engine_Datasets/' + name + '/metadata.txt', 'w') as f:
            data_availability = grid.find_element(By.CSS_SELECTOR, 'dd:nth-child(2)').text
            earth_engine_snippet = grid.find_element(By.CSS_SELECTOR, 'dt:nth-child(6) > span > code').text
            driver.find_element(By.CSS_SELECTOR, '#aria-tab-bands:nth-child(1)').click()
            section = driver.find_element(By.CSS_SELECTOR, '#tabpanel-bands')
            f.write(f'data_availability: {data_availability}\nearth_engine_snippet: {earth_engine_snippet}\n')
            try:
                Resolution = section.find_element(By.CSS_SELECTOR, '#tabpanel-bands > p:nth-child(1)').text
                f.write(f'\nResolution: {Resolution}\n')
            except:
                pass
            f.close()
        try:
            index = 2
            Bands = {}
            with open('Earth_Engine_Datasets/' + name + f'/Bands.json', "w") as json_file:
                while True:
                    try:
                        tr = driver.find_element(By.CSS_SELECTOR, f'#tabpanel-bands > div:nth-child(3) > table > tbody > tr:nth-child({index})')
                        Bands[tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text] = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
                        index += 1
                    except:
                        json.dump(Bands, json_file)
                        break
        except:
            pass
        try:
            index = 2
            geomorphic_class_table = {}
            with open('Earth_Engine_Datasets/' + name + f'/geomorphic class table.json', "w") as json_file:
                while True:
                    try:
                        tr = driver.find_element(By.CSS_SELECTOR, f'#tabpanel-bands > div:nth-child(5) > table > tbody > tr:nth-child({index})')
                        color_description = [tr.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text, tr.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
                        geomorphic_class_table[tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text] = color_description
                        index += 1
                    except:
                        json.dump(geomorphic_class_table, json_file)
                        break
        except:
            pass
        try:
            index = 2
            benthic_class_table = {}
            with open('Earth_Engine_Datasets/' + name + f'/benthic class table.json', "w") as json_file:
                while True:
                    try:
                        tr = driver.find_element(By.CSS_SELECTOR, f'#tabpanel-bands > div:nth-child(7) > table > tbody > tr:nth-child({index})')
                        color_description = [tr.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text, tr.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
                        benthic_class_table[tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text] = color_description
                        index += 1
                    except:
                        json.dump(benthic_class_table, json_file)
                        break
        except:
            pass
        try:
            index = 2
            reef_mask_class_table = {}
            with open('Earth_Engine_Datasets/' + name + f'/reff_mask class table.json', "w") as json_file:
                while True:
                    try:
                        tr = driver.find_element(By.CSS_SELECTOR, f'#tabpanel-bands > div:nth-child(9) > table > tbody > tr:nth-child({index})')
                        color_description = [tr.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text, tr.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text]
                        reef_mask_class_table[tr.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text] = color_description
                        index += 1
                    except:
                        json.dump(reef_mask_class_table, json_file)
                        break
        except:
            pass
    except:
        pass
driver.quit()
