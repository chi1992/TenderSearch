from logging import exception
from holder_gui import *
from holder_webParser import Holder_webParser
from holder_workbook import Holder_workbook
from threading import Thread
from tkcalendar import Calendar
from tkinter import PhotoImage
from tkinter import ttk
from Holder_resources import *
from datetime import date
import requests
from lxml import etree
import xlwings as xw
import os

import time


class TenderSearcher():

    def __init__(self) -> None:
        self.holder_gui = Holder_gui()
        self.holder_workbook = Holder_workbook()
        self.holder_webParser = Holder_webParser()
    

        self.bind_events()

        self.holder_gui.root.mainloop()


    def bind_events(self):

        self.holder_gui.btn_execute.configure(command = self.pressed_execute)

    def pressed_execute(self):
        
        
        self.holder_gui.btn_execute.configure(state = 'disabled')
        var_state = self.holder_gui.vars['目前執行']
        t1 = Thread(target = self.execute)
        t1.start()


        # self.holder_workbook.wb.close()

    def execute(self):

        var_state = self.holder_gui.vars['目前執行']

        date = self.holder_gui.vars['日期'].get()
        dict_parsed = self.holder_webParser.get_dataDictOfDate(date, var_state)

        if dict_parsed == None:
            var_state.set('無資料')
            self.holder_gui.btn_execute.configure(state = 'active')
            self.holder_gui.btn_execute.configure(state = 'active')
            time.sleep(3)
            var_state.set('待命')
            return

        dict_filtered = {}

        var_state.set('關鍵字過濾中...')
        for k, v in dict_parsed.items():
            list_keywords = self.holder_gui.holder_resources.data['關鍵字']
            for keyword in list_keywords:
                if keyword in v[2]:
                    dict_filtered[k] = v
                    break
        dir_path = self.holder_gui.vars['資料夾'].get()
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = self.holder_gui.vars['全檔名'].get()

        self.holder_workbook.link_toNewBook()
        font_title = self.holder_gui.holder_resources.data['title font']
        font_content = self.holder_gui.holder_resources.data['content font']
        self.holder_workbook.load_dictFromParsed('勞務類全案件', dict_parsed, font_title, font_content, var_state)
        self.holder_workbook.load_dictFromParsed('關鍵字過濾案件', dict_filtered, font_title, font_content, var_state)
        var_state.set('存檔中...')
        self.holder_workbook.save_book(path)

        self.holder_gui.btn_execute.configure(state = 'active')
        var_state.set('完成！')
        time.sleep(3)
        var_state.set('待命')






# holder_gui = Holder_gui()

# holder_gui.root.mainloop()


if __name__ == '__main__':

    TenderSearcher()