import requests
from bs4 import BeautifulSoup


def grabUrl(idx):
    url = 'https://findlifee.com/category-3_%d.html' % idx
    res = requests.get(url)
    res.raise_for_status()
    soupUrl = BeautifulSoup(res.text, 'lxml')
    for fr in soupUrl.find(class_='list').find_all(class_='fr'):
        urlList.append(fr.next_sibling.get('href'))


if __name__ == '__main__':
    urlList = []
    for i in range(1, 35):
        grabUrl(i)
    print(urlList)
    with open('UrlCollection.txt', 'w') as f:
        f.write('\n'.join(urlList))
