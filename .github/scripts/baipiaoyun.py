import requests, os

email = os.environ["EMAIL"]
passwd = os.environ["PASSWD"]
code = os.environ["CODE"]

request = requests.Session()


def ajax(url, method='GET', headers=None, data=None, proxies=None):
    # proxy = {
    #     "http": "http://127.0.0.1:7890",
    #     "https": "http://127.0.0.1:7890",
    # }
    # if proxies is None:
    #     proxies = proxy
    if method == 'GET':
        return request.get(url, params=data, headers=headers, proxies=proxies)
    else:
        return request.post(url, data=data, headers=headers, proxies=proxies)


headers = {
    'Referer': 'https://baipiaoyun.xyz/auth/login',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.8.9980.88 Safari/537.36'
}

data = {
    'email': email if email is not None else '',
    'passwd': passwd if passwd is not None else '',
    'code': code if code is not None else ''
}

res = ajax('https://baipiaoyun.xyz/auth/login', method='POST', data=data, headers=headers)
print(res.json())

res = ajax('https://baipiaoyun.xyz/user')
print(f'状态码:{res.status_code}')

res = ajax('https://baipiaoyun.xyz/user/checkin', method='POST')
print(res.json())
