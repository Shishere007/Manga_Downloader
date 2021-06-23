
import requests
from bs4 import BeautifulSoup
from os import mkdir, system
import concurrent.futures
import multiprocessing
import re
import urllib.request
from tqdm import tqdm


__version__ = '1.0'

def prepare_soup(link: str) -> BeautifulSoup:
    html = requests.get(link)
    if html.status_code == 200:
        return BeautifulSoup(html.text, 'html.parser')
    return False


# def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
#     """
#     Call in a loop to create terminal progress bar
#     @params:
#         iteration   - Required  : current iteration (Int)
#         total       - Required  : total iterations (Int)
#         prefix      - Optional  : prefix string (Str)
#         suffix      - Optional  : suffix string (Str)
#         decimals    - Optional  : positive number of decimals in percent complete (Int)
#         length      - Optional  : character length of bar (Int)
#         fill        - Optional  : bar fill character (Str)
#         printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
#     """
#     percent = ("{0:." + str(decimals) + "f}").format(100 *
#                                                      (iteration / float(total)))
#     filledLength = int(length * iteration // total)
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
#     # Print New Line on Complete
#     if iteration == total:
#         print()


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
                urllib.request.urlretrieve(link, filename)
            else:
                link = 'http:' + link
                urllib.request.urlretrieve(link, filename)
        except Exception as e:
            if e.code == 403:
                try:
                    open(filename, 'wb').write(requests.get(link,stream=True).content)
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


if __name__ == "__main__":
    pass
