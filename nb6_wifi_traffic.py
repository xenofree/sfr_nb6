import re
import hashlib
import hmac
import base64
import sys

try:
    import requests
except:
    print('Merci d\'installer le module \'requests\' "pip install requests"')
    sys.exit(1)
try:
    from bs4 import BeautifulSoup
except:
    print('Merci d\'installer le module \'BeautifulSoup\' "pip install BeautifulSoup4"')
    sys.exit(1)


IP_NB6 = '192.168.1.1'
USER_NB6 = 'admin'
MDP_NB6 = 'XXXXXXXXXXXXXXX'
VALUE_WANTED = ['txbyte', 'rxbyte'] #Value a extraire de la page

headers = {'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
params = {'action': 'challenge'}

s = requests.Session()
result = s.get(f'http://{IP_NB6}/login', headers=headers, params=params, timeout=10)
try:
    challenge = re.search('<challenge>(.+?)</challenge>', result.text).group(1) #On recupere le challenge
except AttributeError:
    sys.exit(1)

user_nb6_sha256 = hashlib.sha256(USER_NB6.encode()).hexdigest() #On hash le user en sha256
mdp_nb6_sha256 = hashlib.sha256(MDP_NB6.encode()).hexdigest() #On hash le mdp en sha256

user_nb6_digest = hmac.new(challenge.encode(), msg=user_nb6_sha256.encode(), digestmod=hashlib.sha256).hexdigest() #On calcul le hmac du user via le challenge
mdp_nb6_digest = hmac.new(challenge.encode(), msg=mdp_nb6_sha256.encode(), digestmod=hashlib.sha256).hexdigest() #On calcul le hmac du mdp via le challenge

digest = user_nb6_digest + mdp_nb6_digest #On concatene les deux

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
params = {'method': 'passwd', 'page_ref': '', 'zsid': challenge, 'hash': digest, 'login': '', 'password': ''}
s.post(f'http://{IP_NB6}/login', headers=headers, params=params, timeout=10) #On se log
result = s.get(f'http://{IP_NB6}/state/wifi', timeout=10) #On recupere la page de stats

soup = BeautifulSoup(result.text, 'html.parser')
for pre in soup.findAll('pre'): #On cherche toutes les balises <pre>
    pre = str(pre)
    for value in VALUE_WANTED: #Pour toutes les value voulu
        try:
            result = re.search(f'{value} = (.+)', pre).group(1) #On extrait la stat
        except AttributeError:
            sys.exit(1)
        print(f'{value}:{result}', end=' ')
