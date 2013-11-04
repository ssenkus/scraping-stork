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

    categories.append(href)
    resp = br.open(url + href)
    
    soup = BeautifulSoup(resp)
    breadcrumbContainer = soup.find(id="c4-breadcrumbs-id10T")
    products = soup.find(id="wrapper")
    prods = soup.find(id="contents-table")
    
    print "\n\n"
    print text + " -> " + href + "\n"
    print "\n\nBREADCRUMB CONTAINER\n\n"
    print breadcrumbContainer    
    print "\n\nWRAPPER\n\n"
    print products
    print "\n\nCONTENT-TABLE\n\n"
    print prods
    print "\n\n###################################################\n\n"
    f.write(text + " -> " + href + "\n")
    f.write("\n\nBREADCRUMB CONTAINER\n\n")
    f.write(str(breadcrumbContainer))
    f.write("\n\nWRAPPER\n\n")
    f.write(str(products))
    f.write("\n\nCONTENT-TABLE\n\n")
    f.write(str(prods))
    f.write("\n\n###################################################\n\n")
    
raw_input("\n\nPress Enter to continue...\n\n")

f.close()
