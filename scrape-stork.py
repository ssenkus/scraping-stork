import os
import mechanize
from bs4 import BeautifulSoup

os.system('cls')
br = mechanize.Browser();
url = "http://www.storkbabygiftbaskets.com/"
response = br.open(url)
soup = BeautifulSoup(response)

catLinks = soup.find(id="left-navigation").find_all('a')
categories = [];
print "Featured Gift Links:\n\n"
for link in catLinks:
    href = link.get('href')
    print href
    categories.append(href)


raw_input("\n\nPress Enter to continue...\n\n")
