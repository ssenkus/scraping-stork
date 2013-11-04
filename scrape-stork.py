import os
import mechanize
from bs4 import BeautifulSoup

os.system('cls')

f = open("datafile.txt", "w")

br = mechanize.Browser();
url = "http://www.storkbabygiftbaskets.com/"
response = br.open(url)
soup = BeautifulSoup(response)

catLinks = soup.find(id="left-navigation").find_all('a')
categories = [];
print "Featured Gift Links:\n\n"
for link in catLinks:
    href = link.get('href')
    text = link.string
    print text + " -> " + href + "\n"
    categories.append(href)
    resp = br.open(url + href)
    soup = BeautifulSoup(resp)
    breadcrumbContainer = soup.find(id="c4-breadcrumbs-id10T")
    print breadcrumbContainer.b.prettify()
    f.write(text + " -> " + href + "\n")
    f.write(str(breadcrumbContainer) + "\n\n")
    
    
raw_input("\n\nPress Enter to continue...\n\n")
f.close();
