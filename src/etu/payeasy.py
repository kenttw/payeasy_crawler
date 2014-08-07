import requests 
import sqlite3
import payeasyDB
import payEasyClass
import time
import re

from BeautifulSoup import BeautifulSoup



def getCategoryList():
    url = 'http://www.payeasy.com.tw/index.shtml'
    rs = requests.session() 
    rs_get = rs.get(url) 
    response = rs_get.text.encode('utf8')
    soup = BeautifulSoup(response)
    alist = soup.findAll('a')    
    links = []
    for item in alist:
        link = item['href']
        if isCategoryUrl(link):
            links.append(link)
            print link
    return links   

def startCrawl(url):
    
    rs = requests.session() 
    rs_get = rs.get(url) 
    response = rs_get.text.encode('utf8')
    soup = BeautifulSoup(response)
    # print soup
    total = soup.findAll('li',{'class':'no_bor'})[0].findAll('span')[1].text
    categoryID = getCategoryId(url)
    print total
    for i in range(1,int(total)):
        
        p_list = [];
        payload = {
                   'page' : i,
                   'sort' : 2,
                   'direction' : 1
                   }
        print url
        print payload
        rs_get = rs.get(url,data=payload) 
        response = rs_get.text.encode('utf8')
        soup = BeautifulSoup(response)
    #     print soup
        
        list = soup.findAll('li',{'class':'item'})
        
        for item in list:
            pp = payEasyClass.prodcut()
            pp.p_url = item.find('a')['href']
            pp.p_img = item.find('img')['src']
            pp.p_description = item.find('p',{'class':'ProductName'}).text
            pp.p_price = item.find('p',{'class':'ProducPrice'}).find('span').text
            pp.p_pid = getProductId(pp.p_url)

            p_list.append(pp)
        payeasyDB.savePostToSqlite(p_list,categoryID)
        time.sleep(1);
def getProductId(url):
    
#     http://www.payeasy.com.tw/ECShop/ProductDetail.jsp?pidnum=3420008
    r = re.match(r'.*pid[nN]um=([0-9]+)$', url)
    if r!=None:
        return r.group(1) + ""
    else:
        return None
    
def getCategoryId(url):
    r = re.match(r'^http://member\.payeasy\.com\.tw/EcCategoryV2/Product/ProductList/([0-9]+)$', url)
#     return r != None
    if r != None:
        return r.group(1) + ""
    
    
    
def isCategoryUrl(url):
    r = re.match(r'^http://member\.payeasy\.com\.tw/EcCategoryV2/Product/ProductList/([0-9]+)$', url)
    return r != None

def main():
    
    
    
#     print isCategoryUrl('http://member.payeasy.com.tw/EcCategoryV2/Product/ProductList/29652')
#     getCategoryList()
#     print getProductId('http://www.payeasy.com.tw/ECShop/ProductDetail.jsp?pidnum=3420008')
    
    clist = getCategoryList()
    for link in clist:
        startCrawl(link)
    
    pass
    
if  __name__ =='__main__':
    main()
    
    
