from tkinter import Button, Entry, IntVar, Label, StringVar, Tk, ttk
from tkinter.constants import END
from tkinter.messagebox import showinfo
from KissManga import KissManga
from threading import Thread

__author__ = "Shishere"
__version__ = "1.1"

class downloader:
    def __init__(self) -> None:
        self.__manga_site_list = ['KissManga']
        
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

        self.__save_type_label = Label(self.__root, text="Save Chapter as", font=15)
        self.__save_type_label.place(x=600,y=175)
        self.zip = IntVar()
        values = {"Zip":1,"Folder":0}
        x = 650
        y = 200
        for text,val in values.items():
            ttk.Radiobutton(
                master=self.__root,
                text=text,
                variable=self.zip,
                value=val,
            ).place(x=x,y=y)
            x += 70
        self.zip.set(1)

        self.__from_chapter_label = Label(self.__root, text="From", font=15)
        self.__from_chapter_label.place(x=600, y=300)
        self.__from_chapter_textbox = Entry(self.__root, font=15, width=15)
        self.__from_chapter_textbox.place(x=650,y=300)

        self.__to_chapter_label = Label(self.__root, text="To", font=15)
        self.__to_chapter_label.place(x=600, y=350)
        self.__to_chapter_textbox = Entry(self.__root,font=15,width=15)
        self.__to_chapter_textbox.place(x=650,y=350)

        self.__download_button = Button(self.__root, text='Download', font=13, width=20, command=self.__download_thread)
        self.__download_button.place(x=630, y=400)
        self.__download_button.config(state='disabled')

        self.__custom_label = Label(self.__root, text="Custom", font=15)
        self.__custom_label.place(x=700, y=500)
        self.__custom_textbox = Entry(self.__root,font=15,width=20)
        self.__custom_textbox.place(x=630,y=530)
        self.__custom_download_button = Button(self.__root, text='Download', font=13, width=20,command=self.__download_thread_custom)
        self.__custom_download_button.place(x=630, y=570)
        self.__custom_download_button.config(state='disabled')

        note = 'NOTE :\nDouble click on chapter name to add\n chapter to custom download list\n or enter SLNO of chapter manually\n seperated by commas'

        self.__note = Label(self.__root, text=note, font=15)
        self.__note.place(x=600, y=650)

        self.__manga_chapter_search_result_table.bind(sequence="<Double-1>",func=self.__double_click_add)

    def initialize(self,) -> None:
        self.__root.mainloop()
    
    def __popup(self,field:str) -> None:
        if field == 'to':
            showinfo("Window","'To' Field Cannot be Empty")
        elif field == 'from':
            showinfo("Window","'From' Field Cannot be Empty")
        elif field == 'manga':
            showinfo("Window","Enter Manga Link")
        elif field == 'invlid site':
            sites = '\n > ' + '\n'.join(self.__manga_site_list)
            showinfo("Window",f"Cant download from this site\nCurrently Available : {sites}")
        elif field == 'no chapter':
            showinfo("Window","Enter chapters.\nDouble click on chapter name to add chapter to custom list")
        else:
            showinfo("Window",f"Invalid chapter Number -> {field.split('.')[-1]}")
        
    def __site_allowed(self,) -> bool:
        for site in self.__manga_site_list:
            if self.__manga_link.lower().__contains__(site.lower()):
                return True
            return False

    def __search(self) -> None:
        try:
            self.__manga_chapter_search_result_table.delete(*self.__manga_chapter_search_result_table.get_children())

            self.__manga_link = self.__manga_link_textbox.get()
            if not self.__manga_link:
                self.__popup('manga')
                return
            
            if not self.__site_allowed():
                self.__popup('invlid site')
                return

            self.manga = KissManga(manga_link=self.__manga_link,zip=self.zip.get())
            self.manga.get_chapter_list()
            self.__mange_name_textbox.insert(0, self.manga.manga_name)

            for ind,chapter in enumerate([chap.get('chapter') for chap in self.manga.chapter_list]):
                self.__manga_chapter_search_result_table.insert("", "end", values=[ind+1,chapter])

            self.__from_chapter_textbox.delete(0)
            self.__from_chapter_textbox.insert(0,'1')

            self.__to_chapter_textbox.delete(0)
            self.__to_chapter_textbox.insert(0,str(self.manga.chapter_count))

            self.__download_button.config(state='active')
            self.__custom_download_button.config(state='active')
        except Exception as e:
            print(e)
            
    def __download(self,) -> None:
        try:
            self.__update_zip()
            
            self.__download_button.config(state='disabled')
            self.__custom_download_button.config(state='disabled')

            from_chapter = self.__from_chapter_textbox.get()
            to_chapter = self.__to_chapter_textbox.get()

            if not from_chapter:
                self.__popup('from')
                return

            if not to_chapter:
                self.__popup('to')
                return

            if not from_chapter.isnumeric():
                self.__popup(f'chapter.({from_chapter})')
                return
            if not to_chapter.isnumeric():
                self.__popup(f'chapter.({to_chapter})')
                return
            
            from_chapter = int(from_chapter)
            to_chapter = int(to_chapter)


            from_chapter = 1 if from_chapter < 1 else from_chapter
            to_chapter = self.manga.chapter_count if to_chapter > self.manga.chapter_count else to_chapter

            chapter_list = self.manga.chapter_list[from_chapter-1:to_chapter]

            self.manga.download_multiple_chapters(chapter_list)

        except Exception as e:
            print(e)
        finally:
            self.__custom_download_button.config(state='active')
            self.__download_button.config(state='active')
    
    def __download_custom(self,) -> None:
        try:
            self.__update_zip()

            self.__custom_download_button.config(state='disabled')
            self.__download_button.config(state='disabled')

            chapters_num = sorted(list(map(int,[item for item in self.__custom_textbox.get().split(",") if item.isnumeric()])))
            if not chapters_num:
                self.__popup('no chapter')
                return
            chapters = [self.manga.chapter_list[ind-1] for ind in chapters_num if ind-1 < self.manga.chapter_count]
            for chapter in chapters:
                self.manga.download_chapter(chapter)

        except Exception as e:
            print(e)
        finally:
            self.__download_button.config(state='active')
            self.__custom_download_button.config(state='active')

    def __download_thread(self,) -> None:
        thread = Thread(target=self.__download)
        thread.start()
    
    def __download_thread_custom(self,) -> None:
        thread = Thread(target=self.__download_custom)
        thread.start()
        

    def __double_click_add(self, event) -> None:
        try:
            selected_ind = self.__manga_chapter_search_result_table.item(self.__manga_chapter_search_result_table.selection()[0],"values")[0]
            a = self.__custom_textbox.get()
            already_selected = [num for num in self.__custom_textbox.get().split(',') if num.isnumeric()]
            if selected_ind not in already_selected : already_selected.append(selected_ind)

            self.__custom_textbox.delete(0,END)
            self.__custom_textbox.insert(0,",".join(already_selected))
        except Exception as e:
            print(e)
    
    def __update_zip(self,) -> None:
        self.manga.zip = self.zip.get()



if __name__ == "__main__":
    pass

