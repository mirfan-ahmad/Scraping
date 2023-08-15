from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from tqdm import tqdm


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
Service = Service('/home/umair/Desktop/irfan/chromedriver_linux64/chromedriver')


driver = Chrome(service=Service)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

def scrape(anchors):
	with open('links.txt', 'w') as file:
		for i in tqdm(range(len(anchors))):
			try:
				driver.get(anchors[i])
				carousel = wait.until(EC.presence_of_element_located((By.ID, 'imageGallery')))
				total = driver.find_element(By.CSS_SELECTOR, 'span#ltslide-total').text.split()
				for ele in total:
					if ele.isdigit():
						global total_imgs
						total_imgs = int(ele)
				for i in tqdm(range(total_imgs)):
					img = driver.find_element(By.CSS_SELECTOR, f'#imageGallery > li:nth-child({i+2}) > img:nth-child({1})')
					link = img.get_attribute('src')
					file.write(f'{link}\n')
					next_button = driver.find_element(By.CSS_SELECTOR, '#gallery-photos-all > div > div > div > a.lSNext')
					next_button.click()
			except:
				pass

if __name__ == '__main__':
	anchors = []
	
	# Read the Links & store into anchors
	
	with open('links1.txt', 'r') as file:
		while True:
			link = file.readline()
			if link == '':
				break
			anchors.append(link)
	
	# scrape the link Images
	
	scrape(anchors)
