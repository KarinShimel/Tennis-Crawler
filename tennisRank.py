import sys

import numpy as np


# Create an array of all the URLs.
def get_urls(list_of_lists):
    set_of_urls = []
    for pair in list_of_lists:
        if pair[0] not in set_of_urls:
            set_of_urls.append(pair[0])
        if pair[1] not in set_of_urls:
            set_of_urls.append(pair[1])
    return set_of_urls


def tennisRank(list_of_lists, numIters):
    urls = get_urls(list_of_lists)
    count = len(urls)
    epsilon = sys.float_info.epsilon
    randomteleport = 0.2 * (1 / count)
    indeg = inDegree(list_of_lists)
    outdeg = outDegree(list_of_lists)
    # initialization
    v0 = np.array([1 / count] * count)
    v1 = v0.copy()
    for i in range(numIters):
        for page in range(len(urls)):
            firstSigma = firstSig(indeg, outdeg, urls[page], v0, urls)
            thirdSigma = thirdSig(outdeg, v0, count, urls)
            v1[page] = firstSigma * 0.8 + randomteleport + thirdSigma * 0.8
            # convergence condition check - if the difference between the current and the previous page rank vector is samller than epsilon we will stop.
        if np.abs(v1 - v0).sum() <= epsilon:
            break
        else:
            v0 = v1.copy()
    output = dict()
    for i in range(len(v0)):
        output[urls[i]] = v0[i]
    return output

# the first part in the formula presented in this exercise
def firstSig(inDeg, outDeg, url, ranks, urls):
    sum = 0
    if url in inDeg.keys():
        for i in inDeg[url]:
            pageindex = urls.index(i)
            sum += (ranks[pageindex]) / len(outDeg[i])
        return sum
    else:
        return 0


# the last part in the formula presented in this exercise
def thirdSig(outdeg, ranks, count, urls):
    sum = 0
    for i in range(count):
        if urls[i] not in outdeg.keys():
            sum += ranks[i]
    sum = sum / count
    return sum


# generates a dict of all of the pages our current page reffers to
def outDegree(listOfPairs):
    urls_graph = dict()
    for pair in listOfPairs:
        if pair[0] not in urls_graph.keys():
            urls_graph[pair[0]] = []
        urls_graph[pair[0]].append(pair[1])
    return urls_graph


# generates a dict of all of the pages our current page reffered by
def inDegree(listOfPairs):
    urls_graph = dict()
    for pair in listOfPairs:
        if pair[1] not in urls_graph.keys():
            urls_graph[pair[1]] = []
        urls_graph[pair[1]].append(pair[0])
    return urls_graph
