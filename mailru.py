import os
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, ActionChains, Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By

main_url = 'https://cloud.mail.ru/'
url_to_files = 'https://cloud.mail.ru/home/Games/Digger'
options = Options()
options.add_extension('./extensions/Browsec-VPN.crx')
# options.add_argument("--headless")
options.add_argument("window-size=1600,800")
driver = webdriver.Chrome(options)
driver.page_source.encode('utf-8')
actions = ActionChains(driver)


time.sleep(5)
driver.get(main_url)
time.sleep(61)
driver.get(url_to_files)
main_container = driver.find_element('//div[@id="reactApp"]')
items_container = main_container.find_element('//div[@id="VirtualList__root--2_JbO"')
list_of_urls = items_container.find_elements('//a[@class="class="DataListItem__root--CNJMg"]')
for url in list_of_urls:
    ActionChains(driver) \
        .context_click(url) \
        .perform()
    driver.find_element('//div[@data-name="download"]').click()
time.sleep(1)

