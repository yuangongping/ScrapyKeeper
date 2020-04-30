from scrapyd_api import ScrapydAPI
scrapyd = ScrapydAPI('http://localhost:6800')
ss = scrapyd.delete_project("nadsadsadasd")
print(ss)