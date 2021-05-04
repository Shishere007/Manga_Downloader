from bin import tools


__author__ = "Shishere"
__version__ = "1.0"


class KissManga:
    def __init__(self,manga_name:str,manga_link:str) -> None:
        self.__base_url = 'https://kissmanga.org'
        self.manga_name = manga_name
        self.manga_link = manga_link

        self.__chapter_list_main_div_className = 'listing listing8515 full'


    def start(self,):
        chapter_list = self.get_chapter_list()

    def get_chapter_list(self) -> list:
        '''
        return [
            {
                chapter:'',
                link:''
            }
        ]
        '''
        # soup = tools.prepare_soup(link=self.manga_link)
        soup = tools.test_soup()
        if not soup:
            return False
        chapter_div_list = soup.find_all('a')
        chapter_list = []
        for a in chapter_div_list[::-1]:
            if 'title' in a.attrs:
                if a.attrs['title'].__contains__('Read'):
                    chapter_list.append(
                        {
                            'chapter': tools.clear_chapter_name(a.text.strip()),
                            'link': self.__base_url + a.attrs['href']
                        }
                    )
        return chapter_list

    def download_chapter(self, chapter_link: str) -> None:
        soup = tools.prepare_soup(link=chapter_link)
        if not soup:
            return False
        page_list = [item.attrs['src'] for item in soup.find(id='centerDivVideo').find_all('img')]
        chapter = chapter_link.split("/")[-1].capitalize()
        
        tools.create_folder(self.manga_name)

        chapter_folder = self.manga_name + "/" + chapter + "/"
        tools.create_folder(chapter_folder)

        chapter_folder = chapter_folder[:-1]

        




if __name__ == "__main__":
    pass
