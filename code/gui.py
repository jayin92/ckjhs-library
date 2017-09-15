from tkinter import *


class Manager:

    def __init__(self, master):
        master.title('建國國中書籍借閱系統')
        frame = Frame(master)
        frame.pack()

        self.welcomeText = Label(frame,
                                 text='建國國中數理資優班圖書借閱系統',
                                 bg='green',
                                 fg='pink')
        self.welcomeText.pack(side='top', fill=X)
        self.welcomeText.config(font=("Courier", 44))

        self.borrowButton = Button(frame, text='借書', fg='blue',
                                   command=self.borrow)
        self.borrowButton.pack(side='top')
        self.borrowButton.config(font=("Courier", 30))

        self.rentButton = Button(frame, text='還書', fg='green',
                                 command=self.rent)
        self.rentButton.pack(side='top')
        self.rentButton.config(font=("Courier", 30))
        self.quitButton = Button(frame, text='quit', fg='red',
                                 command=quit)
        self.quitButton.pack(side='top')

    def borrow(self):
        print('借書')

    def rent(self):
        print('還書')
root = Tk()
b = Manager(root)
root.mainloop()
