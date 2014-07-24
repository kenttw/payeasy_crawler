import requests
import sqlite3
import payeasyDB
import payEasyClass
import time

from BeautifulSoup import BeautifulSoup





# url = "http://member.payeasy.com.tw/EcCategoryV2/Product/ProductList/29663"
url = "http://member.payeasy.com.tw/EcCategoryV2/Product/ProductList/29652"
rs = requests.session() 
rs_get = rs.get(url) 
response = rs_get.text.encode('utf8')
soup = BeautifulSoup(response)
# print soup
total = soup.findAll('li',{'class':'no_bor'})[0].findAll('span')[1].text
print total
# total = "2"
# for item in list:
#     print item
 



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
#         print item
        pp = payEasyClass.prodcut
        pp.p_url = item.find('a')['href']
        pp.p_img = item.find('img')['src']
        pp.p_description = item.find('p',{'class':'ProductName'}).text
#         print p_description
        pp.p_price = item.find('p',{'class':'ProducPrice'}).find('span').text
#         print p_price
        ii = []
        ii.append(pp.p_url)
        ii.append(pp.p_img)
        ii.append(pp.p_description)
        ii.append(pp.p_price)
        
        p_list.append(ii)
    
    payeasyDB.savePostToSqlite(p_list)
    time.sleep(1);
