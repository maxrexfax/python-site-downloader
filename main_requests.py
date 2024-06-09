import os
import time
import requests
list_of_downloaded_extensions = ['mp4', 'MP4', 'avi', 'webm', 'flw', 'mkv', 'mov', 'flac', 'mp3', 'Mp3', 'MP3', 'ogg', 'ape', 'cue', 'log', 'txt', 'jpg', 'jpeg']
ArrOfCouplesToSaveFromAndWhere = [('http://192.168.1.103/', '/HDD/Muzic/')]
# ArrOfCouplesToSaveFromAndWhere = [('http://192.168.1.103/Videos/', './downloads/video/')]


def download_files():
    (url_to_files, folder_to_save) = ArrOfCouplesToSaveFromAndWhere[0]
    response = requests.get(url_to_files)
    content_as_string = response.text    

    if not os.path.exists(folder_to_save):
        os.makedirs(folder_to_save)
    # print(content_as_string)
    new_index_to_search = 0
    last_found_href_start = 0
    last_found_href_end = 0
    start_index_to_cut = content_as_string.find('<tr><th colspan="5"><hr></th></tr>', 0)
    end_index_to_cut = content_as_string.rfind('<tr><th colspan="5"><hr></th></tr>')

    print('start_index_to_cut:' + str(start_index_to_cut))
    print('end_index_to_cut:' + str(end_index_to_cut))
    start_index = start_index_to_cut + len('start_index_to_cut')
    content_as_string = content_as_string[start_index:end_index_to_cut]
    print(content_as_string)
    new_index_to_search = 0
    parent_directory = content_as_string.find('<img src="/icons/back.gif" alt="[PARENTDIR]">', new_index_to_search)
    if parent_directory != -1:
        new_index_to_search = parent_directory
    is_loop_works = True
    list_of_urls = []
    while is_loop_works:
        is_loop_works = False
        new_index_to_search = content_as_string.find('<tr>', new_index_to_search)
        if new_index_to_search != -1:
            is_loop_works = True
        last_found_href_start = content_as_string.find('a href="', new_index_to_search)
        last_found_a_close_tag = content_as_string.find('</a>', new_index_to_search)
        last_found_href_end = content_as_string.find('"', last_found_href_start + 9)
        current_slice = slice(last_found_href_start, last_found_a_close_tag)
        temporary_string_url = content_as_string[current_slice]
        new_index_to_search = last_found_a_close_tag
        print('temporary_string_url len:' + str(len(temporary_string_url)))
        print(temporary_string_url)
        if len(temporary_string_url) > 0:
            file_name = temporary_string_url.split(">",1)[1]
            if file_name[-1] == '/':#это папка - добавляем в массив обработки
                ArrOfCouplesToSaveFromAndWhere.append((url_to_files + file_name, folder_to_save + file_name))
            full_file_url = url_to_files + file_name
            print(full_file_url)
            file_name_divided_by_dot = file_name.split('.')
            current_file_extension = file_name_divided_by_dot[-1]
            try:
                if current_file_extension in list_of_downloaded_extensions:
                    file_name = file_name.replace('%20', ' ')
                    print("Now saving file:" + file_name)
                    current_file = requests.get(full_file_url)
                    open(folder_to_save + file_name, 'wb').write(current_file.content)
            except Exception as e:
                print("Exception With url:" + full_file_url + " and file:" + folder_to_save + file_name)
                print(e)
    ArrOfCouplesToSaveFromAndWhere.remove((url_to_files, folder_to_save))

def main_work():
    while len(ArrOfCouplesToSaveFromAndWhere) > 0:
        download_files()



print("Array length before:" + str(len(ArrOfCouplesToSaveFromAndWhere)))
# print(ArrOfCouplesToSaveFromAndWhere[0])
# for Key,Value in ArrOfCouplesToSaveFromAndWhere:
#     print(Key + "=" + Value)
#     ArrOfCouplesToSaveFromAndWhere.remove((Key, Value))
# print("Array length After:" + str(len(ArrOfCouplesToSaveFromAndWhere)))
main_work()

time.sleep(3)


# создаем массив с данными откуда скачивать и куда сохранять - пары
# заходим на урл, проходим всех, если это файл, то скачиваем, если это папка, сохряняем в массив будущих закачек - удаляем эту запись в массиве
# цикл повторяется для нового урла,
# если массив пуст, цикл разрываем
