import os
import requests
from bs4 import BeautifulSoup
from os import mkdir
import concurrent.futures
import re
import urllib.request
from tqdm import tqdm
from pathlib import Path
import shutil

__version__ = '1.0'

def prepare_soup(link: str) -> BeautifulSoup:
    html = requests.get(link)
    if html.status_code == 200:
        return BeautifulSoup(html.text, 'html.parser')
    return False

def create_folder(foldername):
    try:
        mkdir(foldername)
        return True
    except FileExistsError:
        return False


def format_manga_name(manga: str):
    manga = manga.lower()
    manga = manga.replace("read", "")
    manga = manga.replace('manga', "")
    if manga[0] in [" ", "_"]:
        manga = manga[1:]
    if manga[-1] in [" ", "_"]:
        manga = manga[:-1]
    return manga.capitalize()


def download_chapter(current_chapter: str, image_list: list) -> None:
    '''
    @param
    current_chapter (str)   :   Chpater 1
    image_list      (list)  :   [(filename,url)]
    '''
    image_count = len(image_list)
    prefix = f"{current_chapter} :"
    progess_bar = tqdm(iterable=range(image_count),desc=current_chapter, total=image_count, unit="img",)
    
    def download_image(image):
        try:
            filename = image[0]
            link = image[1]
            flag = True
            if link.startswith("http") or link.startswith('https'):
                open(filename, 'wb').write(requests.get(link,stream=True).content)
            else:
                link = 'http:' + link
                open(filename, 'wb').write(requests.get(link,stream=True).content)
                # urllib.request.urlretrieve(link, filename)
        except Exception as e:
            if e.code == 403:
                try:
                    urllib.request.urlretrieve(link, filename) 
                    # open(filename, 'wb').write(requests.get(link,stream=True).content)
                except Exception as e:
                    # print(e)
                    flag = False
            else:
                flag = False
        finally:
            progess_bar.update(1)
            return flag

    # def download_image(image):
    #     ind = image[0]
    #     filename = image[1][0]
    #     url = image[1][1]
    #     open(filename, 'wb').write(requests.get(url).content)
    #     # printProgressBar(iteration=ind + 1, total=image_count,
    #     #                  prefix=prefix, suffix='Complete', length=100)

    POOL_SIZE = 2 #multiprocessing.cpu_count()
    # print(f"allotting {POOL_SIZE} threads for multiprocessing")
    with concurrent.futures.ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
        executor.map(download_image, [link for ind,link in enumerate(image_list)])
    # for ind, link in enumerate(image_list):
    #     download_image(link)


def clear_name(chapter_name):
    chapter_name = chapter_name.replace("\n", " ")
    while True:
        spaces = re.findall(r'\s\s+', chapter_name)
        if spaces:
            chapter_name = chapter_name.replace(spaces[0], " ")
        else:
            return chapter_name


def format_manga_name(manga_name: str) -> str:
    return manga_name.replace(" ", "_")

def to_zip(folder:str) -> None:
    for fold in Path(folder).glob('*'):
        if fold.is_dir():
            # zip_filename = str(fold) + ".zip"
            shutil.make_archive(str(fold),'zip',str(fold))
            shutil.rmtree(str(fold))

if __name__ == "__main__":
    # pass
    to_zip('Nan Hao & Shang Feng')
