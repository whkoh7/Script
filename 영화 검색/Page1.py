from tkinter import *
from tkinter import font
import tkinter.ttk
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.messagebox
from Set_xml import *

class Page1():
    def __init__(self,window):
        self.window = window
        self.fontstyle1 = font.Font(self.window, size=12, family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=11, weight='bold', family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.set_xml = Set_xml()

    def P1_InitTopText(self):
        self.P1_Toptext = Label(self.window, font=self.Topfontstyle, text="박스오피스 검색")
        self.P1_Toptext.pack()

    def P1_InitSearchListBox(self):
        self.P1_MovieList = [] * 10
        self.P1_Rank_Label = [] * 10
        for i in range(10):
            self.P1_MovieList.append(
                Button(self.window, font=self.fontstyle2, overrelief="solid", width=28, height=1, bg='white',
                       command=lambda a=i: self.P1_SearchBoxofficeInfo(self.P1_MovieList[a]['text'])))
            self.P1_MovieList[i].place(x=100, y=80 + i * 45)
            self.P1_Rank_Label.append(Label(self.window, font=self.fontstyle2, text=str(i + 1) + "."))
            self.P1_Rank_Label[i].place(x=60, y=80 + i * 45)

    def P1_InitSearchBox(self):
        self.P1_SearchYearEntryBoxlabel = Label(self.window, font=self.fontstyle1, text="년도: ")
        self.P1_SearchYearEntryBoxlabel.place(x=310, y=50)
        self.P1_SearchYearEntryBox = Entry(self.window, font=self.fontstyle1, width=6)
        self.P1_SearchYearEntryBox.place(x=360, y=50)

        self.P1_SearchDateEntryBoxlabel = Label(self.window, font=self.fontstyle1, text="월/일: ")
        self.P1_SearchDateEntryBoxlabel.place(x=430, y=50)
        self.P1_SearchDateEntryBox = Entry(self.window, font=self.fontstyle1, width=6)
        self.P1_SearchDateEntryBox.place(x=490, y=50)

        self.P1_SearchMovieListButton = Button(self.window, overrelief='solid', text="일/주간박스오피스 출력",
                                               command=self.P1_SearchBoxofficeList)
        self.P1_SearchMovieListButton.place(x=560, y=50)

        self.P1_RadioVariety = tkinter.IntVar()
        self.P1_DailySelectionButton = Radiobutton(self.window, value=1, text="일간", variable=self.P1_RadioVariety,
                                                   command=self.P1_ClearList)
        self.P1_DailySelectionButton.place(x=90, y=50)
        self.P1_WeeklySelectionButton = Radiobutton(self.window, value=2, text="주간", variable=self.P1_RadioVariety,
                                                    command=self.P1_ClearList)
        self.P1_WeeklySelectionButton.place(x=150, y=50)

    def P1_InitSearchlabel(self):
        self.P1_Sranklabel = Label(self.window, font=self.fontstyle1, text="순위: ")
        self.P1_Sranklabel.place(x=350, y=75)
        self.P1_SopenDtlabel = Label(self.window, font=self.fontstyle1, text="개봉일: ")
        self.P1_SopenDtlabel.place(x=350, y=100)
        self.P1_SaudiAcclabel = Label(self.window, font=self.fontstyle1, text="누적관객수: ")
        self.P1_SaudiAcclabel.place(x=350, y=125)
        self.P1_SsalesAcclabel = Label(self.window, font=self.fontstyle1, text="누적매출액: ")
        self.P1_SsalesAcclabel.place(x=350, y=150)
        # self.Sactorlabel = Label(self.P1, font=self.Boxfontstyle, text="출연 배우: ")
        # self.Sactorlabel.place(x=300, y=175)
        # self.Sdirectorlabel = Label(self.P1, font=self.Boxfontstyle, text="감독: ")
        # self.Sdirectorlabel.place(x=300, y=300)
        self.P1_Simage = Label(self.window, image='')
        self.P1_Simage.place(x=580, y=100)

    def P1_ClearList(self):
        for i in range(10):
            self.P1_MovieList[i].configure(text='')

    def P1_ClearLabel(self):
        self.P1_Sranklabel.configure(text="순위: ")
        self.P1_SopenDtlabel.configure(text="개봉일: ")
        self.P1_SaudiAcclabel.configure(text="누적관객수: ")
        self.P1_SsalesAcclabel.configure(text="누적매출액: ")
        # self.Sactorlabel.configure(text="출연 배우: ")
        # self.Sdirectorlabel.configure(text="감독: ")
        self.P1_Simage.configure(image='')

    def P1_SearchBoxofficeList(self):  # 입력한 날짜의 개봉한 박스오피스 출력
        self.set_xml.Movie_xml_request(self.P1_SearchYearEntryBox.get() \
                               , self.P1_SearchDateEntryBox.get() \
                               , self.P1_RadioVariety.get())
        count = 0

        if self.set_xml.xml_status == 200:
            self.P1_root = ET.fromstring(self.set_xml.xml_text)
            if self.P1_RadioVariety.get() == 1:
                for child in self.P1_root.find("dailyBoxOfficeList"):
                    self.P1_MovieList[count].configure(text=child.find('movieNm').text)
                    count += 1
            else:
                for child in self.P1_root.find("weeklyBoxOfficeList"):
                    self.P1_MovieList[count].configure(text=child.find('movieNm').text)
                    count += 1

    def P1_SearchBoxofficeInfo(self, name):  # 입력한 박스오피스 정보 출력, 날짜가 입력되어야함
        self.set_xml.Naver_xml_request(name)
        self.P1_ClearLabel()

        openDt = ''  # 개봉연도 저장 변수, 제대로된 포스터 이미지 찾기위함

        if self.set_xml.xml_status == 200:
            self.P1_Nroot = ET.fromstring(self.set_xml.Nxml_text)

            if self.P1_RadioVariety.get() == 1:
                for child in self.P1_root.find("dailyBoxOfficeList"):
                    if child.find('movieNm').text == name:
                        self.P1_Sranklabel.configure(text="순위: " + child.find("rank").text + "위")
                        self.P1_SopenDtlabel.configure(text="개봉일: " + child.find("openDt").text)
                        self.P1_SaudiAcclabel.configure(text="누적관객수: " + child.find("audiAcc").text + "명")
                        self.P1_SsalesAcclabel.configure(text="누적매출액: " + child.find("salesAcc").text + "원")
                        openDt = child.find("openDt").text
                        break
            else:
                for child in self.P1_root.find("weeklyBoxOfficeList"):
                    if child.find('movieNm').text == name:
                        self.P1_Sranklabel.configure(text="순위: " + child.find("rank").text + "위")
                        self.P1_SopenDtlabel.configure(text="개봉일: " + child.find("openDt").text)
                        self.P1_SaudiAcclabel.configure(text="누적관객수: " + child.find("audiAcc").text + "명")
                        self.P1_SsalesAcclabel.configure(text="누적매출액: " + child.find("salesAcc").text + "원")
                        openDt = child.find("openDt").text
                        break

            for child in self.P1_Nroot.find('channel'):
                if child.text == None:
                    if child.find('pubDate').text <= openDt[0:4]:
                        # self.Sactorlabel.configure(text="출연 배우: "+child.find('actor').text.replace('|','\t\n'))
                        # self.Sdirectorlabel.configure(text="감독: "+child.find('director').text.replace('|',''))

                        image_url = child.find('image').text
                        with urllib.request.urlopen(image_url) as u:
                            raw_data = u.read()
                        image = Image.open(BytesIO(raw_data))
                        movie_image = ImageTk.PhotoImage(image)
                        self.P1_Simage.configure(image=movie_image)
                        self.P1_Simage.image = movie_image
                        break

    def Work_page1(self):
        self.P1_InitTopText()
        self.P1_InitSearchListBox()
        self.P1_InitSearchBox()
        self.P1_InitSearchlabel()
