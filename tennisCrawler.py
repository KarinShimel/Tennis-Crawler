import sys

import numpy as np
import requests
import lxml.html
import random
import time

# url - to start crawling from
# urls - accumulating the discovered URLs during crawling
# test with urls = crawl("https://en.wikipedia.org/wiki/Elizabeth_II", [])

MAX_URLS = 80
urls = []
visitedURLs = []
list_of_lists = []

def dfs_crawler_step(url, query, depth=1):
    try:
        time.sleep(3)
        if url.startswith('/wiki/'):
            url = "https://en.wikipedia.org" + url


        res = requests.get(url)
        doc = lxml.html.fromstring(res.content)
        # we just visited this url, so we will add it to the visited
        visitedURLs.append(url)
        source_list = []
        my_urls = []
        i = 0

        for t in doc.xpath(query):
            try:
                if t.startswith('/wiki/'):
                    t = "https://en.wikipedia.org" + t
                source_dest_pair = []
                source_dest_pair.append(url)
                source_dest_pair.append(t)
                if source_dest_pair not in list_of_lists:
                  list_of_lists.append(source_dest_pair)
                # source_list.append(source_dest_pair)
                if t not in urls:
                    urls.append(t)
                my_urls.append(t)
                i = i + 1
            except:
                print("something went wrong in trying to read the links from the query")
                return depth - 1
        # if there are no viable links we will go back to the former url - we didn't get to the depth we wanted
        if i == 0:
            return depth - 1
        # adding the list of pages we got to from this url to the list of lists
        # list_of_lists.append(source_list)
        # if we got to depth 3 we want to stop with the dfs steps
        if depth == 3:
            return 3
        if i > 0:
            while len(my_urls) > 0:
                if len(visitedURLs) == MAX_URLS:
                    return 3
                # Choose random URL from the discovered ones
                rand = random.randint(0, len(my_urls) - 1)
                if my_urls[rand] in visitedURLs:
                    my_urls.remove(my_urls[rand])
                    continue
                try:
                    answer = dfs_crawler_step(my_urls[rand], query, depth + 1)
                    my_urls.remove(my_urls[rand])
                    if answer == 3:
                        return 3
                except:
                    # error in crawling URL, remove from list
                    my_urls.remove(rand)
                    pass
    except:
        pass


def tennisCrawler(url, xpaths):
    if url.startswith('/wiki/'):
        url = "https://en.wikipedia.org" + url
    time.sleep(3)
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    if url not in visitedURLs:
        visitedURLs.append(url)
    # Results are also appended to a text file
    source_list = []
    my_urls = []
    if url not in urls:
        urls.append(url)

    # Changing the list of xpaths into 1 valid xpath request
    query = ""
    for xpath in xpaths:
        if xpaths.index(xpath) == len(xpaths) - 1:
            query += xpath
        else:
            query += xpath + "|"

    # In this part, we essentially want to make a crawler the combines dfs and bfs, so we will use
    # a recursive function that will implement a dfs step and a function that will implement bfs
    # our bfs function will choose randomly a url from its urls, then dfs on it and continue for each url
    # until either we hit 80 crawled urls, or our urls in the first level have all been visited.
    # when that happens we will randomly choose one of the urls we can reach from our main url, the use another
    # bfs step on it and continue with our crawler.

    i = 0
    for t in doc.xpath(query):
        # .attrib['href']
        if t.startswith('/wiki/'):
            t = "https://en.wikipedia.org" + t
        source_dest_pair = []
        source_dest_pair.append(url)
        source_dest_pair.append(t)
        #source_dest_pair = (url, t)
        if source_dest_pair not in list_of_lists:
            list_of_lists.append(source_dest_pair)
        # source_list.append(source_dest_pair)
        if t not in urls:
            urls.append(t)
        my_urls.append(t)
        i = i + 1
    if i==0:
        print("no results from xpath query - try a diffrent url (for example: https://en.wikipedia.org/wiki/Andy_Ram ")
        return
    # now that we extracted all the urls, we will implement bfs
    my_visited = 0
    my_not_visited = my_urls
    while len(my_urls) >= my_visited:
        if len(visitedURLs) == MAX_URLS:
            return list_of_lists
        # Choose random URL from the discovered ones
        rand = random.randint(0, len(my_not_visited) - 1)
        if my_not_visited[rand] in visitedURLs:
            my_not_visited.remove(my_not_visited[rand])
            my_visited += 1
            continue
        try:
            #bfs step
            answer = dfs_crawler_step(my_not_visited[rand], query)
            my_visited += 1
            my_not_visited.remove(my_not_visited[rand])
        except:
            # error in crawling URL, remove from list
            my_not_visited.remove(rand)
            my_visited += 1
            pass

    # now that we finished our first level, we need to continue with bfs and dfs combined in the next level.
    while len(visitedURLs) <= MAX_URLS or len(my_urls) == 0:
        rand = random.randint(0, len(my_urls) - 1)
        tennisCrawler(my_urls[rand], xpaths)
        my_urls.remove(my_urls[rand])
        return list_of_lists


