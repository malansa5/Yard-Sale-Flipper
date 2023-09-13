import cv2 
from pyzbar.pyzbar import decode
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

capture = cv2.VideoCapture(0)
capture.set(3,640)
capture.set(4,480)


while (capture.isOpened()):
    success, frame = capture.read()
    if not success:
        break

    frame=cv2.resize(frame, (600, 400))
    cv2.imshow('Barcode Scanner', frame)
    cv2.waitKey(1)

    for code in decode(frame):
        barcodeItem = code.data.decode('utf-8')
        print(barcodeItem)
        print(code.data.decode('utf-8'))
        time.sleep(5)

cv2.destroyAllWindows() 

#barcodeItem = '8011003872077'

def get_item(barcodeItem):
    url = f'https://www.barcodelookup.com/{barcodeItem}'
    r = requests.get(url)
    if r.status_code != 200:
        print('Failed to get data: ', r.status_code)
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def find_item(soup):
    results = soup.find_all('div', {'class': 'col-50 product-details'}).text
    for item in results:
        product = item.find('h4').text
    return product


def get_data(productItem):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={productItem}&_sacat=0&LH_TitleDesc=0&_odkw=792850910393&_osacat=0'
    r = requests.get(url)
    if r.status_code != 200:
        print('Failed to get data: ', r.status_code)
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

def parse(soup):
    productlist = []
    results = soup.find_all('div', {'class': 's-item__details clearfix'}).text
    for item in results:
        productInfo = {
            'title' : item.find('span', {'role': 'heading'}).text,
            'soldprice' : float(item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',', '').strip()),
            'link' : item.find('a', {'class' : 's-item__link'})['href'],
        }
        #print(productInfo)
        productlist.append(productInfo)
    return productlist

def export(productlist):
    productsdf = pd.DataFrame(productlist)
    productsdf.to_csv('testoutput.csv', index=False)
    print('Saved to CSV')
    return

soup = get_item(barcodeItem)
product = find_item(soup)

soup = get_data(product)
productlist = parse(soup)
export(productlist)


