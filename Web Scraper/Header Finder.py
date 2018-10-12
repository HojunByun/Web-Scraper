# -*- coding: utf-8 -*-

"""
to be implemented in the future with AI recognition of headers without header tag in HTML
"""

from bs4 import BeautifulSoup
import requests
import sys
import csv
import codecs
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')


#initializing html file
with open('test3.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# print(soup.prettify())


# headers = dict()
tables = soup.find_all("table")



print("number of tables: ", len(tables))

tableDict = dict()
newTableDict = defaultdict(dict)


curTable = 0
for table in tables:
    #nested tables TOO HARD ㅠㅠㅠ
    subTable = table.find_all("table")
    if len(subTable) > 0:
        continue

    curTable += 1
    # headers[curTable] = set()
    curRows = table.find_all("tr")
    tableDict[curTable] = [[] for i in range(len(curRows))]


    newTableDict[curTable] = dict()

    isRowHeader = False
    rowSkip, rowS = float('inf'), False
    colSkip, colS = 0, False
    rowCounter = float('inf')


    print("\n\n")
    print("THIS IS TABLE {}, with {} rows".format(curTable, len(curRows)))


    """""""""""""""""""""""""""""""""""""""
    putting everything in 2D array
    """""""""""""""""""""""""""""""""""""""
    for rowIndex in range(0, len(curRows)):

        print("")
        print("00000000000000000000000000000000000000000000000000")
        print("")


        for cellIndex in range(len(curRows[rowIndex].find_all(["td", "th"]))):
            #when storing values next to <br>, stores as "\n"
            #problem when writing csv file
            cell = curRows[rowIndex].find_all(["td", "th"])[cellIndex]
            cellT = cell.text.replace("\n", " ")

            if rowCounter < rowSkip:
                rowS = False
                rowCounter = float('inf')

            if cell.has_attr("scope") and cell["scope"] == "row":
                isRowHeader = True
            print(cellT)

            #rowspan & colspan
            if cell.has_attr('rowspan') and cell.has_attr('colspan'):
                print('yes')
                rowSkip = cellIndex
                for i in range(int(cell['rowspan'])):
                    for j in range(int(cell['colspan'])):
                        if cellT == "":
                            tableDict[curTable][rowIndex +i].insert((cellIndex +j, "Empty"))
                        else:
                            tableDict[curTable][rowIndex + i].insert(cellIndex + j, cellT)
                boxStart, boxEnd = cellIndex, cellIndex + int(cell['colspan']) -1

            #colspan
            elif cell.has_attr("colspan"):
                colSkip = cellIndex + int(cell['colspan'])
                colS = True
                print("colSkip: ", colSkip)
                for i in range(int(cell['colspan'])):
                    if cellT == "":
                        tableDict[curTable][rowIndex].insert(cellIndex, "Empty")
                    else:
                        tableDict[curTable][rowIndex].insert(cellIndex, cellT)

            #handle rowspan
            #rowspans
            elif cell.has_attr("rowspan"):
                rowSkip = cellIndex
                rowS, rowCounter = True, int(cell['rowspan'])
                print("rowSkip: ", rowSkip)
                for i in range(int(cell['rowspan'])):
                    if cellT == "":
                        tableDict[curTable][rowIndex +i].insert(cellIndex, "Empty")
                    else:
                        tableDict[curTable][rowIndex +i].insert(cellIndex, cellT)

            #normal cells
            else:

                if rowS and cellIndex < rowSkip:
                    print('rowSkip, colSkip, cellIndex, rowCounter: ', rowSkip, colSkip, cellIndex, rowCounter)
                    if cellT == "":
                        tableDict[curTable][rowIndex].insert(cellIndex, "Empty")
                    else:
                        tableDict[curTable][rowIndex].insert(cellIndex, cellT)
                else:
                    if cellT == "":
                        tableDict[curTable][rowIndex].append("Empty")
                    else:
                        tableDict[curTable][rowIndex].append(cellT)


    """""""""""""""""""""""""""""""""""""""
    organizes tableDict data
    """""""""""""""""""""""""""""""""""""""
    #creates dictionaries of headers in row and col and their indexes to
    #get values from the table made by extractor above
    rowHeaders, colHeaders = dict(), dict()
    allCols, allRows, rowList = set(), dict(), set()

    for rowIndex in range(0, len(curRows)):
        isFullRow = False
        thisRow = []
        for cellIndex in range(len(curRows[rowIndex].find_all('th'))):
            if len(curRows[rowIndex].find_all('th')) >= len(curRows[rowIndex].find_all(['th', 'td'])) * 0.75:
                isFullRow = True


            cell = curRows[rowIndex].find_all("th")[cellIndex]
            cellT = cell.text.replace("\n", " ")

            #if headers on last row
            if rowIndex > len(curRows) * 0.75 and isFullRow:
                pass

            #rowheaders
            elif rowIndex < len(curRows) //2 and isFullRow:
                rowHeaders[cellT] = cellIndex
                allRows[cellT] = rowIndex
                rowList.add(rowIndex)

            #colheaders
            elif cell.has_attr("scope") and cell['scope'] == 'row' or \
                    cellIndex < len(curRows[rowIndex]) // 2:

                colHeaders[cellT] = rowIndex
                allCols.add(cellIndex)


    print(len(rowHeaders), "rowHeaders: ", rowHeaders)
    print(len(colHeaders), "colheaders: ", colHeaders)


    """""""""""""""""""""""""""""""""""""""""""""
    placing everything into 2 or 1 key dictionary
    """""""""""""""""""""""""""""""""""""""""""""
    #for only row headers
    if len(colHeaders) == 0:
        for rowH, value in rowHeaders.items():
            input = []

            for rowIndex in range(len(tableDict[curTable])):
                for cellIndex in range(len(tableDict[curTable][rowIndex])):
                    if cellIndex == value and tableDict[curTable][rowIndex][value] not in rowHeaders:
                        input.append(tableDict[curTable][rowIndex][value])

            newTableDict[curTable][rowH] = input

    #for only col headers
    elif len(rowHeaders) <= 2:

        #recognizes that all headers are in 1 col, swaps rowheader to col
        for rowH, value in rowHeaders.items():
            for col in allCols:
                if value == col:
                    colHeaders[rowH] = allRows[rowH]
                    del rowHeaders[rowH]

        print("revised",rowHeaders, colHeaders)

        #places values with header into dictionary
        for colH in colHeaders:
            input = []
            valueList = tableDict[curTable][colHeaders[colH]]
            for value in valueList:
                if value != colH and value not in rowHeaders and value not in colHeaders:
                    input.append(value)
            newTableDict[curTable][colH] = input

    #for row and col headers
    else:
        print('passed here')
        for rowH in rowHeaders:
            for colH in colHeaders:
                # try:
                #     newTableDict[curTable][rowH][colH] = \
                #         tableDict[curTable][rowHeaders[rowH]][colHeaders[colH]]
                # except KeyError:
                #     print("KeyError: ",tableDict[curTable])
                # print(tableDict[curTable][(colHeaders[colH],rowHeaders[rowH])])
                print(rowH, colH, rowHeaders[rowH], colHeaders[colH])

                #no cell added if colH and rowH in same col
                if rowHeaders[rowH] not in allCols:
                    newTableDict[curTable][(rowH,colH)] = \
                        tableDict[curTable][colHeaders[colH]][rowHeaders[rowH]]

    print('new')
    for header in newTableDict[curTable]:
        print('newTableDict[curtable][{}]'.format(header),newTableDict[curTable][header])



""""""""""""""""""""""""""""""""""""


def typeTest(posH, cells):
    HType = type(posH)
    numer, deno = 1, 1
    for cell in cells:
        if type(cell) == HType:
            deno += 1

    return numer / deno



def lenTest(posH, cells):
    Hlen = len(posH)
    numer, deno = 1, 1
    for cell in cells:
        # if   x < Hlen .....   < y :
        # if cell len is bigger by over magnitude of 2
        if Hlen < len(cell) and len(cell) // Hlen < 2:
            multi = Hlen / len(cell)

        # if posH len is bigger by over magnitude of 2
        elif Hlen > len(cell) and Hlen // len(cell) < 2:
            multi = (cell) / Hlen

        #if its in between
        else:
            pass

    return


# def fontTest(posH, cells):
#     pass


def placementTest(posH, cells, table):
    isFirstRow, isFirstCol = False, False

    firstRow = table[0]
    firstCol = [table[i][0] for i in range(len(table))]

    for cell in firstRow:
        if lenTest(cell)  > (some factor) and/or typeTest(cell) > (some factor) and/or

    for cell in firstCol:
        if lenTest(cell) > (some factor) and/or typeTest(cell) > (some factor) and/or


def differenceCheckRow(row, rowIndex, table):

    for cell in table[rowIndex]:

        #type check + len check
        pass



def differenceCheckCol(col, colIndex, table):
    curCol = [table[i][colIndex] for i in range(len(table))]

    for cell in curCol:

        #type check + len check
        pass



def numOrderCheck(col):

    for i in range(len(col)):
        if col[i] == i:
            continue
        else:
            return False
    return True


def imageTest():
    pass

def alignmentTest():
    pass

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




""""""""""""""""""""""""""""""""""""""""""""""""""""""
print("\n\n\n\n")
for entry in tableDict:
    print(tableDict[entry])


with codecs.open('csvTest3', 'w', 'utf-8-sig') as temp:
    writer = csv.writer(temp, delimiter = ',')

    for i in tableDict:

        writer.writerow("")
        writer.writerow("")
        writer.writerow("Table {}".format(i))

        print(i)
        # writer.writerow(headers[i])

        for row in tableDict[i]:
            writer.writerow(row)


""""""""""""""""""""""""""""""""""""""""""""""""""""""

