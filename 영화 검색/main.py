from Page1 import *
from Page2 import *

class mainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("박스오피스 정보 검색")
        self.notebook = tkinter.ttk.Notebook(self.window, width=1200, height=600)
        self.notebook.pack()

        self.P1 = Frame(self.window)
        self.notebook.add(self.P1, text="박스오피스")
        self.page1 = Page1(self.P1)

        self.P2 = Frame(self.window)
        self.notebook.add(self.P2, text="영화검색")
        self.page2 = Page2(self.P2)

        self.page1.Work_page()
        self.page2.Work_page()

        self.window.mainloop()

mainGUI()