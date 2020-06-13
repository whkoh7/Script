from tkinter import *
from tkinter import font
import tkinter.ttk
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.messagebox
from Set_Parsing import *
import webbrowser

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
        self.Label1 = Label(self.window, font=self.Topfontstyle, text="")
        self.Label1.place(x=700,y=100)


    def SearchActor(self):
        self.set_Parsing.actorInfo_HTML_request(self.SearchEntryBox.get())
        self.set_Parsing.actor_xml_request(self.SearchEntryBox.get())
        movie_list = []
        del movie_list[:]

        self.ActorinfoLabel[0].configure(text = self.set_Parsing.actor_info[0])
        for i in range(1,5):
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

        self.actor_movie_image = []
        self.actor_movie_name = []
        for i in range(len(self.actor_movie_image)):
            self.actor_movie_image[i].destroy()
            self.actor_movie_name[i].destroy()
        del self.actor_movie_image[:]
        del self.actor_movie_name[:]
        for i in range(len(self.set_Parsing.movie_img_list)):
            if self.set_Parsing.actor_image_url != None:
                with urllib.request.urlopen(self.set_Parsing.movie_img_list[i]) as u:
                    raw_data = u.read()
                image = Image.open(BytesIO(raw_data))
                image = image.resize((100, 150))
                _image = ImageTk.PhotoImage(image)
                self.actor_movie_image.append(Label(self.window, image=_image))
                self.actor_movie_image[i].image = _image
            else:
                self.actor_movie_image.append(Label(self.window, text="이미지 없음"))
            self.actor_movie_name.append(Label(self.window, font=self.fontstyle2,text=self.set_Parsing.movie_name_list[i]))
            self.actor_movie_image[i].place(x=700+i*150,y=150)
            self.actor_movie_name[i].place(x=700 + i * 150, y=310)
        self.Label1.configure(text='출연작')

        self.Actor_naver_url = Button(self.window, font=self.fontstyle1, text="네이버에서 검색"\
                                      ,command=lambda a=self.set_Parsing.actorInfo_url:webbrowser.open(a))
        self.Actor_naver_url.place(x=300, y=150)






    def Work_page(self):
        self.InitTopText()
        self.InitSearchBox()
        self.InitSearchlabel()