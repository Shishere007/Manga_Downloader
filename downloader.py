





# def download_chapter_pages(link_list, chapter, folder):
#     image_list = []
#     cnt = len(link_list)
#     for ind, url in enumerate(link_list):
#         ext = url.split(".")[-1]
#         page = str(ind + 1)
#         if len(page) == 1:
#             page = "0" + page
#         filename = folder + page + "." + ext
#         image_list.append((filename, url, ind+1, cnt))
#     print(f"Downloading {chapter}", end=" -> ")
#     thread_download(image_list)
#     print("\n")


def download_chapter(link, manga_name):
    soup = prepare_soup(link)
    img_list_temp = [item.attrs['src']
                     for item in soup.find(id='centerDivVideo').find_all('img')]
    # manga_name = format_manga_name(link.split("/")[-2])
    chapter = link.split("/")[-1].capitalize()
    chapter = manga_name.replace(" ", "_") + "_" + chapter
    create_folder(manga_name)
    folder = manga_name + "/" + chapter + "/"
    create_folder(folder)
    download_chapter_pages(img_list_temp, chapter, folder)
    folder = folder[:-1]
#     # system(f"7z a -tzip {folder}.zip {folder}")





# if __name__ == "__main__":
#     # link = 'https://kissmanga.org/chapter/read_horimiya_manga/chapter_27'
#     # download_chapter(link)
#     base = 'https://kissmanga.org'

#     # manga_name = "Horimiya"
#     manga_name = "Bokura Wa Minna Kawaisou"

#     div = ''
#     soup = BeautifulSoup(div, 'html.parser')

#     # div_list = soup.find_all('a',{'title':'Read Horimiya Manga online '})
#     div_list = soup.find_all(
#         'a', {'title': 'Read Bokura Wa Minna Kawaisou Manga online '})
#     link_list = [base+a.attrs['href'] for a in div_list[::-1]]
#     print(len(link_list))
#     for link in link_list[75:80]:
#         print(link)
#         download_chapter(link, manga_name)



import zipfile
from bin.KissManga import KissManga

# for i in KissManga().get_chapter_list('https://kissmanga.org/manga/yw925560'):
#     print(i)

import shutil

from os import path

# src = path.realpath(r'test\new file')
# print(src)

# shutil.make_archive(r'new file',"zip",src)

# from zipfile import  ZipFile

# a = ZipFile('test/new file.zip','w')
# a.close()


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

import time

# A List of Items
items = list(range(0, 57))
item_len = len(items)

# Initial call to print 0% progress
printProgressBar(iteration=0, total=item_len, prefix = 'Progress:', suffix = 'Complete', length = 100)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, total=item_len, prefix = 'Progress:', suffix = 'Complete', length = 100)


printProgressBar(iteration=0, total=item_len, prefix = 'Progress:', suffix = 'Complete', length = 100)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, total=item_len, prefix = 'Progress:', suffix = 'Complete', length = 100)


printProgressBar(iteration=0, total=item_len, prefix = 'Progress:', suffix = 'Complete', length = 100)
for i, item in enumerate(items):
    # Do stuff...
    time.sleep(0.1)
    # Update Progress Bar
    printProgressBar(i + 1, total=item_len, prefix = 'Progress:', suffix = 'Complete', length = 100)


