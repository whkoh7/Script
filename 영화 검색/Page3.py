from tkinter import *
from tkinter import font
import tkinter.ttk
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.messagebox
from Set_Parsing import *
import webbrowser

class page3():
    def __init__(self,window):
        self.window = window
        self.img = PhotoImage(file="resource/BackGround_3.png")
        self.bg = Label(self.window, image=self.img)
        self.bg.place(x=0, y=0)
        self.bg.image = self.img
        self.fontstyle1 = font.Font(self.window, size=12, family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=9, weight='bold', family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.set_Parsing = Set_Parsing()
        self.textbox = Text(self.window, font=self.fontstyle1, width=40, height=10)

    def InitTopText(self):
        pass

    def InitSearchBox(self):
        self.SearchEntryBox = Entry(self.window, font=self.fontstyle1, width=20)
        self.SearchEntryBox.place(x=250, y=50)

        Button_img = PhotoImage(file="resource/Button_Search.png")
        self.SearchButton = Button(self.window, overrelief='solid', image=Button_img,
                                               command=self.SearchActor,bg = "dark slate gray")
        self.SearchButton.image = Button_img
        self.SearchButton.place(x=440, y=45)

    def InitSearchlabel(self):
        self.ActorimageLabel = Label(self.window, font=self.fontstyle1, text="", image='')
        self.textbox.place(x=100,y=325)
        self.Label1 = Label(self.window, font=self.Topfontstyle, text="",fg="white", bg = "dark slate gray")


    def SearchActor(self):
        self.set_Parsing.actorInfo_HTML_request(self.SearchEntryBox.get())
        movie_list = []
        del movie_list[:]

        self.textbox.insert(CURRENT,self.set_Parsing.actor_info[0]+'\n\n')
        for i in range(1,5):
            self.textbox.insert(CURRENT,self.set_Parsing.actor_info_tag[i-1]\
                                                 +": "+self.set_Parsing.actor_info[i]+'\n')

        if self.set_Parsing.actor_image_url != None:
            with urllib.request.urlopen(self.set_Parsing.actor_image_url) as u:
                raw_data = u.read()
            image = Image.open(BytesIO(raw_data))
            _image = ImageTk.PhotoImage(image)
            self.ActorimageLabel.configure(bg = "dark slate gray",image=_image)
            self.ActorimageLabel.image = _image
        else:
            self.ActorimageLabel.configure(text="이미지 없음")

        #출연 영화 목록
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
                self.actor_movie_image.append(Label(self.window, image=_image, bg = "dark slate gray"))
                self.actor_movie_image[i].image = _image
            else:
                self.actor_movie_image.append(Label(self.window, text="이미지 없음",fg = "white", bg = "dark slate gray"))
            self.actor_movie_name.append(Label(self.window, font=self.fontstyle2,fg = "white", bg = "dark slate gray",text=self.set_Parsing.movie_name_list[i]))
            self.actor_movie_image[i].place(x=700+i*150,y=150)
            self.actor_movie_name[i].place(x=700 + i * 150, y=310)
        self.Label1.configure(text='출연작')

        Button_img = PhotoImage(file="resource/Button_Naver_Search.png")
        self.Actor_naver_url = Button(self.window, font=self.fontstyle1,bg = "dark slate gray", image=Button_img\
                                      ,command=lambda a=self.set_Parsing.actorInfo_url:webbrowser.open(a))
        self.Actor_naver_url.place(x=200, y=525)
        self.Actor_naver_url.image=Button_img

        self.ActorimageLabel.place(x=100, y=150)
        self.Label1.place(x=700, y=100)




    def Work_page(self):
        self.InitTopText()
        self.InitSearchBox()
        self.InitSearchlabel()