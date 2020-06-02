from tkinter import *
from tkinter import font
import tkinter.messagebox
import xml.etree.ElementTree as ET
import urllib
import http.client

#print(req.status,req.reason)
#print(req.read().decode('utf-8'))

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

    def Search(self):
        self.conn = http.client.HTTPConnection("kobis.or.kr")
        self.conn.request("GET",
                     "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=0f7d6638c03ecc9885350d92093d8f8b&targetDt=20200404")
        self.req = self.conn.getresponse()
        self.xml_status = self.req.status
        self.xml_text = self.req.read().decode('utf-8')

        self.root = ET.fromstring(self.xml_text)

        for child in self.root.find("dailyBoxOfficeList"):
            if child.find('movieNm').text == self.SearchEntryBox.get():
                self.Sranklabel.configure(text="순위: " + child.find("rank").text + "위")
                self.SopenDtlabel.configure(text="개봉일: " + child.find("openDt").text)
                self.SaudiAcclabel.configure(text="누적관객수: " + child.find("audiAcc").text + "명")
                self.SsalesAcclabel.configure(text= "누적매출액: "+child.find("salesAcc").text+"원")







mainGUI()



