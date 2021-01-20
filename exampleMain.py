# An example for our functions
# make sure you rename Q2.tennisCrawler.py to ---> Q2tennisCrawler
# and Q3.tennisRank.py to ---> Q3tennisRank.py before useage.
import sys
import lxml
from tennisRank import tennisRank
from tennisCrawler import tennisCrawler

import requests

if __name__ == '__main__':
    xpaths = [
        "//table[contains(@class,'sortable')]/tbody/tr/td[count(../../tr/th[contains(text(), 'Opponents')]/preceding-sibling::th)+1]/a[1]/@href",
        "//table[contains(@class,'sortable')]/tbody/tr/td[count(../../tr/th[contains(text(),'Partner')]/preceding-sibling::th)+1]/a[1]/@href"]
    url = 'https://en.wikipedia.org/wiki/Andy_Ram'
    listOfLists = tennisCrawler(url, xpaths)
    dictt = tennisRank(list_of_lists=listOfLists, numIters=100)
    sum = 0
    for d in dictt:
        print(d + " -----> " + str(dictt[d]))
        sum += dictt[d]
    print(str(sum))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
