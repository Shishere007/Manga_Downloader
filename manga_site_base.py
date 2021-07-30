import tools
import concurrent.futures
import multiprocessing

__author__ = "Shishere"
__version__ = "1.0"

class MangaSite:
    def __init__(self, manga_link: str, manga_name: str = None,zip:bool=True) -> None:
        self.__base_url = ''
        
        self.manga_name = manga_name
        self.manga_link = manga_link
        self.zip = zip

        self.chapter_list = []
        self.chapter_count = 0
    
    def get_chapter_list(self, ) -> list:
        '''
        return [{chapter:'',link:''}]
        '''
        return []
    
    def download_chapter(self, chapter: dict) -> None:
        '''
        @param
        chapter (dict)  :   {"chapter":"chapter","link":"link"}
        '''
        pass

    def download_multiple_chapters(self, chapter_list: list, thread_count: int = 1) -> None:
        '''
        @param
        chapter_list    (list)  : [{"chapter":"chapter","link":"link"}]
        thread_count    (int)   :   integer value : default = 1
        '''
        if len(self.chapter_list) == 0:
            print("NO CHAPTER FOUND")
            return
        available_thread_count = multiprocessing.cpu_count() * 2

        if thread_count < 1:
            thread_count = 1
        elif thread_count > available_thread_count:
            thread_count = available_thread_count

        POOL_SIZE = thread_count  # multiprocessing.cpu_count()
        with concurrent.futures.ThreadPoolExecutor(max_workers=POOL_SIZE) as executor:
            executor.map(self.download_chapter, chapter_list)
    
    def download_all_chapters(self,thread_count:int = 1) -> None:
        if len(self.chapter_list) == 0:
            print("NO CHAPTER FOUND")
            return
        self.download_multiple_chapters(chapter_list=self.chapter_list,thread_count=thread_count)


if __name__ == "__main__":
    pass