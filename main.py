from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, ActionChains, Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import requests

list_of_downloaded_extensions = ['mp4', 'avi', 'webm', 'flw', 'mkv', 'mov', 'flac', 'mp3', 'ogg', 'ape', 'cue', 'log', 'txt', 'jpg', 'jpeg']

# url_to_files = 'http://192.168.1.103/Videos'
url_to_files = 'http://192.168.1.103/Muzic'
options = Options()
# options.add_argument("--headless")
options.add_argument("window-size=1600,800")
driver = webdriver.Chrome(options)
actions = ActionChains(driver)
time.sleep(1)
driver.get(url_to_files)
main_table = driver.find_element(By.TAG_NAME, 'table')
table_rows = main_table.find_elements(By.TAG_NAME, 'tr')
length_trs = len(table_rows)
trs_count = length_trs - 1
print("Rows count:" + str(len(table_rows)))
for current_row_index in range(3, trs_count):
    print("Index:" + str(current_row_index))
    tds = table_rows[current_row_index].find_elements(By.TAG_NAME, 'td')
    print("Tds count:" + str(len(tds)))
    url = tds[1].find_element(By.TAG_NAME, 'a')
    current_url = url.get_attribute('href')
    print(current_url)
    current_url_divide_by_point = current_url.split('.')
    current_file_extension = current_url_divide_by_point[-1]
    current_url_divide_by_slash = current_url.split('/')
    current_file_name = current_url_divide_by_slash[-1]
    print("Extension:" + current_file_extension)
    if current_file_extension in list_of_downloaded_extensions:
        # url.click()
        current_file_name = current_file_name.replace('%20', ' ')
        print("Now saving file:" + current_file_name)
        current_file = requests.get(current_url)
        open('./downloads/' + current_file_name, 'wb').write(current_file.content)
time.sleep(3)

driver.close()