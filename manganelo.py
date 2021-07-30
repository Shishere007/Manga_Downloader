import tools
from manga_site_base import MangaSite

__author__ = "Shishere"
__version__ = "1.0"

class Manganelo(MangaSite):
    def __init__(self, manga_link: str, manga_name: str=None, zip: bool = True) -> None:
        super().__init__(manga_link=manga_link, manga_name=manga_name, zip=zip)
        self.__base_url = 'https://chap.manganelo.com/'

        self.manga_name = manga_name
        self.manga_link = manga_link
        self.zip = zip

        self.header = {
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Referer':'https://chap.manganelo.com/'
        }
        self.chapter_list = []
        self.chapter_count = 0

    def get_chapter_list(self, ) -> list:
        '''
        return [{chapter:'',link:''}]
        '''
        soup = tools.prepare_soup(link=self.manga_link)
        if not soup:
            return False
        if self.manga_name in [None, "", " "]:
            name_div = soup.find_all('div',{'class':'story-info-right'})
            if name_div:
                if name_div[0].find_all('h1'):
                    self.manga_name = name_div[0].find_all('h1')[0].text
        
        chapter_div_list = soup.find_all('li')
        for li in chapter_div_list:
            a = li.find_all('a')
            if a:
                self.chapter_list.append(
                    {
                        'chapter':a[0].text,
                        'link':a[0].attrs['href']
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

        page_list = [item.attrs['src'] for item in soup.find_all('div',{'class':'container-chapter-reader'})[0].find_all('img')]
        image_list = []
        for ind, url in enumerate(page_list):
            extension = url.split(".")[-1]
            page = str(ind+1)
            if len(page) == 1:
                page = "0" + page
            filename = chapter_folder + page + "." + extension
            image_list.append((filename, url))
        
        tools.download_chapter(current_chapter=chapter, image_list=image_list,header=self.header)
        chapter_folder = chapter_folder[:-1]
        if self.zip:
            tools.to_zip(self.manga_name)
        

if __name__ == "__main__":
    pass