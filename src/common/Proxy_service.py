from fake_useragent import UserAgent
from urllib.request import Request, urlopen
import random
from bs4 import BeautifulSoup


ua = UserAgent() # From here we generate a random user agent
proxies = []

# Retrieve latest proxies
proxies_req = Request('https://www.sslproxies.org/')
proxies_req.add_header('User-Agent', ua.random)
proxies_doc = urlopen(proxies_req).read().decode('utf8')
# print(proxies_doc)


soup = BeautifulSoup(proxies_doc, 'html.parser')
proxies_table = soup.find(id='proxylisttable')

# Save proxies in the array
for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
        'ip':   row.find_all('td')[0].string,
        'port': row.find_all('td')[1].string
    })

#print(len(proxies))
def random_proxy():

    proxy_index = random.randint(0, len(proxies) - 1)
    proxy = proxies[proxy_index]
    proxy_text = proxy['ip'] + ':' + proxy['port']
    proxy_text = 'http://' + str(proxy_text)
    proxy = {'http': proxy_text}
    return proxy

def del_proxy(proxy):
    proxies.pop(proxies.index(proxy))














