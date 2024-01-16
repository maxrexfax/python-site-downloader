import io
import os
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, ActionChains, Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import requests
# -*- coding: utf-8 -*-
ArrOfCouplesToSaveFromAndWhere = [('http://192.168.1.103/Muzic/', './')]

(url_to_files, folder_to_save) = ArrOfCouplesToSaveFromAndWhere[0]
web_page = requests.get(url_to_files)
request_as_string = web_page.text
print(request_as_string)
# encoded_data = io.open(current_file.content, mode="r", encoding="utf-8")
# open(folder_to_save + 'files.html', 'wb').write(current_file.content)
# with open("files2.html", "w") as text_file:
#     text_file.write(encoded_data.read())
#     text_file.close()
