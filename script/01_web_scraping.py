
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import numpy as np
from itertools import zip_longest



headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Encoding": "gzip, deflate" 
}
dataF = pd.DataFrame()
for i in range(1,11):
    content=requests.get("https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&page={}".format(i),headers=headers).text
    data = BeautifulSoup(content,"lxml")

    con=data.find_all("div",class_="ZFwe0M row")
    names = []
    ratings= []
    discounted_price = []
    orginal_price = []
    off = []
    memory= []
    display = []
    cemera = []
    for i in con:
        names.append(i.find_all("div",class_="RG5Slk")[0].text)
        ratings.append(i.find_all("div",class_="MKiFS6")[0].text)
        discounted_price.append(i.find_all("div",class_="hZ3P6w DeU9vF")[0].text)
        divs = i.find_all("div", class_="kRYCnD gxR4EY")
        orginal_price.append(divs[0].text) if divs and divs[-1].text.strip() else "NaN"
        divs = i.find_all("div", class_="HQe8jr")
        off.append(divs[0].text.strip() if divs else "NaN")

        memory.append(i.find_all("li",class_="DTBslk")[0].text)
        display.append(i.find_all("li",class_="DTBslk")[1].text)
        cemera.append(i.find_all("li",class_="DTBslk")[2].text)
    
    df = pd.DataFrame(zip_longest(
    names,
    display,
    memory,
    cemera,
    orginal_price,
    discounted_price,
    off,
    fillvalue=np.nan
), columns=[
    "Name",
    "Display",
    "Memory",
    "Camera",
    "Original_Price",
    "Discounted_Price",
    "Off_Upto"
])
    dataF=pd.concat([dataF,df], ignore_index=True)
    
dataF.to_csv("data/raw/flipkart_raw.csv")






