from tkinter import *
from tkinter import font
from io import BytesIO
from PIL import Image, ImageTk
from Set_Parsing import *
import webbrowser

class page2:
    def __init__(self,window):
        self.window = window
        self.img = PhotoImage(file="resource/BackGround_2.png")
        self.bg = Label(self.window, image=self.img)
        self.bg.place(x=0, y=0)
        self.bg.image = self.img
        self.fontstyle1 = font.Font(self.window, size=12, family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=9, weight='bold', family='Consolas')
        self.Topfontstyle = font.Font(self.window, size=18, weight='bold', family='Consolas')
        self.movieListPage = 0
        self.set_Parsing = Set_Parsing()
        self.textbox = Text(self.window, width=35, height=10, font=self.fontstyle1)

    def InitTopText(self):
        pass


    def InitSearchBox(self):
        self.SearchMovieEntryBox = Entry(self.window, font=self.fontstyle1, width=20)
        self.SearchMovieEntryBox.place(x=275, y=50)

        Button_img = PhotoImage(file="resource/Button_Search.png")
        self.SearchMovieButton = Button(self.window, overrelief='solid', image=Button_img
                                               ,bg = "dark slate gray",command=self.SearchMovieList)
        self.SearchMovieButton.image=Button_img
        self.SearchMovieButton.place(x=465, y=45)


    def InitSearchlabel(self):
        self.MovieimageLabel = Label(self.window, image='',bg = "dark slate gray")

        self.textbox.place(x=800, y=325)

        Label_img = PhotoImage(file="resource/Button_Naver_Info.png")
        self.MovieLinkLabel = Label(self.window,image=Label_img,bg = "dark slate gray")
        self.MovieLinkLabel.image = Label_img

        Next_img = PhotoImage(file="resource/Button_Next.png")
        Prev_img = PhotoImage(file="resource/Button_Prev.png")
        self.NextListButton = Button(self.window, font=self.fontstyle1,bg = "dark slate gray"\
                                     , image=Next_img,command = self.Button_next)
        self.NextListButton.image = Next_img
        self.NextListButton.place(x=375, y=550)
        self.PrevListButton = Button(self.window, font=self.fontstyle1,bg = "dark slate gray"\
                                     , image=Prev_img,command = self.Button_prev)
        self.PrevListButton.image = Prev_img
        self.PrevListButton.place(x=300, y=550)
        self.PrevListButton['state'] = 'disabled'
        self.NextListButton['state'] = 'disabled'


    def SearchMovieList(self):
        self.set_Parsing.Naver_xml_request(self.SearchMovieEntryBox.get())
        count = 0
        index_num = [0]*50
        self.movieListPage = 0
        self.PrevListButton['state'] = 'disabled'

        if self.set_Parsing.Nxml_status == 200:
            self.Nroot = ET.fromstring(self.set_Parsing.Nxml_text)

            try:
                for i in range(len(self.MovieName)):
                    self.MovieName[i].destroy()
                    self.Movieimage[i].destroy()
                del self.MovieName
                del self.Movieimage
                del self.MovieName_text
                del self.MoviePubdate
            except AttributeError:
                pass

            self.MovieName = [] * 50
            self.Movieimage = [] * 50
            self.MovieName_text = [] * 50
            self.MoviePubdate = [] * 50

            for child in self.Nroot.find('channel'):
                if child.text == None:
                    self.MovieName_text.append(child.find('title').text)
                    self.MoviePubdate.append(child.find('pubDate').text)
                    temp = child.find('title').text.replace('<b>','')
                    temp = temp.replace('</b>','')
                    temp = temp.replace('&amp;', '')
                    self.MovieName.append(Label(self.window,font=self.fontstyle2,fg = "white", bg = "dark slate gray", text=temp[0:10]))
                    image_url = child.find('image').text
                    index_num[count] = count
                    if image_url != None:
                        with urllib.request.urlopen(image_url) as u:
                            raw_data = u.read()
                        image = Image.open(BytesIO(raw_data))
                        movie_image = ImageTk.PhotoImage(image)
                        self.Movieimage.append(Button(self.window, image=movie_image\
                                                      ,bg = "dark slate gray",command=lambda n=index_num[count] :self.SearchMovieInfo(n)))
                        self.Movieimage[count].image = movie_image
                    else:
                        self.Movieimage.append(Button(self.window, image='', text = '이미지 없음' \
                                                      ,fg = "white", bg = "dark slate gray", command=lambda n=index_num[count]: self.SearchMovieInfo(n)))
                    count += 1
        self.MovieListSet()
        if len(self.MovieName)//10 != 0:
            self.NextListButton['state'] = 'active'

    def Button_next(self):
        if self.movieListPage < (len(self.MovieName)//10):
            self.movieListPage += 1
            if self.movieListPage == 5:
                self.movieListPage = 4
            self.MovieListSet()
            self.PrevListButton['state'] = 'active'
            if self.movieListPage == len(self.MovieName)//10 or self.movieListPage == 4:
                self.NextListButton['state'] = 'disabled'

    def Button_prev(self):
        if self.movieListPage != 0:
            self.movieListPage -= 1
            self.MovieListSet()
            if self.movieListPage != 0:
                self.PrevListButton['state'] = 'active'
                self.NextListButton['state'] = 'active'
            else:
                self.PrevListButton['state'] = 'disabled'
                self.NextListButton['state'] = 'active'



    def MovieListSet(self):
        for i in range(0, len(self.MovieName)):
            if self.movieListPage==0:
                if 0 <= i and i < 5 :
                    self.MovieName[i].place(x=20 + 150 * (i), y=90)
                    self.Movieimage[i].place(x=25 + 150 * (i), y=110)

                elif i >= 5 and i < 10 :
                    self.MovieName[i].place(x=20 + 150 * (i - 5), y=300)
                    self.Movieimage[i].place(x=25 + 150 * (i - 5), y=320)
                else:
                    self.MovieName[i].place(x=-200, y=-200)
                    self.Movieimage[i].place(x=-200, y=-200)
            else:
                if 10 * self.movieListPage <= i and i < 5 + 10 *self.movieListPage:
                    self.MovieName[i].place(x=20 + 150 * (i - 10 * self.movieListPage), y=90)
                    self.Movieimage[i].place(x=25 + 150 * (i - 10 * self.movieListPage), y=110)

                elif i >= 5 + 10 * self.movieListPage and i < 10 + 10 * self.movieListPage:
                    self.MovieName[i].place(x=20 + 150 * (i - 5 - (10 * self.movieListPage)), y=300)
                    self.Movieimage[i].place(x=25 + 150 * (i - 5 - (10 * self.movieListPage)), y=320)
                else:
                    self.MovieName[i].place(x=-200, y=-200)
                    self.Movieimage[i].place(x=-200, y=-200)



    def SearchMovieInfo(self,n):
        self.MovieimageLabel.configure(image='')
        self.MovieLinkLabel.configure(relief='flat')
        movieLink = ''
        self.textbox.delete("1.0", "end")
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
                    temp2 = child.find('title').text.replace('<b>', '')
                    temp2 = temp2.replace('</b>', '')
                    temp2 = temp2.replace('&amp;', '')
                    self.textbox.insert(CURRENT,temp2+'\n\n')
                    self.textbox.insert(CURRENT,'제작 연도: ' + child.find('pubDate').text+'\n')
                    self.textbox.insert(CURRENT,'평점: ' + child.find('userRating').text+'\n')
                    self.textbox.insert(CURRENT,'감독: ' + child.find('director').text.replace('|', ' ')+'\n')
                    try:
                        actor_list = temp1.split('|')
                        actor_list.append(' ')
                        actor_list.append(' ')
                        self.textbox.insert(CURRENT,'출연 배우: ' + actor_list[0] + ', ' \
                                                            + actor_list[1] + ', ' + actor_list[2] + '\n')
                    except AttributeError:
                        pass
                    self.MovieLinkLabel.configure(relief='ridge')
                    movieLink = child.find('link').text
                    MovieSummary = self.set_Parsing.Naver_HTML_request(movieLink)
                    if MovieSummary != "네이버 영화 : 영화정보":
                        self.textbox.insert(CURRENT,'\n'+'줄거리: '+MovieSummary)
                    else:
                        pass
        self.MovieimageLabel.place(x=800, y=50)
        self.MovieLinkLabel.place(x=880, y=525)
        self.MovieLinkLabel.bind('<Button-1>',lambda a:webbrowser.open(movieLink))



    def Work_page(self):
        self.InitTopText()
        self.InitSearchBox()
        self.InitSearchlabel()