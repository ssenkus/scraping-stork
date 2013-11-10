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
        self.getHtml()

    def getName(self):
        print "\n\n###################################"
        print "Page Name:{0}\t\n".format(self.name)

    def getHtml(self):
        response = self.browser.open(self.url)
        self.soup = BeautifulSoup(response)
        return self.soup


##############################################################

class IndexPage(Page):

    def getLeftNavLinks(self):
        catLinks = self.soup.find(id="left-navigation").find_all('a')
        cat = {}
        for link in catLinks:        
            cat[link.string] = link.get('href')
            newPage = CategoryPage(link.string,link.get('href'), self.browser);
        return cat

##############################################################

class CategoryPage(Page):

    def __init__(self, name, url, browser):
        Page.__init__(self, name, url, browser)
        self.getBreadcrumbContainer()
        self.wrapper = self.testFor('wrapper')
        self.contentsTable = self.testFor('contents-table')

    def getBreadcrumbContainer(self):
        container = self.soup.find(id="c4-breadcrumbs-id10T")
        count = 0
        for node in container:
            count += 1
            bcText = ''
            hrefs = ''
            # get all anchor tags
            try: 
                links = node.findAll('a')
                for link in links:
                    hrefs += link.get('href')
                bcText = str("".join(node.findAll(text=True)))
            except:
                pass
            print "\tBreadcrumb Trail #{0}\n".format(count)
            print "\t-------------------"
            print "{0}".format(bcText)
            print "{0}".format(hrefs)

    def testFor(self, elemId):
        result = self.soup.find(id=elemId)
        hrefs = ''
        try:
            for node in result:
                links = node.findAll('a')
                for link in links:
                    hrefs += "\t" + link.get("href") + "\n"
        except: 
            pass

        print "\n#{0}\n{1}".format(elemId, hrefs)
        return result
       
##############################################################

br = Browser();
baseUrl = "http://www.storkbabygiftbaskets.com/"
homepage = IndexPage('Home', baseUrl, br)
homepage.getLeftNavLinks()

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