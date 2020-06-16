import smtplib
from email.mime.text import MIMEText
from tkinter import *
from tkinter import font
from tkinter.scrolledtext import *

my_email = "anis15740@gmail.com"
key = "gcfrmifmtmpizphi"

class page4():
    def __init__(self,window):
        self.window = window
        self.img = PhotoImage(file="resource/BackGround_4.png")
        self.bg = Label(self.window, image=self.img)
        self.bg.place(x=0, y=0)
        self.bg.image = self.img
        self.fontstyle1 = font.Font(self.window, size=10, family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.textbox = ScrolledText(self.window,width=35,height=30)


    def InitTopText(self):
        pass

    def InitWidget(self):
        self.textbox.place(x=25,y=125)

        Button_img = PhotoImage(file="resource/Button_Mail.png")
        self.EmailEntry = Entry(self.window, font=self.fontstyle1, width=30)
        self.EmailEntry.place(x=300, y=125)
        self.sendbutton = Button(self.window,bg = "dark slate gray", image=Button_img, command=self.SendMail)
        self.sendbutton.image = Button_img
        self.sendbutton.place(x=335, y=150)

    def SendMail(self):
        self.s = smtplib.SMTP('smtp.gmail.com', 587)
        self.s.starttls()
        self.s.login(my_email, key)
        msg=MIMEText(self.textbox.get("1.0","end"))
        msg['Subject'] = '제목: 영화정보검색'
        self.s.sendmail(my_email,self.EmailEntry.get(),msg.as_string())
        self.s.quit()

    def Work_page(self):
        self.InitTopText()
        self.InitWidget()
