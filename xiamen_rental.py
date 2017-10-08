import requests
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient('localhost',27017)
rental = client['rental']
table = rental['table']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                        '(KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36'}

def get_page(url):
    try:
        r = requests.get(url,headers=headers)
        r.raise_for_status()
        return r.text
    except:
        return "爬取失败"

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    images = soup.select('div.img_list > a > img')
    titles = soup.select('div.des > h2 > a')
    layouts = soup.select('div.des > p.room')
    prices = soup.select('div.money > b')
    positions = soup.select('div.des > p.add > a')
    sources = soup.select('div.des > div')
    for image,title,layout,price,position,source in zip(images,titles,layouts,prices,positions,sources):
        data = {
            'image': image.get('src'), #获得属性
            'title': title.get_text().strip(),
            'layout': layout.get_text().replace('\n','').replace(' ','').replace('\r','').strip(),
            'price': price.get_text(),
            'position': position.get_text(),
            'source':source.get_text().replace('\n','').replace(' ','').replace('\r','').strip()
        }
        print(data)
        table.insert_one(data)

def main():
    url = "http://xm.58.com/chuzu/pn"
    for i in range(1,70):
        url += str(i)
        html = get_page(url)
        parse_page(html)

if __name__=='__main__':
    main()