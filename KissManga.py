import tools
from manga_site_base import MangaSite

__author__ = "Shishere"
__version__ = "1.2"


class KissManga(MangaSite):
    def __init__(self, manga_link: str, manga_name: str = None,zip:bool=True) -> None:
        super().__init__(manga_link, manga_name=manga_name, zip=zip)
        self.__base_url = 'https://kissmanga.org'
        # self.__search = f"https://kissmanga.org/manga_list?q={self.manga_name.replace(' ','+')}&action=search"

        self.manga_name = manga_name
        self.manga_link = manga_link
        self.zip = zip

        self.__chapter_list_main_div_className = 'listing listing8515 full'
        self.__pages_div_id = 'centerDivVideo'
        # self.__search_manga_div_className = 'item_movies_in_cat '
        # self.__search_manga_pager_className = 'pager'

        self.chapter_list = []
        self.chapter_count = 0

    # def search(self) -> list:
    #     '''
    #     return (list)   :   [{'mange_name':'name','manga_link',:'link','status':'status'}]
    #     '''
    #     soup = tools.prepare_soup(link=self.__search)
    #     if not soup:
    #         return False
    #     search_list = []
    #     def update_manga_list(soup:BeautifulSoup)->None:
    #         mangas = soup.find_all('div',{'class':self.__search_manga_div_className})
    #         for manga in mangas:
    #             div_list = manga.findchildren()
    #             manga_name = tools.clear_name(div_list[0].text.strip())
    #             manga_link = self.__base_url + manga.find_all('a')[0].attrs['href']
    #             status = tools.clear_name(div_list[1].text.strip())
    #             search_list.append(
    #                 {
    #                     'manga_name':manga_name,
    #                     'manga_link':manga_link,
    #                     'status':status
    #                 }
    #             )
    #     update_manga_list(soup)
    #     pager = soup.find_all('ul',{'class':self.__search_manga_pager_className})[0].findAll('li')[1:]
    #     for page in pager:
    #         soup = tools.prepare_soup(link=self.__base_url+page.find_all('a')[0].attrs['href'])
    #         update_manga_list(soup)

    #     return search_list

    def get_chapter_list(self, ) -> list:
        '''
        return [{chapter:'',link:''}]
        '''
        # self.manga_link = manga_link
        soup = tools.prepare_soup(link=self.manga_link)
        if not soup:
            return False
        if self.manga_name in [None, "", " "]:
            self.manga_name = soup.find_all('div', {'class': 'barContent full'})[0].find_all('strong', {'class': 'bigChar'})[0].text.strip()

        chapter_div_list = soup.find_all('div', {'class': self.__chapter_list_main_div_className})[0].find_all('a')
        
        for a in chapter_div_list[::-1]:
            if 'title' in a.attrs:
                if a.attrs['title'].__contains__('Read'):
                    self.chapter_list.append(
                        {
                            'chapter': tools.clear_name(a.text.strip()),
                            'link': self.__base_url + a.attrs['href']
                        }
                    )
        self.chapter_count = len(self.chapter_list)
        return self.chapter_list

    def download_chapter(self, chapter: dict) -> None:
        '''
        @param
        chapter (dict)  :   {"chapter":"chapter","link":"link"}
        '''

        chapter_link = chapter.get('link')
        soup = tools.prepare_soup(link=chapter_link)
        if not soup:
            return False

        chapter = chapter_link.split("/")[-1].capitalize().replace("_", " ")
        tools.create_folder(self.manga_name)
        chapter_folder = self.manga_name + "/" + chapter + "/"
        tools.create_folder(chapter_folder)

        page_list = [item.attrs['src'] for item in soup.find(id=self.__pages_div_id).find_all('img')]
        image_list = []
        for ind, url in enumerate(page_list):
            extension = url.split(".")[-1]
            page = str(ind+1)
            if len(page) == 1:
                page = "0" + page
            filename = chapter_folder + page + "." + extension
            image_list.append((filename, url))
        tools.download_chapter(current_chapter=chapter, image_list=image_list)
        chapter_folder = chapter_folder[:-1]
        if self.zip:
            tools.to_zip(self.manga_name)

if __name__ == "__main__":
    pass
