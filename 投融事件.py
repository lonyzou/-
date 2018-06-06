import requests
import json
import pandas as pd
import xlwt


class juzi():
    def __init__(self):
        self.url = "http://radar.itjuzi.com/investevent/info?location=in&orderby=def&page={}&scope=1"
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'http://radar.itjuzi.com/investevent',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            "Cookie": "gr_user_id=ccd197be-56e2-4fec-9e91-bbab2c03aece; _ga=GA1.2.161685632.1528190578; _gid=GA1.2.646378601.1528190578; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1528190578; gr_session_id_eee5a46c52000d401f969f4535bdaa78=4732957e-9f13-4262-9be9-d7b2d0b36e98_true; session=49cef7c742e34b3e68cd722b540413b743afaee2; acw_tc=AQAAAIS6Uwl2PwgARrnBc/P++Hh5ZFFH; identity=chao.zheng%40welian.com; remember_code=r8zNkkHhKn; unique_token=572792; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1528191529; user-radar.itjuzi.com=%7B%22n%22%3A%22zccccccc%22%2C%22v%22%3A2%7D; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1528191557; MEIQIA_EXTRA_TRACK_ID=15ao2BuhB1oSRjqcmx9OPyi3Sg2; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1528192301"
        }

    def get_url_list(self):
        url_list = [self.url.format(i) for i in range(1, 116)]
        for url in url_list:
            self._parse_url(url)

    def _parse_url(self, url):
        response = requests.get(url, timeout=10, headers=self.headers)
        assert response.status_code == 200
        data = json.loads(response.text)['data']
        aaa = []
        for i in range(0, len(data["rows"])):
            comment = []
            date = data['rows'][i]['date']
            com_name = data['rows'][i]['com_name']
            round = data['rows'][i]['round']
            money = data['rows'][i]['money']
            invsest_with = self.inspect(data['rows'][i]['invsest_with'])
            comment.extend([date, com_name, round, money, invsest_with])
            aaa.append(comment)
        print(aaa)
        name = ["", "", "", "", ""]
        bbb = pd.DataFrame(columns=name, data=aaa)

        bbb.to_csv("jiaoyu.csv", mode="a")
        #bbb.to_csv("jiaoyu.csv", mode="a",index=False, encoding="utf_8_sig")
        #bbb.to_excel("aa.xls",index=False, encoding="utf-8")

    def inspect(self, data):
        if type(data) == dict:
            result = [[n for n in d.values() if not n.startswith('http')] for d in data.values()]
            return result
        else:
            return [value['invst_name'] for value in data]


if __name__ == "__main__":
    comment = juzi()
    comment.get_url_list()
