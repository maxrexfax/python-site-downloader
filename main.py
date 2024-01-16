import os
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, ActionChains, Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import requests
# -*- coding: utf-8 -*-
list_of_downloaded_extensions = ['mp4', 'MP4', 'avi', 'webm', 'flw', 'mkv', 'mov', 'flac', 'mp3', 'Mp3', 'MP3', 'ogg', 'ape', 'cue', 'log', 'txt', 'jpg', 'jpeg']
# ArrOfCouplesToSaveFromAndWhere = [('http://192.168.1.103/Muzic/', './downloads/music/')]
ArrOfCouplesToSaveFromAndWhere = [('http://192.168.1.103/Videos/', './downloads/video/')]


def download_files(driver):
    (url_to_files, folder_to_save) = ArrOfCouplesToSaveFromAndWhere[0]
    driver.get(url_to_files)
    if not os.path.exists(folder_to_save):
        os.makedirs(folder_to_save)
    time.sleep(1)
    main_table = driver.find_element(By.TAG_NAME, 'table')
    table_rows = main_table.find_elements(By.TAG_NAME, 'tr')
    length_trs = len(table_rows)
    trs_count = length_trs - 1
    # print("Rows count:" + str(len(table_rows)))
    for current_row_index in range(3, trs_count):
        # print("Index:" + str(current_row_index))
        tds = table_rows[current_row_index].find_elements(By.TAG_NAME, 'td')
        # print("Tds count:" + str(len(tds)))
        url = tds[1].find_element(By.TAG_NAME, 'a')
        text_in_url = url.text
        # print("Got text inside url:" + text_in_url)
        current_url_href = url.get_attribute('href')
        # print('current_url_href:' + current_url_href)  # если урл кончается на / то это не файл а папка
        # сначала сохраняем все файлы, потом начинаем лазить по папкам или что то другое придумать
        # папку надо отдать в таккую же функцию рекурсивно
        if current_url_href[-1] == '/':
            # print("Folder found")
            # folder_name = current_url_href.split('/')[-2]
            folder_name = text_in_url
            # print("folder_name:" + folder_name)
            # print("New URL:" + url_to_files + folder_name)
            # print("New path to save:" + folder_to_save + folder_name)
            # создать папку, потом отдавать на сохранение
            newpath = folder_to_save + folder_name
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            folder_name = folder_name.replace('%20', ' ')
            ArrOfCouplesToSaveFromAndWhere.append((url_to_files + folder_name, folder_to_save + folder_name))
        current_url_divide_by_point = current_url_href.split('.')
        current_file_extension = current_url_divide_by_point[-1]
        current_url_divide_by_slash = current_url_href.split('/')
        # current_file_name = current_url_divide_by_slash[-1]
        current_file_name = text_in_url
        # print("Extension:" + current_file_extension)
        # ниже проверка только по совпадению расширения файла
        if current_file_extension in list_of_downloaded_extensions:
            current_file_name = current_file_name.replace('%20', ' ')
            # print("Now saving file:" + current_file_name)
            current_file = requests.get(current_url_href)
            open(folder_to_save + current_file_name, 'wb').write(current_file.content)
    ArrOfCouplesToSaveFromAndWhere.remove((url_to_files, folder_to_save))

def main_work(driver):
    while len(ArrOfCouplesToSaveFromAndWhere) > 0:
        download_files(driver)



# url_to_files = 'http://192.168.1.103/Videos/'
# url_to_files = 'http://192.168.1.103/Muzic/'
options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1600,800")
driver = webdriver.Chrome(options)
driver.page_source.encode('utf-8')
actions = ActionChains(driver)
time.sleep(1)

print("Array length before:" + str(len(ArrOfCouplesToSaveFromAndWhere)))
# print(ArrOfCouplesToSaveFromAndWhere[0])
# for Key,Value in ArrOfCouplesToSaveFromAndWhere:
#     print(Key + "=" + Value)
#     ArrOfCouplesToSaveFromAndWhere.remove((Key, Value))
# print("Array length After:" + str(len(ArrOfCouplesToSaveFromAndWhere)))
main_work(driver)

time.sleep(3)

driver.close()

# создаем массив с данными откуда скачивать и куда сохранять - пары
# заходим на урл, проходим всех, если это файл, то скачиваем, если это папка, сохряняем в массив будущих закачек - удаляем эту запись в массиве
# цикл повторяется для нового урла,
# если массив пуст, цикл разрываем