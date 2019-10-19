
from handlers import *
from util import *
from rules import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, askdirectory
from os import system
import sys
import re


class Parser:
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilters(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                    if rule in self.rules:
                        if rule.condition(block):
                            last = rule.action(block, self.handler)
                            if last:
                                break
        self.handler.end('document')


class BasicTextParser(Parser):
    """
    建立添加了具体规则和过滤器的子类
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilters(r'\*(.+?)\*', 'emphasis')
        self.addFilters(r'(http://[\.a-zA-Z0-9/]+)', 'url')
        self.addFilters(r'([\.a-zA-Z0-9]+@[\.a-zA-Z0-9]+[.a-zA-Z]+)', 'mail')


class File:
    def __init__(self, var1):
        self.file1 = ''
        self.file2 = ''
        self.var1 = var1

    def searchfile1(self):
        self.file1 = askopenfilename()
        if self.file1:
            self.var1.set('Your TXT file:'+self.file1)
        else:
            self.file1 = ''
    def searchfile2(self):
        self.file2 = askdirectory()
        # print(self.file2)

    def transition(self):
        try:
            with open(self.file1) as f:
                self.searchfile2()
                with open(self.file2 + '/new2018.html', 'w') as g:
                    # print('label1')
                    temp = sys.stdout
                    sys.stdout = g
                    handler = HTMLRenderer()
                    parser = BasicTextParser(handler)
                    parser.parse(f)
                    sys.stdout = temp
        except FileNotFoundError:
            showerror("Error", "Please give a right file")
        except TypeError:
            pass
        else:
            system(' google-chrome {}'.format(self.file2 + '/new2018.html'))

def start():
    top = Tk()
    var = StringVar()
    file = File(var)
    top.title('TXT to HTML')
    Label(top, textvariable=var).pack(side=LEFT, expand=False, fill=X)
    Button(text='select', command=file.searchfile1).pack(side=LEFT)
    Label(top, text=' ').pack(side=LEFT)
    Button(text='translate', command=file.transition).pack(side=LEFT)
    top.mainloop()
