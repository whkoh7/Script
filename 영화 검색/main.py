from tkinter import *
from tkinter import font
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.messagebox
import xml.etree.ElementTree as ET
import urllib.request

client_id = "tbnHeHUwtbVgWtr91vX5"
client_secret = "rFSWzcfijB"

daily_movie_url = "http://www.kobis.or.kr//kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=0f7d6638c03ecc9885350d92093d8f8b&targetDt="
Naver_url = "https://openapi.naver.com/v1/search/movie.xml?query="
Naver_url_option = "&display=10"


class mainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("600x400")
        self.window.title("영화 정보 검색")
        self.Boxfontstyle = font.Font(self.window, size=14, weight='bold', family='Consolas')
        self.InitTopText()
        self.InitSearchBox()
        self.window.mainloop()

    def InitTopText(self):
        self.Topfontstyle = font.Font(self.window, size=22, weight='bold', family='Consolas')
        self.Toptext = Label(self.window,font = self.Topfontstyle,text="영화 정보 검색 APP")
        self.Toptext.pack()

    def InitSearchListBox(self):
        self.SearchListBox = Listbox(self.window, font=self.Boxfontstyle,activestlye='none'\
                                     )

    def InitSearchBox(self):
        self.SearchEntryBox = Entry(self.window, font=self.Boxfontstyle)
        self.SearchEntryBox.pack()
        self.SearchButton = Button(self.window,overrelief = 'solid',text = "검색",command=self.Search)
        self.SearchButton.pack()
        self.Sranklabel = Label(self.window, font=self.Boxfontstyle, text="순위: ")
        self.Sranklabel.pack()
        self.SopenDtlabel = Label(self.window, font=self.Boxfontstyle, text="개봉일: ")
        self.SopenDtlabel.pack()
        self.SaudiAcclabel = Label(self.window, font=self.Boxfontstyle, text="누적관객수: ")
        self.SaudiAcclabel.pack()
        self.SsalesAcclabel = Label(self.window, font=self.Boxfontstyle, text="누적매출액: ")
        self.SsalesAcclabel.pack()
        self.Simage = Label(self.window,image = '')
        self.Simage.pack()

    def Search(self):
        self.request = urllib.request.Request(daily_movie_url+"20200404")
        self.response = urllib.request.urlopen(self.request)
        self.xml_status = self.response.getcode()
        self.response_text = self.response.read()
        self.xml_text = self.response_text.decode('utf-8')

        self.Nrequest = urllib.request.Request(Naver_url + urllib.parse.quote(self.SearchEntryBox.get()))
        self.Nrequest.add_header("X-Naver-Client-Id", client_id)
        self.Nrequest.add_header("X-Naver-Client-Secret", client_secret)

        self.Nresponse = urllib.request.urlopen(self.Nrequest)
        self.Nxml_status = self.Nresponse.getcode()
        self.Nresponse_text = self.Nresponse.read()
        self.Nxml_text = self.Nresponse_text.decode('utf-8')

        if self.xml_status == 200:
            self.root = ET.fromstring(self.xml_text)
            self.Nroot = ET.fromstring(self.Nxml_text)

            print(self.Nroot.find("channel").find("item").find('image').text)

            for child in self.root.find("dailyBoxOfficeList"):
                if child.find('movieNm').text == self.SearchEntryBox.get():
                    self.Sranklabel.configure(text="순위: " + child.find("rank").text + "위")
                    self.SopenDtlabel.configure(text="개봉일: " + child.find("openDt").text)
                    self.SaudiAcclabel.configure(text="누적관객수: " + child.find("audiAcc").text + "명")
                    self.SsalesAcclabel.configure(text= "누적매출액: "+child.find("salesAcc").text+"원")

            image_url = self.Nroot.find("channel").find("item").find('image').text
            with urllib.request.urlopen(image_url) as u:
                raw_data = u.read()
            image = Image.open(BytesIO(raw_data))
            movie_image = ImageTk.PhotoImage(image)
            self.Simage.configure(image = movie_image)
            self.Simage.image = movie_image



mainGUI()



