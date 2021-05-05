from tkinter import Button,Entry,Label,StringVar, Tk,ttk


class downloader:
    def __init__(self) -> None:
        pass

    def initialize(self,) -> None:
        self.__root = Tk()
        self.__root.title("Manga Downloader")
        self.__root.minsize(900, 800)
        self.__root.maxsize(900, 800)

        
        self._mange_name_link_label = Label(self.__root,text="Manga Link",font=15)
        self._mange_name_link_label.place(x=10,y=20)
        self._mange_name_link_textbox = Entry(self.__root,font=15,width=80)
        self._mange_name_link_textbox.place(x=110,y=20)


        self.__root.mainloop()




if __name__ == "__main__":
    downloader().initialize()