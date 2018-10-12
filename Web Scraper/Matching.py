# -*- coding: utf-8 -*-
import sys
import csv
import codecs


reload(sys)
sys.setdefaultencoding('utf-8')

headers = []
with codecs.open('csvHeaders', 'r', 'utf-8-sig') as temp:
    reader = csv.reader(temp, delimiter = ',')
    for row in reader:
        for attribute in row:
            headers.append(attribute)
            print(attribute)

print(headers)



# Equal Names
def EN(newData, headers):
    for word in newData[0]:
        for synonym in headers:
            if synonym == word:
                headers.append(word)


# SCS
def scs(newData, headers):
    for word in newData[0]:
        for synonym in headers:
            levDist = calcLev(word, synonym)
            if levDist < len(synonym) // 2:
                headers.append(word)




# Levenshtein distance
def calcLev(s1, s2):

    rows, cols = len(s1) + 1, len(s2) + 1
    distance = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(1, rows):
        distance[i][0] = i
    for j in range(1, cols):
        distance[0][j] = j

    for row in range(1, rows):
        for col in range(1, cols):
            if s1[row-1] == s2[col-1]:
                cost = 0
            else:
                cost = 1

            distance[row][col] = min(distance[row -1][col] +1,
                                    distance[row][col -1] + 1,
                                     distance[row -1][col -1] + cost)

    return distance[row][col]



# # http://nlogn.tistory.com/340
def calcLevKor(first, second):

    first_len , second_len = len(first) , len(second)

    if first_len > second_len :
        first , second = second , first
        first_len , second_len = second_len , first_len

    current = range(first_len+1)

    for i in range(1,second_len+1):
        previous , current = current , [i]+[0]*second_len

        for j in range(1,first_len+1):
            add , delete = previous[j]+1 , current[j-1]+1
            change = previous[j-1]
            if first[j-1] != second[i-1]:
                change = change + 1

            current[j] = min(add , delete , change)

    return current[first_len]



print(calcLevKor('', 'this is'))