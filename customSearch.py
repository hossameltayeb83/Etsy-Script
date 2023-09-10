from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import os
import sys

options = Options()
options.add_argument('--headless=new')
options.add_argument("--window-size=1920,1080")
minimumFavCount = minimumFavCount= input('Enter minimum favorites counts for each product: ')
driver = webdriver.Chrome(options=options)
time.sleep(1)
os.system('clear')
try:
    while True:
        if minimumFavCount.isnumeric() and int(minimumFavCount)>0:
            break
        else:
            minimumFavCount = input('Please enter a positive whole number: ')
    fileName = input('Enter HTML file name : ')    
except KeyboardInterrupt:
    print('')
    print('Exited...')
    sys.exit(1)            



productsData=[]

def main():
    config('https://www.etsy.com/')
    #setCountry()
    search()
    productsLinks=gatherProductsLinks()
    gatherProductsData(productsLinks)
    

def config(url):
    driver.get(url)
    driver.implicitly_wait(5)
    
def setCountry():
    driver.find_element(By.CSS_SELECTOR,('span[class="wt-display-inline-block wt-vertical-align-middle"]')).click()
    time.sleep(1)  
    select = Select(driver.find_element(By.ID,('locale-overlay-select-region_code')))
    select.select_by_value('US')
    driver.find_element(By.ID,('locale-overlay-save')).click()
    time.sleep(1)
    
def search():
    
    searchQuery= input('What do you want to search for? ')
    search = driver.find_element(By.ID,('global-enhancements-search-query'))
    search.send_keys(searchQuery)   
    driver.find_element(By.CSS_SELECTOR,('form[id="gnav-search"] button[type="submit"]')).click()
    
def gatherProductsLinks():
    productsNumber = input('How many products you want to sort by favorites? ')
    while True:
        if productsNumber.isnumeric():
            break
        else:
            productsNumber = input('Please enter a whole number: ')
    print('Script is running...')        
    productsLinks =[]        
    while len(productsLinks)< int(productsNumber):
        links = driver.find_elements(By.CSS_SELECTOR,('ol li a[class*="listing-link"]'))
        for i in range(0,4):
            links.pop((i*12))
            links.pop((i*12)+1)
            links.pop((i*12)+2)
            links.pop((i*12)+3)     
        for link in links:
            productsLinks.append(link.get_attribute('href'))      
        nextBTN = driver.find_elements(By.CSS_SELECTOR,('nav > ul[class="wt-action-group wt-list-inline search-pagination "] li:last-child a'))[1]
        nextBTN.click()
        time.sleep(5)
    return productsLinks[0:int(productsNumber)]    
               
def gatherProductsData(productsLinks):
    requestedProducts = len(productsLinks)
    remaining = 0
    for productLink in productsLinks:
        os.system('clear')
        if requestedProducts-remaining == 1:
            print(f'{requestedProducts-remaining} product left to be scraped from {requestedProducts}')
            print('Press ctrl+c to exit, gathered products won\' be lost')  
        else:    
            print(f'{requestedProducts-remaining} products left to be scraped from {requestedProducts}')
            print('Press ctrl+c to exit, gathered products won\' be lost')   
        remaining += 1   
        try:
            driver.get(productLink)
            productName = driver.find_element(By.CSS_SELECTOR,('h1')).text
            productPrice = driver.find_element(By.CSS_SELECTOR,('p[class*="wt-text-title-03 wt-mr-xs-1 "]')).text    
            productImage = driver.find_element(By.CSS_SELECTOR,('[data-carousel-first-image]')).get_attribute('src')
            productDate= driver.find_element(By.CSS_SELECTOR,('div[class="wt-pr-xs-2 wt-text-caption"]')).text
            try:                      
                productFavCount = driver.find_elements(By.CSS_SELECTOR,('div > a[class="wt-text-link"]'))[0].text
            except:
                productFavCount= '0 favorite'    
            
            if productFavCount == 'One favorite':
                productFavCount='1 favorite'
            elif 'favorite' not in productFavCount:
                productFavCount = '0 fav'
            if int(productFavCount[0:productFavCount.find(' f')]) >int(minimumFavCount):     
                productsData.append({'Product Name':productName,'Product Link':productLink,'Product Image':productImage,'Product Price':productPrice,'Product Date':productDate,'Favorites Count':productFavCount})   
                createHTML()
        except Exception as e:
            driver.get_screenshot_as_file("screenshot.png")
            print(f'problem at product: {productLink}')
            print(e)   
        
def createHTML():
    os.system('clear')
    
    file=open(f'{fileName}.html','w',encoding="utf-8")
    templateHead=f'''<!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>{fileName}</title>
                        <link href="style.css" rel="stylesheet">
                    </head>
                    <body>
                    <table data-table-theme="dark zebra">
                    <thead>
                        <tr>
                        <th scope="col">Product Name</th>
                        <th scope="col">Product Image</th>
                        <th scope="col">Product Price</th>
                        <th scope="col">Product Date</th>
                        <th scope="col">Favorites Count</th>
                        </tr>
                    </thead>
                    <tbody>''' 
    file.write(templateHead)
    for product in productsData:
        productInfo = f'''<tr>
                            <td><a href="{product['Product Link']}" target="_blank">{product['Product Name']}</a></th>
                            <td><img src="{product['Product Image']}"></td>
                            <td>{product['Product Price']}</td>
                            <td>{product['Product Date']}</td>
                            <td>{product['Favorites Count']}</td>
                        </tr>'''
        try:       
            file.write(productInfo)
        except:
            1    
    templateBody='''        </tbody>
                        </table>
                        <script src="sorting.js"></script>  
                    </body>
                    </html>'''
    file.write(templateBody)
    file.close()
    
try:
    main()
except KeyboardInterrupt:
    print('')
    print('Exited...')
    sys.exit(1)            


 