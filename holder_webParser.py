import requests
from lxml import etree


class Holder_webParser():

    def __init__(self) -> None:
        
        self.parser = etree.HTML

        pass

    def get_dataDictOfDate(self, date, var_state):

        var_state.set('資料擷取中...')
        cnt_raw = self.get_rawContentOfDate(date, var_state)
        if cnt_raw == '': return None
        cnt_gpa = self.get_rawContentOfDate(date, var_state, 'gpa')
        cnt_anztec = self.get_rawContentOfDate(date, var_state, 'anztec')
        cnt_astep = self.get_rawContentOfDate(date, var_state, 'astep')

        list_result = self.parse_rawToList(cnt_raw)
        list_isgpa = self.parse_rawToIsAgreement(cnt_gpa)
        list_isanztec = self.parse_rawToIsAgreement(cnt_anztec)
        list_isastep = self.parse_rawToIsAgreement(cnt_astep)

        dict_result = {}
        
        for row in list_result:
            var_state.set(f'解析案號[{row[0]}]資料')
            dict_result[row[0]] = row
            # with open('tmp_parsedResult2.json', 'w', encoding = 'utf-8') as f:
            #     json.dump(dict_result, f, ensure_ascii = False, indent = 2)

        for idt_isgpa in list_isgpa:
            var_state.set(f'案號[{idt_isgpa}]適用GPA協定')
            dict_result[idt_isgpa][6] = 'Yes'

        for idt_isanztec in list_isanztec:
            var_state.set(f'案號[{idt_isanztec}]適用ANZTEC協定')
            dict_result[idt_isanztec][7] = 'Yes'

        for idt_isastep in list_isastep:
            var_state.set(f'案號[{idt_isastep}]適用ASTEP協定')
            dict_result[idt_isastep][8] = 'Yes'

        # print(htmlObj_dateResult)

        # with open('tmp_parsedResult3.json', 'w', encoding = 'utf-8') as f:
        #     json.dump(dict_result, f, ensure_ascii = False, indent = 2)

        return dict_result

    def parse_rawToIsAgreement(self, cnt_isagreement):
        htmlObj = self.parser(cnt_isagreement)[0]
        result = []

        for row in htmlObj:
            item = self.get_cleanTxt(row[0].text)
            result.append(item)
            #idt = self.get_cleanTxt(row[2].text)
            #result.append(idt)
        return result

        pass

    def parse_rawToList(self, cnt_raw):

        htmlObj_dateResult = self.parser(cnt_raw)[0]
        result = []

        for row in htmlObj_dateResult:
            item = self.get_cleanTxt(row[0].text)
            idt = self.get_cleanTxt(row[2].text)
            org = self.get_cleanTxt(row[1].text)
            url = self.form_itemUrl(self.get_surlFromRow(row))
            date_online = self.get_cleanTxt(row[6].text)
            date_deadline = self.get_cleanTxt(row[7].text)
            budget = self.get_cleanTxt(row[8][0].text)
            title = self.get_itemTitle(row)
            result.append([item, idt, title, org, date_online, date_deadline, 'No', 'No', 'No', budget, url])

        return result

    def get_itemTitle(self, row):
        idx_br = 0 if row[2][0].tag == 'br' else 1
        return self.get_textBetween(row[2][idx_br + 1][0][0][0].text, '("', '")')

    def get_rawContentOfDate(self, date, var_state, agreement = ''):
        idx_pageStart = 1
        idx_page = idx_pageStart
        has_next = True
        cnt_raw = ''

        for idx_page in range(idx_pageStart, 5):
            var_state.set(f'嘗試擷取{agreement}第[{idx_page}]頁')
            ret = requests.get(self.form_searchUrl(date, date, idx_page, agreement))
            try:
                tmp_cnt = str(ret.content, encoding = 'utf-8').split('<tbody>')[2].split('</tbody>')[0]
            except:
                tmp_cnt = None
                break
            # print(self.parser(tmp_cnt)[0][0][0].text)
            # print(idx_page)
            if self.parser(tmp_cnt)[0][0][0].text == '無符合條件資料': break
            
            cnt_raw += tmp_cnt
        
        # print(cnt_raw)
        
        return cnt_raw

    def get_cleanTxt(self, txt_dirty):
        return txt_dirty.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')

    def get_surlFromRow(self, row):
        return row[3][0].values()[0].split('=')[1]

    def get_textBetween(self, txt_raw, lbl_start, lbl_end):
        return txt_raw.split(lbl_start)[1].split(lbl_end)[0]

    def form_searchUrl(self, date_start, date_end, page, agreement = None):
        
        state_agreements = {
            'gpa' : 'false',
            'anztec' : 'false',
            'astep' : 'false'
        }

        if not( agreement == '' ):
            state_agreements[agreement] = 'true'

        return f'https://web.pcc.gov.tw/prkms/tender/common/basic/readTenderBasic?pageSize=50&tenderEndDate={date_end}&orgName=&tenderName=&searchType=basic&d-49738-p={page}&firstSearch=false&pageSize=50&radProctrgCate=RAD_PROCTRG_CATE_3&tenderId=&orgId=&tenderStartDate={date_start}&tenderType=TENDER_DECLARATION&dateType=isDate&tenderWay=TENDER_WAY_4&level_1=on&gpa={state_agreements["gpa"]}&anztec={state_agreements["anztec"]}&astep={state_agreements["astep"]}'

    def form_itemUrl(self, surl_item):
        return f'https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain={surl_item}='

# page = 1
# date = '2022/10/6'

# holder_webParser = Holder_webParser()

# holder_webParser.get_dataListOfDate(date)