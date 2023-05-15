import xlwings as xw


class Holder_workbook():

    def __init__(self) -> None:
        # self.wb = xw.Book()
        'yo'

    def link_toNewBook(self):
        self.wb = xw.Book()
    
    def save_book(self, path):
        try:
            self.wb.save(path)
        except(Exception) as e:
            print(e)

    def load_dictFromParsed(self, name_sheet, dict_parsed, font_title, font_content, var_state):
        # try:
        #     ws = self.wb.sheets['sheet1']
        # except:
        #     ws = self.wb.sheets['工作表1']
        self.wb.sheets.add(name_sheet)
        ws = self.wb.sheets[name_sheet]
        list_columnWidth = [5, 20, 80, 40, 8, 8, 8, 8, 8, 12, 8]
        for idx_col in range(1, 12):
            ws.range(1, idx_col).column_width = list_columnWidth[idx_col-1]
        ws.range(1, 1).value = ['項次', '標案案號', '標案名稱', '機關名稱', '公告日期', '截止日期', 'GPA', 'ANZTEC', 'ASTEP', '預算金額', '連結']
        ws.range((1, 1), (1, 11)).font.name = font_title['name']
        #ws.range((1, 1), (1, 10)).font.size = font_title['size']
        ws.range((1, 1), (1, 11)).font.size = 12
        ws.range((1, 1), (1, 11)).font.bold = font_title['bold']
        ws.range((1, 1), (1, 11)).font.italic = font_title['italic']

        for idx_row, (k, v) in enumerate(dict_parsed.items(), 2):
            var_state.set(f'項次[{v[0]}]寫入工作表')
            v1 = [ vi for vi in v]
            hyperLink = v[10]
            v1[1] = "'" + v1[1]
            ws.range(idx_row, 1).value = v1
            ws.range(idx_row, 11).add_hyperlink(hyperLink, "連結")
            # ws.range((idx_row, 1), (idx_row, 10)).font.name = '微軟正黑體'
            ws.range((idx_row, 1), (idx_row, 11)).font.name = font_content['name']
            #ws.range((idx_row, 1), (idx_row, 10)).font.size = font_content['size']
            ws.range((idx_row, 1), (idx_row, 11)).font.size = 12
            ws.range((idx_row, 1), (idx_row, 11)).font.bold = font_content['bold']
            ws.range((idx_row, 1), (idx_row, 11)).font.italic = font_content['italic']

