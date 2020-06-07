from tkinter import *
from tkinter import font
from io import BytesIO
from PIL import Image, ImageTk
from Set_Parsing import *
import webbrowser

class Page2:
    def __init__(self,window):
        self.window = window
        self.fontstyle1 = font.Font(self.window, size=12, family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=9, weight='bold', family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.set_Parsing = Set_Parsing()

    def InitTopText(self):
        self.Toptext = Label(self.window, font=self.Topfontstyle, text="영화 정보 검색")
        self.Toptext.pack()


    def InitSearchBox(self):
        self.SearchMovieEntryBox = Entry(self.window, font=self.fontstyle1, width=20)
        self.SearchMovieEntryBox.place(x=250, y=50)

        self.SearchMovieButton = Button(self.window, overrelief='solid', text="검색",
                                               command=self.SearchMovieList)
        self.SearchMovieButton.place(x=440, y=50)


    def InitSearchlabel(self):
        self.MovieName=[]*20
        self.Movieimage=[]*20
        self.MovieName_text = []*20
        self.MoviePubdate = [] * 20

        self.MovieimageLabel = Label(self.window, image='')
        self.MovieimageLabel.place(x=800,y=50)

        self.MovieNameLabel = Label(self.window, font=self.fontstyle1, text="")
        self.MovieNameLabel.place(x=800, y=300)

        self.MoviePubDateLabel = Label(self.window, font=self.fontstyle1, text="")
        self.MoviePubDateLabel.place(x=800, y=325)

        self.MovieUserRatingLabel = Label(self.window, font=self.fontstyle1, text="")
        self.MovieUserRatingLabel.place(x=800, y=350)

        self.MovieDirectorLabel = Label(self.window, font=self.fontstyle1, text="")
        self.MovieDirectorLabel.place(x=800, y=375)

        self.MovieActorLabel = Label(self.window, font=self.fontstyle1, text="")
        self.MovieActorLabel.place(x=800, y=400)

        self.MovieSummaryLabel = Label(self.window, font=self.fontstyle1, text="")
        self.MovieSummaryLabel.place(x=800, y=480)

        self.MovieLinkLabel = Label(self.window, font=self.fontstyle1, text="",width=15)
        self.MovieLinkLabel.place(x=1000, y=300)

        self.NextListButton = Button(self.window, font=self.fontstyle1, text="다음")
        self.NextListButton.place(x=350, y=550)
        self.PrevListButton = Button(self.window, font=self.fontstyle1, text="이전")
        self.PrevListButton.place(x=300, y=550)



    def SearchMovieList(self):
        self.set_Parsing.Naver_xml_request(self.SearchMovieEntryBox.get())
        count = 0
        index_num = [0]*20

        if self.set_Parsing.Nxml_status == 200:
            self.Nroot = ET.fromstring(self.set_Parsing.Nxml_text)

            for i in range(20):
                try:
                    self.MovieName[i].configure(text='')
                    self.Movieimage[i].configure(image='')
                except IndexError:
                    pass

            del self.MovieName[:]
            del self.Movieimage[:]

            for child in self.Nroot.find('channel'):
                if child.text == None:
                    self.MovieName_text.append(child.find('title').text)
                    self.MoviePubdate.append(child.find('pubDate').text)
                    temp = child.find('title').text.replace('<b>','')
                    temp = temp.replace('</b>','')
                    temp = temp.replace('&amp;', '')
                    self.MovieName.append(Label(self.window,font=self.fontstyle2, text=temp[0:10]))
                    image_url = child.find('image').text
                    index_num[count] = count
                    if image_url != None:
                        with urllib.request.urlopen(image_url) as u:
                            raw_data = u.read()
                        image = Image.open(BytesIO(raw_data))
                        movie_image = ImageTk.PhotoImage(image)
                        self.Movieimage.append(Button(self.window, image=movie_image\
                                                      ,command=lambda n=index_num[count] :self.SearchMovieInfo(n)))
                        self.Movieimage[count].image = movie_image
                    else:
                        self.Movieimage.append(Button(self.window, image='', text = '이미지 없음' \
                                                      , command=lambda n=index_num[count]: self.SearchMovieInfo(n)))
                    count += 1

            # 검색한 결과 위치
            for i in range(0,len(self.MovieName)):
                if i < 5:
                    self.MovieName[i].place(x=20+150*i,y=90)
                    self.Movieimage[i].place(x=25 + 150 * i, y=110)

                elif i>=5 and i<10:
                    self.MovieName[i].place(x=20 + 150 * (i-5), y=300)
                    self.Movieimage[i].place(x=25 + 150 * (i-5), y=320)


    def SearchMovieInfo(self,n):
        self.MovieimageLabel.configure(image='')
        self.MoviePubDateLabel.configure(text='제작 연도: ')
        self.MovieUserRatingLabel.configure(text='평점: ')
        self.MovieDirectorLabel.configure(text='감독: ')
        self.MovieActorLabel.configure(text='출연 배우: ')
        self.MovieSummaryLabel.configure(text='줄거리: ')
        self.MovieLinkLabel.configure(text='',relief='flat')
        movieLink = ''
        MovieSummary=''

        for child in self.Nroot.find('channel'):
            if child.text == None:
                if child.find('title').text == self.MovieName_text[n]\
                        and child.find('pubDate').text==self.MoviePubdate[n]:
                    if child.find('image').text != None:
                        image_url = child.find('image').text
                        with urllib.request.urlopen(image_url) as u:
                            raw_data = u.read()
                        image = Image.open(BytesIO(raw_data))
                        image = image.resize((150, 230))
                        movie_image = ImageTk.PhotoImage(image)
                        self.MovieimageLabel.configure(image=movie_image)
                        self.MovieimageLabel.image = movie_image
                    temp1 = child.find('actor').text
                    actor_list = temp1.split('|')
                    actor_list.append('none')
                    actor_list.append('none')
                    temp2 = child.find('title').text.replace('<b>', '')
                    temp2 = temp2.replace('</b>', '')
                    temp2 = temp2.replace('&amp;', '')
                    self.MovieNameLabel.configure(text=temp2)
                    self.MoviePubDateLabel.configure(text='제작 연도: '+child.find('pubDate').text)
                    self.MovieUserRatingLabel.configure(text='평점: ' + child.find('userRating').text)
                    self.MovieDirectorLabel.configure(text='감독: ' + child.find('director').text.replace('|',''))
                    self.MovieActorLabel.configure(text='출연 배우: ' + actor_list[0]+'\n'+'\t'\
                                                        +actor_list[1]+'\n'+'\t'+actor_list[2]+'\n'+'\t')
                    self.MovieLinkLabel.configure(text='정보 보기',relief='ridge')
                    movieLink = child.find('link').text
                    MovieSummary = self.set_Parsing.Naver_HTML_request(movieLink)
                    MovieSummary = MovieSummary[:20] + "\n" + MovieSummary[20:]
                    MovieSummary = MovieSummary[:40] + "\n" + MovieSummary[40:]
                    self.MovieSummaryLabel.configure(text='줄거리: '+MovieSummary)


        self.MovieLinkLabel.bind('<Button-1>',lambda a:webbrowser.open(movieLink))



    def Work_page(self):
        self.InitTopText()
        self.InitSearchBox()
        self.InitSearchlabel()