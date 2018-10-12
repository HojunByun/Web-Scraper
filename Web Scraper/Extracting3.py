# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import sys
import csv
import codecs
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')


#initializing html file
with open('test websites/test3.html') as html_file:
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

            if cell.has_attr("scope") and cell["scope"] == "row": isRowHeader = True
            print(cellT)

            #rowspan & colspan
            if cell.has_attr('rowspan') and cell.has_attr('colspan'):
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

            if rowIndex > len(curRows) * 0.75 and isFullRow:
                pass

            elif rowIndex < len(curRows) //2 and isFullRow:
                rowHeaders[cellT] = cellIndex
                allRows[cellT] = rowIndex
                rowList.add(rowIndex)

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
                print(rowH, colH, rowHeaders[rowH], colHeaders[colH])

                #no cell added if colH and rowH in same col
                if rowHeaders[rowH] not in allCols:
                    newTableDict[curTable][(rowH,colH)] = \
                        tableDict[curTable][colHeaders[colH]][rowHeaders[rowH]]

    print('new')
    for header in newTableDict[curTable]:
        print('newTableDict[curtable][{}]'.format(header),newTableDict[curTable][header])



""""""""""""""""""""""""""""""""""""
print("\n\n\n\n")
for entry in tableDict:
    print(tableDict[entry])



with codecs.open('csv files/csvTest3', 'w', 'utf-8-sig') as temp:
    writer = csv.writer(temp, delimiter = ',')

    for i in tableDict:

        writer.writerow("")
        writer.writerow("")
        writer.writerow("Table {}".format(i))

        print(i)
        # writer.writerow(headers[i])

        for row in tableDict[i]:
            writer.writerow(row)


""""""""""""""""""""""""""""""""""""
