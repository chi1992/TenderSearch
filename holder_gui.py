import tkinter as tk
from tkcalendar import Calendar
from tkinter import PhotoImage
from tkinter import ttk
from Holder_resources import *
from datetime import date


def doubleClicked_calendar():
    print('yo')
    pass
class Holder_gui():

    def __init__(self) -> None:
        
        self.root = tk.Tk() 
        a = 5
        self.root.title('Tender Searcher v1.0 © by Chase Chi')
        self.root.iconbitmap('./resources/icons/icon.ico')
        self.root.resizable(False, False)

        self.holder_resources = Holder_resources()
        self.calendar = Calendar(self.root)
        self.today = date.today()
        self.str_today = f'{self.today.year}/{self.today.month}/{self.today.day}'
        self.init_images()
        self.render_guiContainer()
        self.init_guis()
        self.calendar.grid(row = 0, column = 0)
        self.calendar.bind('<Enter>', self.doubleClicked_calendar)
        pass

    def doubleClicked_calendar(self, e1):

        print(self.get_dateFromCalendar())

        pass

    def get_dateFromCalendar(self):

        return self.calendar.get_date()

    def init_guis(self):
        
        self.init_vars()
        self.init_calendar()
        self.init_executeRibben()
        self.init_kewordEditor()
        self.init_progressRibben()

        self.bind_events()

    def init_vars(self):

        self.vars = {
            '檔名': tk.StringVar(value = self.holder_resources.data['檔名']),
            '資料夾': tk.StringVar(value = self.holder_resources.data['資料夾']),
            '日期': tk.StringVar(value = self.str_today),
            '檔名日期': tk.StringVar(),
            '編輯關鍵字': tk.StringVar(),
            '全檔名': tk.StringVar(),
            '目前執行': tk.StringVar(value = '待命')
        }

        self.change_fileNameDate()
        self.change_fullFileName()

    def init_executeRibben(self):
        master = self.gui_containers['execute ribben']
        master.configure(highlightthickness = 1, highlightbackground = 'grey50')
        # master.grid(ipadx = 1, ipady = 1)
        self.btn_execute = ttk.Button(master, image = self.images['execute2'])

        self.lbl_fileNameTitle = ttk.Label(master, text = '檔案名稱:')
        self.lbl_dirNameTitle = ttk.Label(master, text = '資料夾:')

        self.ent_fileName = ttk.Entry(master, textvariable = self.vars['檔名'], width = 12, justify = 'right')
        self.ent_dirName = ttk.Entry(master, textvariable = self.vars['資料夾'], width = 12, justify = 'right')

        self.lbl_date = ttk.Label(master, textvariable = self.vars['檔名日期'], width = 12)

        self.btn_execute.grid(row = 0, column = 0, rowspan = 2)

        self.lbl_dirNameTitle.grid(row = 0, column = 1, sticky = 'e')
        self.ent_dirName.grid(row = 0, column = 2, pady = 1)

        self.lbl_fileNameTitle.grid(row = 1, column = 1, sticky = 'e')
        self.ent_fileName.grid(row = 1, column = 2, pady = 1)
        self.lbl_date.grid(row = 1, column = 3, sticky = 'news')


    def init_progressRibben(self):
    
        master = self.gui_containers['progress ribben']

        self.lbl_currentJobTitle = ttk.Label(master, text = '目前執行:')
        self.lbl_currentJob = ttk.Label(master, textvariable = self.vars['目前執行'], width = 30)
        self.pbr_currentJob = ttk.Progressbar(master)

        self.lbl_currentJobTitle.grid(row = 0, column = 0)
        self.lbl_currentJob.grid(row = 0, column = 1, sticky = 'nsw')
        # self.pbr_currentJob.grid(row = 1, column = 0, columnspan = 2, sticky = 'news')


    def init_kewordEditor(self):

        master = self.gui_containers['right']
        master.configure(highlightthickness = 1, highlightbackground = 'grey50')

        self.lbl_keywordEditorTitle = ttk.Label(master, text = '關鍵字列表')
        self.ent_keywordEditor = ttk.Entry(master, textvariable = self.vars['編輯關鍵字'])
        self.lbx_keywordEditor = tk.Listbox(master, selectmod = 'single', relief = 'flat', borderwidth = 1, highlightbackground = 'grey50')

        self.btn_addKeyword = ttk.Button(master, image = self.images['add'])
        self.btn_delKeyword = ttk.Button(master, image = self.images['delete'])

        self.lbl_keywordEditorTitle.grid(row = 0, column = 0)

        self.ent_keywordEditor.grid(row = 1, column = 0, sticky = 'news', pady = 1, padx = 1)
        self.btn_addKeyword.grid(row = 1, column = 1)

        self.lbx_keywordEditor.grid(row = 2, column = 0, sticky = 'news', pady = 2)
        self.btn_delKeyword.grid(row = 2, column = 1, sticky = 'n')


        list_keywords = self.holder_resources.data['關鍵字']

        for keyword in list_keywords:
            self.lbx_keywordEditor.insert('end', keyword)

    def bind_events(self):
        self.lbx_keywordEditor.bind("<<ListboxSelect>>", self.selected_keywordLbx)
        self.btn_addKeyword.configure(command = self.pressed_add)
        self.btn_delKeyword.configure(command = self.pressed_del)
        self.btn_execute.configure(command = self.pressed_execute)
        self.vars['日期'].trace_add('write', self.changed_date)
        self.vars['檔名'].trace_add('write', self.changed_fileName)
        self.vars['資料夾'].trace_add('write', self.changed_dirName)

    def selected_keywordLbx(self, e1):
        idx_selectedKeyword = self.lbx_keywordEditor.curselection()
        keyword_selected = self.lbx_keywordEditor.get(idx_selectedKeyword)
        self.vars['編輯關鍵字'].set(keyword_selected)
    
    def init_calendar(self):

        master = self.gui_containers['calendar container']
        self.cal_chooseDate = Calendar(master, font = ('微軟正黑體', 8), textvariable = self.vars['日期'], cursor = 'hand2', locale = 'zh')
        self.cal_chooseDate.grid(row = 0, column = 0, sticky = 'news')
        # self.ent_dirName.grid(row = 2, column = 0, columnspan = 2)

    def render_guiContainer(self):
        dict_layout = {
# gui layer 0
            "main": {
                "master": "",
                "no_row": 0,
                "no_col": 0,
                "sticky": "news",
                "span_row": 1,
                "span_col": 1,
                "row_stretched": [0, 1],
                "col_stretched": [1],
                "padx": 4,
                "pady": 4
            },

# gui layer 1
            "left": {
                "master": "main",
                "no_row": 0,
                "no_col": 0,
                "sticky": "news",
                "span_row": 1,
                "span_col": 1,
                "row_stretched": [1, 1],
                "col_stretched": [0, 1],
                "padx": 4,
                "pady": 2
            },
            "right": {
                "master": "main",
                "no_row": 0,
                "no_col": 1,
                "sticky": "news",
                "span_row": 1,
                "span_col": 1,
                "row_stretched": [0, 0, 1],
                "col_stretched": [0, 1],
                "padx": 4,
                "pady": 4
            },
# gui layer 2
            "execute ribben": {
                "master": "left",
                "no_row": 0,
                "no_col": 0,
                "sticky": "news",
                "span_row": 1,
                "span_col": 1,
                "row_stretched": [1, 1],
                "col_stretched": [0, 1, 1],
                "padx": 4,
                "pady": 0
            },
            "progress ribben": {
                "master": "left",
                "no_row": 1,
                "no_col": 0,
                "sticky": "news",
                "span_row": 1,
                "span_col": 1,
                "row_stretched": [0, 1],
                "col_stretched": [0, 1],
                "padx": 4,
                "pady": 2
            },
            "calendar container":{
                "master": "left",
                "no_row": 2,
                "no_col": 0,
                "sticky": "news",
                "span_row": 1,
                "span_col": 1,
                "row_stretched": [1],
                "col_stretched": [1],
                "padx": 4,
                "pady": 4
            },

            # "keyword editor": {
            #     "master": "right",
            #     "no_row": 0,
            #     "no_col": 0,
            #     "sticky": "news",
            #     "span_row": 1,
            #     "span_col": 1,
            #     "row_stretched": [0, 1],
            #     "col_stretched": [1],
            #     "padx": 0,
            #     "pady": 0
            # },
        }
        self.gui_containers = {}
        for name_gui, prop_gui in dict_layout.items():
            # list_usePane = ['main', 'body']
            # if name_gui in list_usePane

            master = self.root if prop_gui['master'] == "" else self.gui_containers[prop_gui['master']]

            self.gui_containers[name_gui] = tk.Frame(master, name = name_gui, padx = prop_gui['padx'], pady = prop_gui['pady'])

            self.gui_containers[name_gui].grid(
                row = prop_gui['no_row'],
                column = prop_gui['no_col'],
                sticky = prop_gui['sticky'],
                rowspan = prop_gui['span_row'],
                columnspan = prop_gui['span_col'])

            for idx_row, weight in enumerate(prop_gui['row_stretched']):
                self.gui_containers[name_gui].grid_rowconfigure(idx_row, weight = weight)

            for idx_col, weight in enumerate(prop_gui['col_stretched']):
                self.gui_containers[name_gui].grid_columnconfigure(idx_col, weight = weight)

    # def init_calendar()

    def init_images(self):

        self.images = {key: PhotoImage(file = value[0]).subsample(value[1]) for key, value in self.holder_resources.data['image paths'].items()}
        for key, value in self.holder_resources.data['image mapping'].items():
            self.images[key] = self.images[value]
        pass

    def pressed_del(self):
        idx_selectedKeyword = self.lbx_keywordEditor.curselection()
        self.lbx_keywordEditor.delete(idx_selectedKeyword)
        self.lbx_keywordEditor.select_set(idx_selectedKeyword)
        self.update_resources()
    
    def pressed_add(self):
        keyword_toAdd = self.vars['編輯關鍵字'].get()
        idx_selectedKeyword = self.lbx_keywordEditor.curselection()
        # if len(idx_selectedKeyword) == 0:
        #     idx_selectedKeyword = ('end')
        if keyword_toAdd in self.holder_resources.data['關鍵字']: return
        self.lbx_keywordEditor.insert('end', keyword_toAdd)
        self.lbx_keywordEditor.select_set('end')
        if len(idx_selectedKeyword) > 0:
            self.lbx_keywordEditor.select_clear(idx_selectedKeyword)
        self.update_resources()

    def update_resources(self):

        list_keywords = self.lbx_keywordEditor.get(0, 'end')
        self.holder_resources.data['關鍵字'] = list_keywords
        self.holder_resources.data['檔名'] = self.vars['檔名'].get()
        self.holder_resources.data['資料夾'] = self.vars['資料夾'].get()

        self.holder_resources.save_resource()



    def changed_date(self, e1, e2, e3):

        self.change_fileNameDate()
        self.change_fullFileName()

    def changed_fileName(self, e1, e2, e3):

        self.change_fullFileName()

    def changed_dirName(self, e1, e2, e3):

        self.change_fullFileName()

    def change_fileNameDate(self):
        tmp_list = self.vars['日期'].get().split('/')
        if len(tmp_list[1]) == 1:
            tmp_list[1] = '0' + tmp_list[1]
        if len(tmp_list[2]) == 1:
            tmp_list[2] = '0' + tmp_list[2]
        
        tmp_str = '_' + ''.join(tmp_list) + '.xlsx'

        self.vars['檔名日期'].set(tmp_str)

    def change_fullFileName(self):

        tmp_str = './' + self.vars['資料夾'].get() + '/' + self.vars['檔名'].get() + self.vars['檔名日期'].get()
        self.vars['全檔名'].set(tmp_str)
        # print(self.vars['全檔名'].get())


    def pressed_execute(self):

        self.update_resources()