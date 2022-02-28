"""
@Description: 解析www.tikstar.com网站相关内容，获取tags
@Date       :2021/12/22
@Author     :xhunmon
@Mail       :xhunmon@gmail.com
"""
from bs4 import BeautifulSoup
import file_util as futil


def parse_tags(page):
    '''解析页面，返回标题和文章页面内容，如果生成文章则还需要组装'''
    soup = BeautifulSoup(page, 'html.parser')
    trs = soup.find('tbody').find_all('tr')
    result = []
    for tr in trs:
        tds = tr.find_all('td')
        tag_name = tds[0].find('h3').text.replace('\n', '').replace(' ', '')
        video_num = tds[1].text.replace('\n', '').replace(' ', '')
        views = tds[2].text.replace('\n', '').replace(' ', '')
        result.append('标签：{} 视频数：{} 观看数：{}'.format(tag_name, video_num, views))
    return result


if __name__ == '__main__':
    html = futil.read('source/tags.html')
    result = parse_tags(html)
    print(result)
    futil.write_json(result, 'source/handmade.json')
