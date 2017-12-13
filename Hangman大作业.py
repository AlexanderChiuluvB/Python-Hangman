""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#该程序另外使用的第三方库有tkinter,tkinter.tkk,老师电脑
#没装的话可以pip一下
""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from time import time
import random
import string
import datetime
import csv

class Hangman():
    def __init__(self):
        # 初始化csv数据
        with open('data.csv', 'a+')as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['开始时间', '游戏时间(s)', '单词','输入记录'])
        # 读取文件
        with open('words.txt') as datafile :
            line = datafile.read()
            wordlist = line.split()
            self.data=list(map(str,wordlist)) #返回一个元素都为字符串的列表
        self.r=Tk() #初始化窗口
        self.r.title('Hangman猜单词')
        self.hidden=StringVar()
        self.guesses=StringVar()
        self.first=True #默认是第一次
        self.frame=Labelframe(self.r,height=300)#设置frame
        self.frame.grid(column=1, row=0)#设置窗格
        Label(self.frame, text='你猜过的 : ').grid(column=0, row=0, sticky=(N, E))
        Label(self.frame, textvariable=self.guesses).grid(column=1, row=0, sticky=(N, W))
        Label(self.frame, textvariable=self.hidden).grid(column=0, row=3, columnspan=2)
        self.entry = Entry(self.frame)#设置输入框
        self.entry.grid(column=0, row=5, columnspan=2, sticky=S)
        self.entry.bind('<Return>', self.guessLetter)#输入值即self.guessLetter
        Button(self.frame, text='确定', command=self.guessLetter).grid(column=0, row=7, columnspan=2, sticky=S)#设置按钮
        self.man = Canvas(self.r, width=200, height=300, bg='white')#设置画布
        #画绞刑架
        self.man.grid(column=0, row=0)
        self.man.create_line(10, 285, 190, 285, width=10)
        self.man.create_line(170, 285, 170, 20, width=5)
        self.man.create_line(35, 20, 172, 20, width=5)
        self.man.create_line(110, 20, 110, 40, width=4)
        self.initialize()#初始化

    def getWord(self):
        self.word=random.choice(self.data)
        return self.word,('_ '*len(self.word)).strip()

    def win(self):
        self.t2=time()#记录赢的时候的时间
        with open('data.csv', 'a+')as f: #记录这一次的信息
            writer = csv.writer(f, delimiter=',')
            writer.writerow([self.today, '%.2f'%(self.t2 - self.t1),self.word,self.guesses_])
        #此处参考了网上部分tkinter的代码
        self.frame.grid_forget()
        self.frame2 = Labelframe(self.r,text='你赢了!',height=300)
        self.frame2.grid(column=1,row=0)
        Label(self.frame2,text='正确答案 : '+self.word).grid(column=0,row=0,columnspan=2)
        Button(self.frame2,text='不玩了',command=self.r.quit).grid(column=1,row=1,columnspan=2)
        Button(self.frame2,text='再来一次',command=self.initialize).grid(column=0,row=1)


    def lose(self):
        self.t2 = time()  # 记录赢的时候的时间
        with open('data.csv', 'a+')as f:  # 记录这一次的信息
            writer = csv.writer(f, delimiter=',')
            writer.writerow([self.today, '%.2f' % (self.t2 - self.t1), self.word, self.guesses_])
        # 此处参考了网上部分tkinter的代码
        self.frame.grid_forget()
        self.frame2 = Labelframe(self.r, text='你输了!', height=300)
        self.frame2.grid(column=1, row=0)
        Label(self.frame2, text='正确答案 : ' + self.word).grid(column=0, row=0, columnspan=2)
        Button(self.frame2, text='不玩了', command=self.r.quit).grid(column=1, row=1, columnspan=2)
        Button(self.frame2, text='再来一次', command=self.initialize).grid(column=0, row=1)



    #这里参考了网上一些tkinter的代码
    def show(self):#默认为5，每猜错一次+1，直到猜错六次
        if self.s == 5:
            self.man.itemconfigure('5',outline='black')
        elif self.s < 10:
            self.man.itemconfigure(str(self.s),fill='black')
        else:
            self.man.itemconfigure(str(self.s), fill='black')
            self.lose()
        self.s+=1

    def guessLetter(self,event=None):
        letterguessed=self.entry.get()
        self.entry.delete(0,END)#每次输入字母后清空
        index=[]

        if len(letterguessed)>1:
            messagebox.showinfo(title='Error', message='一次只能输入一个字符')
        elif letterguessed not in string.ascii_letters:
            messagebox.showinfo(title='Error', message='只能输入字母')

        for idx in range(len(self.word)):
            let=self.word[idx]
            if letterguessed==let:
                index.append(idx)#把存在于这个单词的字母所在序数存储在index这个列表当中
        if letterguessed in self.guesses_:
            messagebox.showinfo(title='Error', message='你已经猜过了')
        elif index!=[]: #如果猜中了，把'_'替换为那个字母
            self.replaceBlankWithLetter(index)
        else:
            self.show()#否则显示人的一部分
        self.guesses_ = self.guesses_ + letterguessed + ',' #以逗号分隔开来
        self.guesses.set(self.guesses_)#返回一个集合

    def replaceBlankWithLetter(self,index): #把空格替换为字母
        self.hidden_=self.hidden_.split()
        for idx in index:
            self.hidden_[idx]=self.word[idx]
        self.hidden_=' '.join(self.hidden_)
        self.hidden.set(self.hidden_)
        if not '_' in self.hidden_:
            self.win()



    def initialize(self):
        self.guesses_ = ''
        self.word = self.getWord()
        self.hidden_ = self.word[1]
        self.word = self.word[0]
        self.hidden.set(self.hidden_)
        self.guesses.set('')
        self.today = datetime.datetime.today()#记录开始玩的年月日
        self.t1 = time()#记录开始玩的时间
        self.s = 5
        if not self.first:#如果是重新再玩一次的情况
            self.frame2.destroy()#取消赢了或输了的时候的frame
            self.man.itemconfigure('5', outline='white')
            self.man.itemconfigure('A', fill='white')
            self.frame.grid(column=1, row=0)
        else:
            self.first = False #如果是第一次玩的情况
            #画人
            self.man.create_oval(90, 40, 130, 80, width=3, outline='white') #画人头
            self.man.create_line(110, 90, 70, 95, width=3, fill='white', tags='A', smooth=True)#左手
            self.man.create_line(110, 80, 110, 180, width=3, fill='white', tags='A', smooth=True)#躯干
            self.man.create_line(110, 90, 150, 95, width=3, fill='white', tags='A', smooth=True)#右手
            self.man.create_line(110, 180, 80, 230, width=3, fill='white', tags='A', smooth=True)#左脚
            self.man.create_line(110, 180, 140, 230, width=3, fill='white', tags='A', smooth=True)#右脚


    def start(self):
        self.r.mainloop()

if __name__=='__main__':
    Hangman=Hangman()#初始化实类
    Hangman.start()
