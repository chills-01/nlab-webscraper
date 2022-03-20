from bs4 import BeautifulSoup
import numpy as np
import requests

IN_STOCK_STR = "This item is in stock and will be dispatched immediately."
OUT_STOCK_STR = "We are currently out of stock of this item. It will be ordered for you and placed on backorder. Once this item arrives in our store, we will ship it out for you."

def get_title(soup):
    try:
        return soup.find('h1', {'class': 'hidden-xs bookTitle-details'}).text.strip()
    except:
        return "Title not found"

def get_author(soup):
    try:
        return soup.find('span', {'class': 'details-author hidden-xs'}).text.strip()
    except:
        return "Author not found"

def get_price(soup):
    try:
        return soup.find('span', {'class': 'actual-price'}).text.strip()
    except:
        return 'Price not found'
    
def get_isbn(soup):
    try:
        return soup.find('h2', {'class' : 'productDetails-ISBN'}).text.strip()
    except:
        return 'ISBN not found'

def get_stock(soup):
    try:
        in_stock = soup.find('p', {'class' : 'details-availability'}).text.strip()
        if in_stock == '':
            print('diverting')
            description = soup.find('div', {'id' : 'product-details'}).text
            d_arr = description.split()
            stock_arr = []
            for el in d_arr[d_arr.index('Availability:')]:
                stock_arr.append(el)
            stock = ' '.join(stock_arr)
            if stock == IN_STOCK_STR:
                in_stock = "In stock"
            elif stock == OUT_STOCK_STR:
                in_stock = "Out of stock"
            else:
                in_stock = "Stock not found"
        return in_stock

    except:
        return 'Stock not found'

def get_publisher(soup):
    try:

        description = soup.find('div', {'id' : 'product-details'}).text
        d_arr = description.split()
        p_idx = d_arr.index('Publisher:') # gets the index of publisher
        publisher = []
        for el in d_arr[p_idx + 1:]:
            if el == 'ISBN:':
                break
            else: 
                publisher.append(el)

        if len(publisher) != 0:
            return ' '.join(publisher)
        else:
            raise Exception # pushes to except 
    except:
        return 'Not found'

def get_pub_date(soup):
    try:
        description = soup.find('div', {'id' : 'product-details'}).text
        d_arr = description.split()
        pd_idx = d_arr.index('Date:')
        p_date = []
        for el in d_arr[pd_idx + 1:]: # one after the title
                if el == 'Availability:' or el == 'Bind' or el == 'Audience:':
                    break
                else: 
                    p_date.append(el)
        if len(p_date) != 0:
            return ' '.join(p_date)
        else:
            raise Exception # pushes to except 
    except:
        return 'Not found'

# write request to file to avoid getting blocked
# r = requests.get('https://bookshop.nla.gov.au/book/beautiful-world-where-are-you.do', auth=('user', 'pass'))
# soup = BeautifulSoup(r.text, 'html.parser')
# with open("test2.html", "w") as file:
#     file.write(str(soup))

if __name__ == '__main__':
    soup = BeautifulSoup(open('test2.html', 'r'), 'html.parser')
    print(get_pub_date(soup))
