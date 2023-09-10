# steps to running the script:

## 1- install the latest python for macOS :- https://www.python.org/downloads/macos/

### 1.1- After installing open terminal and type 'python3 --version' to check python is installed successfully

## 2- type 'pip3 install selenium'

### 2.1- right-click on the etsy folder and then choose 'new terminal tab at folder'

## 3- to run the script type in terminal 'python3 categoriesSearch.py'

### 3.1- then you enter category name, check modifiedCategories images for help with categories

### 3.2- you enter the minimum favorite count for each product

### 3.3- you then enter the amount of products you want that is above the specified minimum favorites, and an output file name
		
### 3.2.1- take into consideration that if you name a file with an existing file name, that file will be deleted

### 3.3- if a search is taking too long you can exit using ctrl+c, the search progress is saved

## 4- a different version is 'python3 customSearch.py' in it you can search etsy.com with any key words

### 4.1- in this mode you have to enter a defined number of products to be searched

### 4.2- the products then are sorted by favorites not counting for the favorites filter

## 5- the setCategories file doesn't need to be run unless a major update happened to etsy.com
