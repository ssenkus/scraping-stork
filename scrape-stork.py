import os
from mechanize import Browser
from bs4 import BeautifulSoup

os.system('cls')

# Open file to dump page data into
#f = open("datafile.txt", "w")


script_dir = os.getcwd()
print script_dir


##############################################################

class Page:

    soup = ''
    def __init__(self, name, url, browser):
        self.url = url
        self.name = name
        self.browser = browser
        self.getName()

    def getName(self):
        print self.name

    def getHtml(self):
        response = self.browser.open(self.url)
        self.soup = BeautifulSoup(response)
        return self.soup

    def getBreadcrumbContainer(self):
        return 'asdaf'

##############################################################

class IndexPage(Page):

    def getLeftNavLinks(self):
        catLinks = self.soup.find(id="left-navigation").find_all('a')
        cat = {}
        for link in catLinks:        
            
            cat[link.string] = link.get('href')
#            text = link.string
            newPage = Page(link.string,link.get('href'), br);
        return cat

##############################################################


# Get root page
br = Browser();
baseUrl = "http://www.storkbabygiftbaskets.com/"
homepage = IndexPage('Home', baseUrl, br)
homepage.getHtml()
print homepage.getLeftNavLinks()

'''
for link in catLinks:
    # get category links

    resp = br.open(url + href)
    #  Now parse through each category page     
    soup = BeautifulSoup(resp)
    # The main container
    breadcrumbContainer = soup.find(id="c4-breadcrumbs-id10T")
    # Found on product pages
    products = soup.find(id="wrapper")
    contentsTable = soup.find(id="contents-table")

    print text + " -> " + href + "\n"
    print "\n\n\tBREADCRUMB CONTAINER\n\n"
    count = 0

    # Search through container div
    for node in breadcrumbContainer:
        print node
        count += 1
        print "Breadcrumb Trail {0}".format(count)
        # get all anchor tags
        try: 
            links = node.findAll('a')
            for link in links:
                print link.get('href')
            print str("".join(node.findAll(text=True)))
        except:
            pass
        print "\n"
    print "------------------------------------------------"

    print "\n\n\tWRAPPER\n\n"
    
    try:
        for node in products:
            links = node.findAll('a')
            for link in links:
                print link.get("href")
    except: 
        pass
    print "\n\n\tCONTENT-TABLE\n\n"
    try:
        for node in contentsTable:
            links = contentsTable.findAll('a')
            for link in links:
                print link.get('href')
    except:
        pass    
    print "\n\n###################################################\n\n"
'''
'''    
    f.write(text + " -> " + href + "\n")
    f.write("\n\nBREADCRUMB CONTAINER\n\n")
    f.write(str(breadcrumbContainer))
    f.write("\n\nWRAPPER\n\n")
    f.write(str(products))
    f.write("\n\nCONTENT-TABLE\n\n")
    f.write(str(contentsTable))
    f.write("\n\n###################################################\n\n")
''' 
raw_input("\n\nPress Enter to continue...\n\n")

# f.close()