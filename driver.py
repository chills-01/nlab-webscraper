from concurrent import futures
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import requests
import time
import concurrent.futures
from concurrent.futures import wait, ALL_COMPLETED
import pandas as pd
import parser
import os

from requests.api import get

def get_urls(url):
    r = requests.get(url, auth=('user', 'pass'))
    soup = BeautifulSoup(r.text, 'html.parser')
    prod_urls = []
    prods = soup.find_all('div', {'class':'product-browse-container col-md-5ths col-xs-6 col-sm-4'})
    for p in prods:
        prod_urls.append(base + p.find('a')['href'])
    
    df = pd.DataFrame(prod_urls)
    df.to_csv('product_urls.csv', mode='a', header=False, index=False)

def get_data(url):
    try:
        r = requests.get(url[0], timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        # get variables
        title = parser.get_title(soup)
        author = parser.get_author(soup)
        price = parser.get_price(soup)
        isbn = parser.get_isbn(soup)
        stock = parser.get_stock(soup)
        publisher = parser.get_publisher(soup)
        pub_date = parser.get_pub_date(soup)

        temp_df = pd.DataFrame([[title, author, price, isbn, stock, publisher, pub_date]], columns=cols)
        temp_df.to_csv(output_file, mode='a', header=False, index=False)
    except Exception as e: # timeout error usually
        print(str(e))
        temp_error_df = pd.DataFrame([url[0]])
        temp_error_df.to_csv(error_urls_file, mode='a', header=False, index=False)




## DRIVER 

current_time = time.time()
root_url  = "https://bookshop.nla.gov.au/category/books-3034.do?paginator.pageIndex="
base = "https://bookshop.nla.gov.au"
urls_file = 'product_urls.csv'
output_file = 'NLA_data.csv'
error_urls_file = "error_urls.csv"
cols = ['Title', 'Author', 'Price', 'ISBN', 'Stock', 'Publisher', 'Publication Date'] # for output

# urls to check
if urls_file not in os.listdir():
    page_urls = []
    for i in range(1, 220):
        page_urls.append(root_url + str(i))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_urls, page_urls)

source_urls = pd.read_csv(urls_file).to_numpy()
while len(source_urls) > 0:
    print('loop')
    print(len(source_urls), 'urls to search')

    # make file with headers if doesnt exist
    if output_file not in os.listdir():
        # output dataframe
        output_df = pd.DataFrame(columns=cols)
        output_df.to_csv(output_file, mode='w', header=True, index=False)

    # make errors file
    error_df = pd.DataFrame()
    error_df.to_csv(error_urls_file, mode='w', header=False, index=False)

    # do the scraping
    with concurrent.futures.ThreadPoolExecutor() as e:
        e.map(get_data, source_urls)


    # change new source to errors
    try:
        source_urls = pd.read_csv(error_urls_file).to_numpy()
    except:
        break

final_time = time.time()
print("Process took " + str(final_time-current_time) + " seconds")