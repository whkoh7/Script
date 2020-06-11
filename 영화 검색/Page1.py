from tkinter import *
from tkinter import font
import tkinter.ttk
from io import BytesIO
from PIL import Image, ImageTk
import tkinter.messagebox
from Set_Parsing import *

class Page1():
    def __init__(self,window):
        self.window = window
        self.fontstyle1 = font.Font(self.window, size=12, family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=11, weight='bold', family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.set_Parsing = Set_Parsing()
        self.set_Parsing_od = []*4
        for i in range(4):
            self.set_Parsing_od.append(Set_Parsing())


    def InitTopText(self):
        self.Toptext = Label(self.window, font=self.Topfontstyle, text="박스오피스 검색")
        self.Toptext.pack()

    def InitSearchListBox(self):
        self.MovieList = [] * 10
        self.Rank_Label = [] * 10
        for i in range(10):
            self.MovieList.append(
                Button(self.window, font=self.fontstyle2, overrelief="solid", width=28, height=1, bg='white',
                       command=lambda a=i: self.SearchBoxofficeInfo(self.MovieList[a]['text'])))
            self.MovieList[i].place(x=100, y=80 + i * 45)
            self.Rank_Label.append(Label(self.window, font=self.fontstyle2, text=str(i + 1) + "."))
            self.Rank_Label[i].place(x=60, y=85 + i * 45)

    def InitSearchBox(self):
        self.SearchYearEntryBoxlabel = Label(self.window, font=self.fontstyle1, text="년도: ")
        self.SearchYearEntryBoxlabel.place(x=310, y=50)
        self.SearchYearEntryBox = Entry(self.window, font=self.fontstyle1, width=6)
        self.SearchYearEntryBox.place(x=360, y=50)

        self.SearchDateEntryBoxlabel = Label(self.window, font=self.fontstyle1, text="월/일: ")
        self.SearchDateEntryBoxlabel.place(x=430, y=50)
        self.SearchDateEntryBox = Entry(self.window, font=self.fontstyle1, width=6)
        self.SearchDateEntryBox.place(x=490, y=50)

        self.SearchMovieListButton = Button(self.window, overrelief='solid', text="일/주간박스오피스 출력",
                                               command=self.SearchBoxofficeList)
        self.SearchMovieListButton.place(x=560, y=50)

        self.RadioVariety = tkinter.IntVar()
        self.DailySelectionButton = Radiobutton(self.window, value=1, text="일간", variable=self.RadioVariety,
                                                   command=self.ClearList)
        self.DailySelectionButton.place(x=90, y=50)
        self.WeeklySelectionButton = Radiobutton(self.window, value=2, text="주간", variable=self.RadioVariety,
                                                    command=self.ClearList)
        self.WeeklySelectionButton.place(x=150, y=50)

    def InitSearchlabel(self):
        self.Sranklabel = Label(self.window, font=self.fontstyle1, text="")
        self.Sranklabel.place(x=380, y=425)
        self.SopenDtlabel = Label(self.window, font=self.fontstyle1, text="")
        self.SopenDtlabel.place(x=380, y=450)
        self.SaudiAcclabel = Label(self.window, font=self.fontstyle1, text="")
        self.SaudiAcclabel.place(x=380, y=475)
        self.SsalesAcclabel = Label(self.window, font=self.fontstyle1, text="")
        self.SsalesAcclabel.place(x=380, y=500)
        # self.Sactorlabel = Label(self.P1, font=self.Boxfontstyle, text="출연 배우: ")
        # self.Sactorlabel.place(x=300, y=175)
        # self.Sdirectorlabel = Label(self.P1, font=self.Boxfontstyle, text="감독: ")
        # self.Sdirectorlabel.place(x=300, y=300)
        self.Simage = Label(self.window, image='')
        self.Simage.place(x=380, y=100)

    def InitsalesAccGraph(self):
        self.temp_name = ''
        self.salesAccGraph = Canvas(self.window,relief='sunken',bd=1,bg='white',width=300,height=250)
        self.salesAccGraph.place(x=825,y=100)
        self.salesChange_od = ['0']*4
        self.salesAccGraphlabel = []*5
        for i in range(5):
            self.salesAccGraphlabel.append(Label(self.window, font=self.fontstyle1, text=""))
            self.salesAccGraphlabel[i].place(x=820 + (i * 70), y=340)
        self.salesAccGraphlabel.append(Label(self.window, font=self.fontstyle1, text=""))
        self.salesAccGraphlabel[5].place(x=725 , y=215)
        self.Draw_Graph_Button=Button(self.window,font=self.fontstyle1, text="최근 매출액 비교 그래프 출력",command=lambda n=self.temp_name:self.Draw_Graph(self.temp_name))
        self.Draw_Graph_Button.place(x = 860, y = 375)
        self.Draw_Graph_Button['state'] = 'disabled'

    def ClearList(self):
        for i in range(10):
            self.MovieList[i].configure(text='')

    def ClearLabel(self):
        self.Sranklabel.configure(text="순위: ")
        self.SopenDtlabel.configure(text="개봉일: ")
        self.SaudiAcclabel.configure(text="누적관객수: ")
        self.SsalesAcclabel.configure(text="누적매출액: ")
        # self.Sactorlabel.configure(text="출연 배우: ")
        # self.Sdirectorlabel.configure(text="감독: ")
        self.Simage.configure(image='')

    def SearchBoxofficeList(self):  # 입력한 날짜의 개봉한 박스오피스 출력
        self.set_Parsing.Movie_xml_request(self.SearchYearEntryBox.get() \
                               , self.SearchDateEntryBox.get() \
                               , self.RadioVariety.get())
        count = 0

        if self.set_Parsing.xml_status == 200:
            self.root = ET.fromstring(self.set_Parsing.xml_text)
            if self.RadioVariety.get() == 1:
                for child in self.root.find("dailyBoxOfficeList"):
                    self.MovieList[count].configure(text=child.find('movieNm').text)
                    count += 1
            else:
                for child in self.root.find("weeklyBoxOfficeList"):
                    self.MovieList[count].configure(text=child.find('movieNm').text)
                    count += 1
        self.Draw_Graph_Button['state'] = 'disabled'

    def SearchBoxofficeInfo(self, name):  # 입력한 박스오피스 정보 출력, 날짜가 입력되어야함
        self.set_Parsing.Naver_xml_request(name)
        self.ClearLabel()
        self.temp_name = name

        openDt = ''  # 개봉연도 저장 변수, 제대로된 포스터 이미지 찾기위함

        if self.set_Parsing.xml_status == 200:
            self.Nroot = ET.fromstring(self.set_Parsing.Nxml_text)

            if self.RadioVariety.get() == 1:
                for child in self.root.find("dailyBoxOfficeList"):
                    if child.find("movieNm").text == name:
                        self.Sranklabel.configure(text="순위: " + child.find("rank").text + "위")
                        self.SopenDtlabel.configure(text="개봉일: " + child.find("openDt").text)
                        self.SaudiAcclabel.configure(text="누적관객수: " + child.find("audiAcc").text + "명")
                        self.SsalesAcclabel.configure(text="누적매출액: " + child.find("salesAcc").text + "원")
                        openDt = child.find("openDt").text
                        self.CurrentsalesAcc = child.find("salesAcc").text
                        break
            else:
                for child in self.root.find("weeklyBoxOfficeList"):
                    if child.find('movieNm').text == name:
                        self.Sranklabel.configure(text="순위: " + child.find("rank").text + "위")
                        self.SopenDtlabel.configure(text="개봉일: " + child.find("openDt").text)
                        self.SaudiAcclabel.configure(text="누적관객수: " + child.find("audiAcc").text + "명")
                        self.SsalesAcclabel.configure(text="누적매출액: " + child.find("salesAcc").text + "원")
                        openDt = child.find("openDt").text
                        self.CurrentsalesAcc = child.find("salesAcc").text
                        break

            for child in self.Nroot.find('channel'):
                if child.text == None:
                    if child.find('pubDate').text <= openDt[0:4]:
                        image_url = child.find('image').text
                        with urllib.request.urlopen(image_url) as u:
                            raw_data = u.read()
                        image = Image.open(BytesIO(raw_data))
                        image = image.resize((220, 314))
                        movie_image = ImageTk.PhotoImage(image)
                        self.Simage.configure(image=movie_image)
                        self.Simage.image = movie_image
                        break
            self.Draw_Graph_Button['state'] = 'active'

    def Draw_Graph(self,name):
        self.salesAccGraph.delete('all')
        for i in range(4):
            if i < 2:
                if len(str(int(self.SearchDateEntryBox.get()))) == 3:
                    self.set_Parsing_od[i].Movie_xml_request(self.SearchYearEntryBox.get() \
                                                                 , '0' + str(int(self.SearchDateEntryBox.get()) + (i - 2)) \
                                                                 , self.RadioVariety.get())
                else:
                    self.set_Parsing_od[i].Movie_xml_request(self.SearchYearEntryBox.get() \
                                                                 , str(int(self.SearchDateEntryBox.get()) + (i - 2)) \
                                                                 , self.RadioVariety.get())
            else:
                if len(str(int(self.SearchDateEntryBox.get()))) == 3:
                    self.set_Parsing_od[i].Movie_xml_request(self.SearchYearEntryBox.get() \
                                                                 , '0' + str(int(self.SearchDateEntryBox.get()) + (i - 1)) \
                                                                 , self.RadioVariety.get())
                else:
                    self.set_Parsing_od[i].Movie_xml_request(self.SearchYearEntryBox.get() \
                                                                 , str(int(self.SearchDateEntryBox.get()) + (i - 1)) \
                                                                 , self.RadioVariety.get())

        self.root_od = []

        for i in range(4):
            if self.set_Parsing_od[i].xml_status == 200:
                self.root_od.append(ET.fromstring(self.set_Parsing_od[i].xml_text))
                if self.RadioVariety.get() == 1:
                    for child in self.root_od[i].find("dailyBoxOfficeList"):
                        if child.find('movieNm').text == name:
                            self.salesChange_od[i] = child.find('salesChange').text
                            break
                else:
                    for child in self.root_od[i].find("weeklyBoxOfficeList"):
                        if child.find('movieNm').text == name:
                            self.salesChange_od[i] = child.find('salesChange').text
                            break
            else:
                self.salesChange_od[i] = '0'
            if i < 2:
                self.salesAccGraph.create_oval(10 + (70*i) - 5, 125-(float(self.salesChange_od[i])*1.2) - 5, \
                                            10 + (70*i)+ 5, 125-(float(self.salesChange_od[i])*1.2) + 5,fill='blue',outline = 'blue')
            else:
                self.salesAccGraph.create_oval(10 + (70 * (i+1)) - 5, 125 - (float(self.salesChange_od[i])*1.2) - 5, \
                                              10 + (70 * (i + 1)) + 5, 125 - (float(self.salesChange_od[i]) * 1.2) + 5,fill='blue',outline = 'blue')

        self.salesAccGraph.create_oval(10+140-5,125-5 ,10+140+5,125+5,fill='blue',outline = 'blue')
        self.salesAccGraph.create_line(10,125-float(self.salesChange_od[0])*1.2\
                                       ,10+70,125-float(self.salesChange_od[1])*1.2\
                                       ,10+140,125\
                                        ,10+210,125-float(self.salesChange_od[2])*1.2\
                                       ,10+280,125-float(self.salesChange_od[3])*1.2,width=2,fill='blue')
        for i in range(30):
            self.salesAccGraph.create_line(0+(i*10),125,5+(i*10),125)
        for i in range(5):
            if self.RadioVariety.get() == 1:
                if i < 2:
                    self.salesAccGraphlabel[i].configure(text=str(2-i)+"일전")
                elif i > 2:
                    self.salesAccGraphlabel[i].configure(text=str(i - 2)+"일후")
                else:
                    self.salesAccGraphlabel[i].configure(text='기준일')
            else:
                if i < 2:
                    self.salesAccGraphlabel[i].configure(text=str(2 - i) + "주전")
                elif i > 2:
                    self.salesAccGraphlabel[i].configure(text=str(i - 2) + "주후")
                else:
                    self.salesAccGraphlabel[i].configure(text='기준일')


    def Work_page(self):
        self.InitTopText()
        self.InitSearchListBox()
        self.InitSearchBox()
        self.InitSearchlabel()
        self.InitsalesAccGraph()
