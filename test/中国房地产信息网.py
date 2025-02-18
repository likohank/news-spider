#encoding=gb2312
import requests,re,bs4,time,sys,hashlib,uuid,time,json,base64,rsa,platform,datetime,os,urllib

UserAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
def get_time(format_date,time_pull = None):
    if time_pull:
        return int(time.mktime(time.strptime(time_pull, format_date))*1000)
def standard_work_list():
    return_data = []
    headers = {'User-Agent': UserAgent}
    res = requests.get('http://www.realestate.cei.gov.cn/file/index.aspx?type1=�г�&op=sc&b=1&k=1', headers=headers)
    res.raise_for_status()
    reg_content = res.content.decode('gb2312','ignore')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    infos = html_page.findAll('a',{'class':'lawbra'})
    for one_info in infos:
        _one_info = str(one_info)
        content_dir = one_info
        if content_dir:
            _datetime = 0
            _url_tmp = 'http://www.realestate.cei.gov.cn/file/'+content_dir['href'].strip()
            print({'url': _url_tmp, 'title': content_dir.text})
            return_data.append({'url': _url_tmp, 'title': content_dir.text, 'datetime': _datetime})
    return return_data


def standard_work_article(target_url):
    return_data = []
    headers = {'User-Agent': UserAgent}
    res = requests.get(target_url, headers=headers)
    res.raise_for_status()

    reg_content = res.content.decode('utf-8','ignore')
    charset = re.findall(r'meta http-equiv="Content-Type" content="text/html; charset=(.+?)"', reg_content)
    reg_content = res.content.decode(charset[0], 'ignore')
    html_page = bs4.BeautifulSoup(reg_content, 'lxml')
    try:
        infos = html_page.find(class_='xwzw').findAll('p')
    except:
        try:
            infos = html_page.find(class_='b').findAll('p')
        except:
            try:
                infos = html_page.find(class_='art_contextBox').findAll('p')
            except:
                try:
                    infos = html_page.find(class_='summary-text').findAll('p')
                except:
                    try:
                        infos = html_page.find(class_='TRS_Editor').findAll('p')
                    except:
                        try:
                            infos = html_page.find(class_='left_zw').findAll('p')
                        except:
                            infos = html_page.find(id='p-detail').findAll('p')



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
    if not return_data:
        return
    nian = urllib.parse.unquote_plus('%E5%B9%B4')
    yue = urllib.parse.unquote_plus('%E6%9C%88')
    ri = urllib.parse.unquote_plus('%E6%97%A5')
    date = re.search(r"(\d{4}%s\d{1,2}%s\d{1,2}%s\s\d{1,2}:\d{1,2})" % (nian, yue, ri), reg_content)
    if not date:
        date = re.search(r"(\d{4}%s\d{1,2}%s\d{1,2}%s)" % (nian, yue, ri), reg_content)
        if not date:
            date = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", reg_content)

            if not date:
                date = re.search(r"(\d{4}/\d{1,2}/\d{1,2}\s\d{1,2}:\d{1,2})", reg_content)

                if not date:
                    date = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", reg_content)
                    if not date:
                        date = re.search(r"(\d{4}/\d{1,2}/\d{1,2})", reg_content)
    datetime_dir = re.match( '(?P<year>\d{4})%s(?P<month>\d+?)%s(?P<day>\d+?)%s (?P<hour>\d+?):(?P<minute>\d+)' % (nian, yue, ri), date[0])
    if not datetime_dir:
            datetime_dir = re.match('(?P<year>\d{4})%s(?P<month>\d+?)%s(?P<day>\d+?)%s' % (nian, yue, ri), date[0])
            if not datetime_dir:
                datetime_dir = re.match('(?P<year>\d{4})-(?P<month>\d+?)-(?P<day>\d+?) (?P<hour>\d+?):(?P<minute>\d+)', date[0])
                if not datetime_dir:
                    datetime_dir = re.match('(?P<year>\d{4})/(?P<month>\d+?)/(?P<day>\d+?) (?P<hour>\d+?):(?P<minute>\d+)',date[0])
                    if not datetime_dir:
                        datetime_dir = re.match('(?P<year>\d{4})-(?P<month>\d+?)-(?P<day>\d+)',date[0])
                        if not datetime_dir:
                            datetime_dir = re.match( '(?P<year>\d{4})/(?P<month>\d+?)/(?P<day>\d+)', date[0])

    try:
        tt_tmp = '%s-%s-%s %s:%s' % (datetime_dir['year'], datetime_dir['month'], datetime_dir['day'], datetime_dir['hour'], datetime_dir['minute'])
        _datetime = 0
        if datetime_dir:
            _datetime = get_time('%Y-%m-%d %H:%M', tt_tmp)
    except:
        tt_tmp = '%s-%s-%s' % (
            datetime_dir['year'], datetime_dir['month'], datetime_dir['day'])
        _datetime = 0
        if datetime_dir:
            _datetime = get_time('%Y-%m-%d', tt_tmp)
    _title = html_page.find('title').text
    _title = _title.replace('\r','').replace('\n','').replace('\t','')
    return _datetime, '%s<replace title>%s' % (_title, '\n'.join(return_data))

def main():
   list = standard_work_list()
   for url in list:
       print(standard_work_article(url['url']))



if __name__ == '__main__':
    main()
