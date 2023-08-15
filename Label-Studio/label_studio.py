from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchWindowException
from time import sleep
from tqdm import tqdm

Service = Service('/home/umair/Desktop/irfan/chromedriver_linux64/chromedriver')
driver = Chrome(service=Service)
driver.maximize_window()

wait = WebDriverWait(driver, 10)
driver.get('http://103.31.104.196:3105/')
sleep(2)
# toggle login
# driver.find_element(By.CSS_SELECTOR, '.toggle > a:nth-child(1)').click()
# username
driver.find_element(By.CSS_SELECTOR, '#login-form > p:nth-child(2) > input').send_keys('irfan.ahmad@axcelerate.ai')
# password
driver.find_element(By.CSS_SELECTOR, '#login-form > p:nth-child(3) > input').send_keys('Irfan@1122M')
# login - button
driver.find_element(By.CSS_SELECTOR, '#login-form > p:nth-child(5) > button').click()
sleep(1)
# copliance-detection
a = driver.find_element(By.CSS_SELECTOR, 
                    'body > div.app-wrapper > div > div.ls-content-wrapper__body > div > div > div > div.ls-projects-page__list > a:nth-child(2)')
link = a.get_attribute('href')
driver.get(link)
sleep(5)
# load div tag for image
img_links = []
i = 2
k = 1
while True:
    driver.find_element(By.CSS_SELECTOR, f'body > div.app-wrapper > div > div.ls-content-wrapper__body > div > div > div > div.dm-tabs-content > div > div.dm-data-view.dm-content > div > div > div > div > div:nth-child({i}) > div > div.dm-table__cell.dm-show-source > button').click()
    lnk = driver.find_element(By.CSS_SELECTOR, 'body > div.dm-modal.dm-modal_visible.dm-visible > div > div > div.dm-modal__body > pre')['data']['image']
    print(lnk)
    img_links.append(lnk)
    i += 1
    if i == 400:
        break

with open('links.txt', 'w') as f:
    for link in tqdm(img_links):
        f.write(link + '\n')