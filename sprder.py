# 获取中国天气网 url:http://www.weather.com.cn/textFC/hb.shtml
import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

ALL_DATA = []


# 作用域解析页面
def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3554.0 Safari/537.36',
        'Referer': 'http://www.weather.com.cn/forecast/cma_forecast.shtml'
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text, 'html5lib')
    conMidtab = soup.find('div', class_='conMidtab')  # 获取到第一个div
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all("tr")[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]

            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city": city, "min_temp": int(min_temp)})


# 作用域url
def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        parse_page(url)

    # 分析数据 简单的可视化（根据最低气温进行排序）
    ALL_DATA.sort(key=lambda data: data['min_temp'])
    data = ALL_DATA[0:10]
    cities = list(map(lambda x: x['city'], data))
    temps = list(map(lambda x: x['min_temp'], data))
    chart = Bar("中国天气最低气温排行版")
    chart.add('', cities, temps)
    chart.render('temperature.html')


if __name__ == '__main__':
    main()
