import json
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def GetAllFund():
    '''
        功能：获取所有基金名称、代码、类型，天天基金数据接口：http://fund.eastmoney.com/js/fundcode_search.js
        传入：无
        返回：所有基金基础数据
    '''
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    list_ = eval(re.findall(r'\[.*\]', res.text)[0])
    df = pd.DataFrame(list_)
    df.columns = ['基金代码', '基金拼音简写', '基金名称', '基金类型', '基金拼音全称']

    return df


def GetAllFundCompany():
    '''
        功能：获取所有基金公司名称、代码，天天基金数据接口：http://fund.eastmoney.com/js/jjjz_gs.js
        传入：无
        返回：所有基金公司名称、代码
    '''
    url = "http://fund.eastmoney.com/js/jjjz_gs.js"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    list_ = eval(re.findall(r'\[.*\]', res.text)[0])
    df = pd.DataFrame(list_)
    df.columns = ['基金公司代码', '基金公司名称']

    return df


def GetFundInfoNow(FundCode):
    '''
        功能：获取基金实时信息，天天基金数据接口：http://fundgz.1234567.com.cn/js/基金代码.js
        传入：基金代码
        输出：基金实时信息 --> dict
                fundcode -- 基金代码
                name     -- 基金名称
                jzrqv    -- 上一交易日
                dwjz     -- 基金净值（截止上一交易日）
                gsz      -- 估算净值（实时）
                gszzl    -- 估算涨幅（实时）
                gztime   -- 更新时间（实时）
    '''
    url = "http://fundgz.1234567.com.cn/js/%s.js" % FundCode
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    js_data = json.loads(re.findall(r'jsonpgz\((.*)\)', res.text)[0])  # 正则匹配

    return js_data


def Get_html(fund_code, start_date, end_date, type_="lsjz", page=1, per=20):
    '''
        获取基金网页数据
    '''
    url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type={}&code={}&page={}&sdate={}&edate={}&per={}" \
        .format(type_, fund_code, page, start_date, end_date, per)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    }
    HTML = requests.get(url, headers=headers)
    HTML.encoding = "utf-8"

    return HTML


def Get_pages(HTML):
    '''
        获取最大页数
    '''
    pages = re.findall(r'pages:(.*),', HTML.text)[0]

    return int(pages)


def Get_FundData_history(HTML):
    '''
        通过html获取基金历史数据
    '''
    soup = BeautifulSoup(HTML.text, 'html.parser')
    trs = soup.find_all("tr")
    res = []
    for tr in trs[1:]:
        date = tr.find_all("td")[0].text  # 净值日期
        unit_net = tr.find_all("td")[1].text  # 单位净值
        acc_net = tr.find_all("td")[2].text  # 累计净值
        fund_r = tr.find_all("td")[3].text  # 日增长率
        buy_status = tr.find_all("td")[4].text  # 申购状态
        sell_status = tr.find_all("td")[5].text  # 赎回状态
        res.append([date, unit_net, acc_net, fund_r, buy_status, sell_status])
    df = pd.DataFrame(res, columns=['净值日期', '单位净值', '累计净值', '日增长率', '申购状态', '赎回状态'])

    return df


def Get_FundData_main(fund_code, start_date, end_date):
    '''
        获取基金数据主函数（仅支持单基金）
    '''
    html = Get_html(fund_code, start_date, end_date)
    pages = Get_pages(html)
    res_df = pd.DataFrame()
    for page in range(1, pages + 1):
        html = Get_html(fund_code, start_date, end_date, "lsjz", page)
        df_ = Get_FundData_history(html)
        res_df = pd.concat([res_df, df_])

    res_df.insert(0, "基金代码", fund_code)

    return res_df


if __name__ == "__main__":
    funds = GetAllFund()
    print(funds)
