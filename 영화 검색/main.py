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
Naver_url_option = "&display=20"


class mainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("720x400")
        self.window.title("영화 정보 검색")
        self.Boxfontstyle = font.Font(self.window, size=12, family='Consolas')
        self.InitTopText()
        self.InitSearchListBox()
        self.InitSearchBox()
        self.InitSearchlabel()
        self.window.mainloop()

    def InitTopText(self):
        self.Topfontstyle = font.Font(self.window, size=22, weight='bold', family='Consolas')
        self.Toptext = Label(self.window,font = self.Topfontstyle,text="영화 정보 검색 APP")
        self.Toptext.pack()

    def InitSearchListBox(self):
        self.MovieList = Canvas(self.window,width=200,height=200,bg="white",bd=2,relief="groove")
        self.MovieList.place(x=495,y=80 )

    def InitSearchBox(self):
        self.SearchMovieEntryBoxlabel = Label(self.window, font=self.Boxfontstyle, text="영화 이름: ")
        self.SearchMovieEntryBoxlabel.place(x=20, y=50)
        self.SearchMovieEntryBox = Entry(self.window, font=self.Boxfontstyle,width = 16)
        self.SearchMovieEntryBox.place(x=110,y=50)

        self.SearchYearEntryBoxlabel = Label(self.window, font=self.Boxfontstyle, text="년도: ")
        self.SearchYearEntryBoxlabel.place(x=275, y=50)
        self.SearchYearEntryBox = Entry(self.window, font=self.Boxfontstyle,width = 6)
        self.SearchYearEntryBox.place(x=325, y=50)

        self.SearchDateEntryBoxlabel = Label(self.window, font=self.Boxfontstyle, text="월/일: ")
        self.SearchDateEntryBoxlabel.place(x=380, y=50)
        self.SearchDateEntryBox = Entry(self.window, font=self.Boxfontstyle, width=6)
        self.SearchDateEntryBox.place(x=440, y=50)

        self.SearchMovieInfoButton = Button(self.window, overrelief='solid', text="정보검색", command=self.SearchMovieInfo)
        self.SearchMovieInfoButton.place(x=520, y=50)
        self.SearchMovieListButton = Button(self.window,overrelief = 'solid',text = "일/주간리스트",command=self.SearchMovieList)
        self.SearchMovieListButton.place(x=580,y=50)

    def InitSearchlabel(self):
        self.Sranklabel = Label(self.window, font=self.Boxfontstyle, text="순위: ")
        self.Sranklabel.place(x=50,y=75)
        self.SopenDtlabel = Label(self.window, font=self.Boxfontstyle, text="개봉일: ")
        self.SopenDtlabel.place(x=50,y=100)
        self.SaudiAcclabel = Label(self.window, font=self.Boxfontstyle, text="누적관객수: ")
        self.SaudiAcclabel.place(x=50,y=125)
        self.SsalesAcclabel = Label(self.window, font=self.Boxfontstyle, text="누적매출액: ")
        self.SsalesAcclabel.place(x=50,y=150)
        self.Sactorlabel = Label(self.window, font=self.Boxfontstyle, text="출연 배우: ")
        self.Sactorlabel.place(x=50, y=175)
        self.Sdirectorlabel = Label(self.window, font=self.Boxfontstyle, text="감독: ")
        self.Sdirectorlabel.place(x=50, y=300)
        self.Simage = Label(self.window,image = '')
        self.Simage.place(x=350,y=100)

    def ClearLabel(self):
        self.Sranklabel.configure(text="순위: ")
        self.SopenDtlabel.configure(text="개봉일: ")
        self.SaudiAcclabel.configure(text="누적관객수: ")
        self.SsalesAcclabel.configure(text="누적매출액: ")
        self.Sactorlabel.configure(text="출연 배우: ")
        self.Sdirectorlabel.configure(text="감독: ")
        self.Simage.configure(image='')


    def Movie_xml_request(self): #영화진흥위원회 api 호출
        self.request = urllib.request.Request(daily_movie_url+self.SearchYearEntryBox.get() + self.SearchDateEntryBox.get())
        self.response = urllib.request.urlopen(self.request)
        self.xml_status = self.response.getcode()
        self.response_text = self.response.read()
        self.xml_text = self.response_text.decode('utf-8')

    def Naver_xml_request(self): #네이버영화 api 호출
        self.Nrequest = urllib.request.Request(Naver_url + urllib.parse.quote(self.SearchMovieEntryBox.get()))
        self.Nrequest.add_header("X-Naver-Client-Id", client_id)
        self.Nrequest.add_header("X-Naver-Client-Secret", client_secret)

        self.Nresponse = urllib.request.urlopen(self.Nrequest)
        self.Nxml_status = self.Nresponse.getcode()
        self.Nresponse_text = self.Nresponse.read()
        self.Nxml_text = self.Nresponse_text.decode('utf-8')


    def SearchMovieList(self): #입력한 날짜의 개봉한 박스오피스 출력
        self.MovieList.delete("all")
        self.MovieListText = self.SearchYearEntryBox.get()+"/"+self.SearchDateEntryBox.get()+" 박스오피스"+'\n\n'
        self.Movie_xml_request()

        if self.xml_status == 200:
            self.root = ET.fromstring(self.xml_text)
            for child in self.root.find("dailyBoxOfficeList"):
                self.MovieListText += child.find('movieNm').text+'\n'

        self.MovieList.create_text(110,100,text=self.MovieListText)


    def SearchMovieInfo(self): #입력한 박스오피스 정보 출력, 날짜가 입력되어야함
        self.Movie_xml_request()
        self.Naver_xml_request()
        self.ClearLabel()

        openDt = '' #개봉연도 저장 변수, 제대로된 포스터 이미지 찾기위함

        if self.xml_status == 200:
            self.root = ET.fromstring(self.xml_text)
            self.Nroot = ET.fromstring(self.Nxml_text)

            for child in self.root.find("dailyBoxOfficeList"):
                if child.find('movieNm').text == self.SearchMovieEntryBox.get():
                    self.Sranklabel.configure(text="순위: " + child.find("rank").text + "위")
                    self.SopenDtlabel.configure(text="개봉일: " + child.find("openDt").text)
                    self.SaudiAcclabel.configure(text="누적관객수: " + child.find("audiAcc").text + "명")
                    self.SsalesAcclabel.configure(text= "누적매출액: "+child.find("salesAcc").text+"원")
                    openDt = child.find("openDt").text

            for child in self.Nroot.find('channel'):
                if child.text == None:
                    if child.find('pubDate').text <= openDt[0:4]:
                        self.Sactorlabel.configure(text="출연 배우: "+child.find('actor').text.replace('|','\t\n'))
                        self.Sdirectorlabel.configure(text="감독: "+child.find('director').text.replace('|',''))

                        image_url = child.find('image').text
                        with urllib.request.urlopen(image_url) as u:
                            raw_data = u.read()
                        image = Image.open(BytesIO(raw_data))
                        movie_image = ImageTk.PhotoImage(image)
                        self.Simage.configure(image = movie_image)
                        self.Simage.image = movie_image
                        break


mainGUI()



