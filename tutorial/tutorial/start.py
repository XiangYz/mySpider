from bs4 import BeautifulSoup

import urllib
import re

'''
web = urllib.urlopen("http://freebuf.com/")
soup = BeautifulSoup(web.read())
tags_a = soup.findAll(name="a",attrs={'href':re.compile("^https?://")})

for tag_a in tags_a:
    printtag_a["href"]
'''