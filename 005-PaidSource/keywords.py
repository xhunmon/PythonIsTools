import json
import random
import re
import time
from urllib.parse import quote_plus

from v2ray_pool import Net

import chardet
import requests
import urllib3
from bs4 import BeautifulSoup
from my_fake_useragent import UserAgent


class Keywords(Net):
    '''url：https://www.5118.com/ciku/index#129'''

    def get_keys_by_net(self) -> []:
        try:
            r = self.request(r'https://www.5118.com/ciku/index#129')
            if r.status_code != 200:
                return None
            r.encoding = r.apparent_encoding
            # <span>法律</span><br>
            soup = BeautifulSoup(r.text, "html.parser")
            results = []
            for a in soup.find_all(name='a'):
                results += re.findall(r'<span>(.*?)</span><br', str(a.get_text), re.DOTALL)
            return results
        except Exception as e:
            print(e)
            return None

    def get_keys_by_local(self) -> []:
        with open('test/key_tag.json', 'r') as f:
            js_get = json.load(f)
            f.close()
        return js_get

    def get_titles_by_local(self) -> []:
        with open('test/key_title.json', 'r') as f:
            js_get = json.load(f)
            f.close()
        return js_get

    def get_titles_by_net(self, key):
        '''通过网盘搜索检查出
        https://www.alipanso.com/search.html?page=1&keyword=%E7%90%86%E8%B4%A2&search_folder_or_file=2&is_search_folder_content=1&is_search_path_title=1&category=doc&file_extension=doc&search_model=1
        '''
        results = []
        try:
            time.sleep(random.randint(1, 4))
            r = self.request_en(
                r'https://www.alipanso.com/search.html?page=1&keyword=%s&search_folder_or_file=2&is_search_folder_content=1&is_search_path_title=1&category=doc&file_extension=doc&search_model=1' % key)
            if r.status_code != 200:
                print(r.status_code)
                return None
            r.encoding = r.apparent_encoding
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all(name='a'):
                ts = re.findall(r'(.*?).doc', str(a.get_text()).replace('\n', ''), re.DOTALL)
                for t in ts:
                    if '公众号' in t or '【' in t or '[' in t or ',' in t or '，' in t or ')' in t or '）' in t or t in results:
                        continue
                    if len(t) < 4:
                        continue
                    results.append(t)
            return results
        except Exception as e:
            print(e)
            return None


def test():
    js = ['a', 'b', 'c']
    with open('test/key_tag.json', 'w') as f:
        json.dump(js, f)
        f.close()
    with open('test/key_tag.json', 'r') as f:
        js_get = json.load(f)
        f.close()
    print(js_get)


if __name__ == "__main__":
    # test()
    keys = Keywords().get_keys_by_net()
    print(keys)
    with open('test/key_tag.json', 'w') as f:
        json.dump(keys, f, ensure_ascii=False)
        f.close()
