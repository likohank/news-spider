#encoding=utf-8
import requests,re,bs4,time,sys,hashlib,uuid,time,json,base64,rsa,platform,datetime,os,urllib

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
def get_time(format_date,time_pull = None):
    if time_pull:
        return int(time.mktime(time.strptime(time_pull, format_date))*1000)
def standard_work_list():
    return_data = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'cookie': 'maxPageNum5097045=258; __jsluid=328605e1a60939bf562083db25a6a7a2; __jsl_clearance=1560149586.607|0|GDFAZGO5qh9urcx%2FFHw31gcRSoo%3D; zh_choose=n',
               'Referer': 'http://www.mps.gov.cn/'
               }
    res = requests.get('http://www.mps.gov.cn/n2253534/n2253535/index.html', headers=headers)
    res.raise_for_status()
    reg_content = res.content.decode('utf-8')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    infos = html_page.select('span#comp_5097045 dl dd a')
    for one_info in infos:
        _one_info = str(one_info)
        content_dir = one_info
        if content_dir:
            _datetime = 0
            _url_tmp = content_dir['href'].strip()
            _url_tmp=_url_tmp.replace('../../','http://www.mps.gov.cn/')
            print({'url': _url_tmp, 'title': content_dir.text.strip()})
            return_data.append({'url': _url_tmp, 'title': content_dir.text.strip(), 'datetime': _datetime})
    return return_data


def standard_work_article(target_url):
    return_data = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'cookie': 'maxPageNum5097045=258; __jsluid=328605e1a60939bf562083db25a6a7a2; __jsl_clearance=1560149586.607|0|GDFAZGO5qh9urcx%2FFHw31gcRSoo%3D; zh_choose=n',
               'Referer': 'http://www.mps.gov.cn/n2253534/n2253535/index.html',
               # 'If-None-Match':'W/"10000000663bc-44bc-58ad92cff04c0"',
               }
    res = requests.get(target_url, headers=headers)
    time.sleep(1)
    res.raise_for_status()
    reg_content = res.content.decode('utf-8')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    infos = html_page.find(class_='arcContent center').findAll('p')
    for one_info in infos:
        content_dir = re.search('<p[\\s\\S]+/p>', str(one_info))
        if content_dir:
            need_content = one_info.text
        else:
            if isinstance(one_info, bs4.NavigableString):
                need_content = one_info
            else:
                continue
        if not need_content.strip():
            continue
        return_data.append(need_content.strip())
        nian = urllib.parse.unquote_plus('%E5%B9%B4')
    yue = urllib.parse.unquote_plus('%E6%9C%88')
    ri = urllib.parse.unquote_plus('%E6%97%A5')

    date = re.search(r"(\d{4}%s\d{1,2}%s\d{1,2}%s)"%(nian, yue, ri), reg_content)

    datetime_dir = re.match('(?P<year>\d{4})%s(?P<month>\d+?)%s(?P<day>\d+?)%s' % (nian, yue, ri), date[0])

    tt_tmp = '%s-%s-%s' % (
        datetime_dir['year'], datetime_dir['month'], datetime_dir['day'])
    _datetime = 0
    if datetime_dir:
        _datetime = get_time('%Y-%m-%d', tt_tmp)
    _title = html_page.find('title').text
    return _datetime, '%s<replace title>%s' % (_title, '\n'.join(return_data))

def main():
   list = standard_work_list()
   for url in list:
       print(standard_work_article(url['url']))



if __name__ == '__main__':
    main()
