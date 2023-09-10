from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import json
import time
import os
import sys

options = Options()
options.add_argument('--headless=new')
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

productsData=[]

def main():  
    config('https://www.etsy.com/')
    #setCountry()
    time.sleep(3)
    link=getCategory()
    gatherProducts(link)
    
def config(url):
    driver.get(url)
    driver.implicitly_wait(5)
    
def setCountry():
    driver.find_element(By.CSS_SELECTOR,('span[class="wt-display-inline-block wt-vertical-align-middle"]')).click()
    time.sleep(2)  
    select = Select(driver.find_element(By.ID,('locale-overlay-select-region_code')))
    select.select_by_value('US')
    driver.find_element(By.ID,('locale-overlay-save')).click()
    time.sleep(1)
    
def getCategory():
    data = open(f'categories.json')
    categoryLinks =json.load(data)    
    os.system('clear')
    print('You can press ctrl+c at any time to exit the script')
    link=''
    while link =='' or link=='CATEGORY NOT FOUND':
        category = input('Enter a valid category, check notes for help : ').upper()          
        a=[d.get(category,0) for d in categoryLinks]       
        for c in a:
            if c == 0:
                link="CATEGORY NOT FOUND"
            else:
                link=c
                break 
    config(link)
    return link
    
def gatherProducts(categorylink):
    minimumFavCount= input('Enter minimum favorites counts for each product: ')
    while True:
        if minimumFavCount.isnumeric() and int(minimumFavCount)>0:
            break
        else:
            minimumFavCount = input('Please enter a positive whole number: ')
    productsNumber = input(f'How many products above {minimumFavCount} favourites you want to sort by favorites? ')
    while True:
        if productsNumber.isnumeric() and int(productsNumber)>0:
            break
        else:
            productsNumber = input('Please enter a positive whole number: ')
    fileName = input('Enter file name for the HTML file: ')        
    print('Script is running...')        
    k = 0
    j = 2        
    while len(productsData)< int(productsNumber):
        productsLinks =[]    
        links = driver.find_elements(By.CSS_SELECTOR,('ol li a[class*="listing-link"]'))
        for i in range(0,4):
            links.pop((i*12))
            links.pop((i*12)+1)
            links.pop((i*12)+2)
            links.pop((i*12)+3)   
        for link in links:
            productsLinks.append(link.get_attribute('href')) 
        for productLink in productsLinks:        
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
                    
                    createHTML(fileName)
                    if len(productsData) == int(productsNumber):
                        os.system('clear') 
                        print(f'Searched {k+1} products')
                        print(f'Gathered {len(productsData)} product from {productsNumber} products')
                        sys.exit(1)
                else:
                    1
                os.system('clear')    
                k+=1
                if k == 1:
                    print(f'Searched {k} product')
                else:   
                    print(f'Searched {k} products')
                if len(productsData)== 1 or len(productsData) == 0:                
                    print(f'Gathered {len(productsData)} product from {productsNumber} products')
                else:
                    print(f'Gathered {len(productsData)} product from {productsNumber} products')
                print('Press ctrl+c to exit, gathered products won\' be lost')        
            except Exception as e:
                print(f'problem at product: {productLink}')
                print(e)
        newLink = categorylink[0:categorylink.find('catnav')]+f'pagination&page={j}'   
        driver.get(newLink)
        time.sleep(5)
        j+=1
               
def createHTML(fileName):  
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

 