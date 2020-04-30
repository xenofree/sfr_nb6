import requests
import re

SFR_NB6_IP   = '192.168.1.1'
VALUE_WANTED = ['rate_down', 'rate_up', 'crc']

result = requests.get(f'http://{SFR_NB6_IP}/api/1.0/?method=dsl.getInfo')

for value in VALUE_WANTED:
    re_find = re.search(f'{value}="(.+?)"', result.text).group(1)
    print(f'{value}:{re_find}', end=' ')
