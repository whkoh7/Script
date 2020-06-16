from tkinter import *
from tkinter import font
import tkinter.ttk
import Page1
import Page2
import Page3
import Page4

window = Tk()
window.title("박스오피스 정보 검색")
notebook = tkinter.ttk.Notebook(window, width=1200, height=600)
notebook.pack()

P1 = Frame(window)
notebook.add(P1, text="박스오피스")
_page1 = Page1.page1(P1)

P2 = Frame(window)
notebook.add(P2, text="영화검색")
_page2 = Page2.page2(P2)

P3 = Frame(window)
notebook.add(P3, text="배우검색")
_page3 = Page3.page3(P3)

P4 = Frame(window)
notebook.add(P4, text="메일")
_page4 = Page4.page4(P4)

# 메일로 보낼 내용 page4에 보내는 벤자민 버튼
button_img = PhotoImage(file = "resource/Button_Save.png")
gettext_button1 = Button(P1,image=button_img,bg = "dark slate gray",command=lambda n=_page1.textbox.get("1.0","end"):\
                     _page4.textbox.insert(CURRENT,"---------------------------------\n"\
                                           +_page1.SearchYearEntryBox.get()+_page1.SearchDateEntryBox.get()+"\n"\
                                           +_page1.textbox.get("1.0","end")))
gettext_button1.place(x=750,y=545)
gettext_button2 = Button(P2,image=button_img,bg = "dark slate gray",command=lambda n=_page2.textbox.get("1.0","end"):\
                     _page4.textbox.insert(CURRENT,"---------------------------------\n"+_page2.textbox.get("1.0","end")))
gettext_button2.place(x=800,y=525)
gettext_button3 = Button(P3,image=button_img,bg = "dark slate gray",command=lambda n=_page3.textbox.get("1.0","end"):\
                     _page4.textbox.insert(CURRENT,"---------------------------------\n"+_page3.textbox.get("1.0","end")))
gettext_button3.place(x=100,y=525)

_page1.Work_page()
_page2.Work_page()
_page3.Work_page()
_page4.Work_page()

window.mainloop()