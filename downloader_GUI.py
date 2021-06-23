from tkinter import Button, Entry, Label, StringVar, Tk, ttk
from KissManga import KissManga
from threading import Thread

__version__ = '1.0'

class downloader:
    def __init__(self) -> None:
        self.__manga_site_list = ['KissManga']

    def initialize(self,) -> None:
        self.__root = Tk()
        self.__root.title("Manga Downloader")
        self.__root.minsize(900, 800)
        self.__root.maxsize(900, 800)

        self.__manga_sites_label = Label(self.__root, text="Web site", font=15)
        self.__manga_sites_label.place(x=10, y=20)
        self.__manga_site = StringVar()
        self.__manga_sites_combobox = ttk.Combobox(self.__root, width=25, textvariable=self.__manga_site)
        self.__manga_sites_combobox.place(x=110, y=20)
        self.__manga_sites_combobox['values'] = self.__manga_site_list
        self.__manga_sites_combobox.current()
        self.__manga_sites_combobox.configure(state='readonly')

        self.__manga_link_label = Label(self.__root, text="Manga Link", font=15)
        self.__manga_link_label.place(x=10, y=60)
        self.__manga_link_textbox = Entry(self.__root, font=15, width=75)
        self.__manga_link_textbox.place(x=110, y=60)
        self.__seach_chapter_button = Button(self.__root, text='Search', font=13, width=8, command=self.__search)
        self.__seach_chapter_button.place(x=800, y=58)

        self.__mange_name_label = Label(self.__root, text="Manga Name", font=15)
        self.__mange_name_label.place(x=10, y=100)
        self.__mange_name_textbox = Entry(self.__root, font=15, width=75)
        self.__mange_name_textbox.place(x=110, y=100)

        self.__manga_chapter_search_result_label = Label(self.__root, text="Chapter list", font=15)
        self.__manga_chapter_search_result_label.place(x=10, y=140)
        self.__manga_chapter_search_result_table = ttk.Treeview(self.__root, columns=(1,2), show="headings", height=30)
        self.__manga_chapter_search_result_table.place(x=10, y=160)
        self.__manga_chapter_search_result_table.column("#1",width=100)
        self.__manga_chapter_search_result_table.heading(1,text="SLNO")
        self.__manga_chapter_search_result_table.column("#2",width=400)
        self.__manga_chapter_search_result_table.heading(2,text="Chapter")

        self.__manga_chapter_search_result_table_scrollbar = ttk.Scrollbar(self.__root, orient="vertical", command=self.__manga_chapter_search_result_table.yview)
        self.__manga_chapter_search_result_table.configure(yscroll=self.__manga_chapter_search_result_table_scrollbar.set)
        self.__manga_chapter_search_result_table_scrollbar.pack(side="right", fill='y')

        self.__from_chapter_label = Label(self.__root, text="From", font=15)
        self.__from_chapter_label.place(x=600, y=300)
        self.__from_chapter_textbox = Entry(self.__root, font=15, width=15)
        self.__from_chapter_textbox.place(x=650,y=300)

        self.__to_chapter_label = Label(self.__root, text="To", font=15)
        self.__to_chapter_label.place(x=600, y=350)
        self.__to_chapter_textbox = Entry(self.__root,font=15,width=15)
        self.__to_chapter_textbox.place(x=650,y=350)

        self.__download_button = Button(self.__root, text='Download', font=13, width=14, command=self.__download_thread)
        self.__download_button.place(x=650, y=400)
        self.__download_button.config(state='disabled')

        self.__root.mainloop()

    def __search(self) -> None:
        try:
            self.__manga_chapter_search_result_table.delete(*self.__manga_chapter_search_result_table.get_children())

            self.__manga_link = self.__manga_link_textbox.get()
            if not self.__manga_link:
                return
            self.manga = KissManga(manga_link=self.__manga_link)
            self.manga.get_chapter_list()
            self.__mange_name_textbox.insert(0, self.manga.manga_name)

            for ind,chapter in enumerate([chap.get('chapter') for chap in self.manga.chapter_list]):
                self.__manga_chapter_search_result_table.insert("", "end", values=[ind+1,chapter])

            self.__from_chapter_textbox.delete(0)
            self.__from_chapter_textbox.insert(0,'1')

            self.__to_chapter_textbox.delete(0)
            self.__to_chapter_textbox.insert(0,str(self.manga.chapter_count))
            self.__download_button.config(state='active')

        except Exception as e:
            print(e)
            
    def __download(self,) -> None:
        try:
            self.__download_button.config(state='disabled')

            from_chapter = self.__from_chapter_textbox.get()
            to_chapter = self.__to_chapter_textbox.get()
            if not (from_chapter.isnumeric() and to_chapter.isnumeric()):
                return
            
            from_chapter = int(from_chapter)
            to_chapter = int(to_chapter)

            from_chapter = 1 if from_chapter < 1 else from_chapter
            to_chapter = self.manga.chapter_count if to_chapter > self.manga.chapter_count else to_chapter

            chapter_list = self.manga.chapter_list[from_chapter-1:to_chapter]

            self.manga.download_multiple_chapters(chapter_list)

            self.__download_button.config(state='active')
        except Exception as e:
            print(e)

    def __download_thread(self,) -> None:
        thread = Thread(target=self.__download)
        thread.start()

    # def __double_click_add(self, event) -> None:
    #     try:
    #         download_list = [self.__manga_chapter_download_result_table.item(item,"values")[0] for item in self.__manga_chapter_download_result_table.get_children()]
    #         a = self.__manga_chapter_download_result_table.selection()
    #         selected = self.__manga_chapter_download_result_table.item(self.__manga_chapter_download_result_table.selection()[0],"values")
    #         if selected not in download_list:
    #             download_list.append(selected)
    #             self.__manga_chapter_download_result_table.delete(*self.__manga_chapter_download_result_table.get_children())
    #             for item in download_list:
    #                 self.__manga_chapter_download_result_table.insert("","end",values=[item])
    #     except Exception as e:
    #         print(e)



if __name__ == "__main__":
    downloader().initialize()
    # manga = KissManga('https://kissmanga.org/manga/gn921773',
    #                   "Nan Hao Shang feng")
