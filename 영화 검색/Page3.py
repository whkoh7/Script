from tkinter import *
from tkinter import font
import tkinter.ttk
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.messagebox
from Set_Parsing import *

class Page3():
    def __init__(self,window):
        self.window = window
        self.fontstyle1 = font.Font(self.window, size=12, family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=9, weight='bold', family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.set_Parsing = Set_Parsing()

    def InitTopText(self):
        self.Toptext = Label(self.window, font=self.Topfontstyle, text="배우 정보 검색")
        self.Toptext.pack()

    def InitSearchBox(self):
        self.SearchEntryBox = Entry(self.window, font=self.fontstyle1, width=20)
        self.SearchEntryBox.place(x=250, y=50)

        self.SearchButton = Button(self.window, overrelief='solid', text="검색",
                                               command=self.SearchActor)
        self.SearchButton.place(x=440, y=50)

    def InitSearchlabel(self):
        self.ActorimageLabel = Label(self.window, font=self.fontstyle1, text="", image='')
        self.ActorimageLabel.place(x=100, y=150)
        self.ActorinfoLabel = [] *6
        for i in range(6):
            self.ActorinfoLabel.append(Label(self.window, font=self.fontstyle1, text=""))
            self.ActorinfoLabel[i].place(x=100,y=325+(i*25))


    def SearchActor(self):
        self.set_Parsing.actorInfo_HTML_request(self.SearchEntryBox.get())
        self.ActorinfoLabel[0].configure(text = self.set_Parsing.actor_info[0])
        for i in range(1,6):
            self.ActorinfoLabel[i].configure(text=self.set_Parsing.actor_info_tag[i-1]\
                                                 +": "+self.set_Parsing.actor_info[i])


        if self.set_Parsing.actor_image_url != None:
            with urllib.request.urlopen(self.set_Parsing.actor_image_url) as u:
                raw_data = u.read()
            image = Image.open(BytesIO(raw_data))
            _image = ImageTk.PhotoImage(image)
            self.ActorimageLabel.configure(image=_image)
            self.ActorimageLabel.image = _image
        else:
            self.ActorimageLabel.configure(text="이미지 없음")



    def Work_page(self):
        self.InitTopText()
        self.InitSearchBox()
        self.InitSearchlabel()