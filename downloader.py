import sys
import requests
from bs4 import BeautifulSoup
import os
import fire

"""
枚数の計算処理がおぞくなっているが大方OK
"""

class Downloader:
    def __init__(self,keyword ,cnt):
        self.dirname = keyword 
        self.keyword = keyword
        self.cnt = cnt
        if os.path.exists(keyword):
            pass
            print("Specified Directory ")
        else:
            print("Create new file")
            os.mkdir(keyword)

    def download(self, url, filepath):
        binary = requests.get(url, stream=True)
        if binary.status_code == 200:
            with open(filepath,"wb") as f:
                f.write(binary.content)
                print(url,"\n {} download completed".format(filepath))
        else:
            print(url, "\n {} donwload failed".format(filepath))

    def get_urls(self, keyword, cnt):
        if keyword == "":
            print("No keyword specified")
            sys.exit(1)
        if cnt > 60:
            pages = int(cnt/60) + 1
            last_page_cnt = cnt - 60*pages
        else:
            pages = 1
            last_page_cnt = cnt
        # http requests
        img_urls = []
        for page in range(pages):
            if page == pages - 1: # in the last page
                url = "https://search.yahoo.co.jp/image/search?p={}&n={}&b=11".format(keyword, last_page_cnt, page)
            else:
                url = "https://search.yahoo.co.jp/image/search?p={}&n={}&b=11".format(keyword, cnt, page)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, features="html.parser")
            img_tags = soup.find_all("img")
            img_urls_tmp = [e.get("src") for e in img_tags]
            for url_tmp in img_urls_tmp:
                img_urls.append(url_tmp)
        return img_urls

    def main(self):
        urls = self.get_urls(self.keyword, self.cnt)
        filenum = 0
        for url in urls:
            filename = self.dirname + "/" + str(filenum) + ".jpg"
            self.download(url, filename)
            filenum += 1

def driver(keyword, cnt):
    downloader = Downloader(keyword, cnt)
    downloader.main()


if __name__ == "__main__":
    fire.Fire(driver)
