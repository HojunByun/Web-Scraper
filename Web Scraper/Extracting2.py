from bs4 import BeautifulSoup
import requests
import sys
import csv
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


#initializing html file
with open('test websites/test2.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

#print(soup.prettify())


headers = [[]]
tables = soup.find_all("table")


for table in tables:
    rowHeaders = table.find_all('th', scope= "row")


print("number of tables: ", len(tables))

tableDict = dict()

curTable = 0

for table in tables:
    curTable += 1
    curRows = table.find_all("tr")
    tableDict[curTable] = [[] for i in range(len(curRows))]
    rowIndex = 0
    skip = False

    print("THIS IS TABLE {}, with {} rows".format(curTable, len(curRows)))

    #putting each cell into 2D array
    for rowIndex in range(0, len(curRows)):
        #skips rows of table after rowspan or colspan, is flawed
        if skip:
            skip = False
            continue
        print("")
        print("00000000000000000000000000000000000000000000000000")
        print("")


        for cell in curRows[rowIndex].find_all(["td", "th"]):
            #when storing values next to <br>, stores as "\n"
            #problem when writing csv file
            cellT = cell.text.replace("\n", " ")
            print(cellT)

            #handle colspan
            if cell.has_attr("colspan"):
                if cellT == "": tableDict[curTable][rowIndex].append("Empty")
                else:

                    #sub categorize next row here
                    if rowIndex != len(curRows) -1:
                        subHeaders = curRows[rowIndex +1].find_all(["td", "th"])
                        for sub in subHeaders:
                            tableDict[curTable][rowIndex].append(sub.text)
                    skip = True

            #handle rowspan
            elif cell.has_attr("rowspan"):

                #place sameCol into the col where rowspan is over 1
                sameCol = cell.text
                print("sameCol: ", sameCol)

                if cellT == "": tableDict[curTable][rowIndex].append("Empty")
                else:  tableDict[curTable][rowIndex].append(cellT)

                #make next row's cell with same col
                if rowIndex != len(curRows) -1 and rowIndex != 0:
                    nextRow = curRows[rowIndex +1].find_all(["td", "th"])
                    tableDict[curTable][rowIndex +1].append(sameCol)

                    for next in nextRow:
                        if next.text == "": tableDict[curTable][rowIndex+1].append("Empty")
                        else: tableDict[curTable][rowIndex+1].append(next.text)

                #skip next row, *** cannot skip if colspan > 2 ***
                skip = True

            else:
                if cellT == "":
                    tableDict[curTable][rowIndex].append("Empty")
                else:
                    tableDict[curTable][rowIndex].append(cellT)





""""""""""""""""""""""""""""""""""""
#creates csv file
for entry in tableDict:
    print(tableDict[entry])


with codecs.open('csv files/csvTest2', 'w', 'utf-8-sig') as temp:
    writer = csv.writer(temp, delimiter = ',')

    for i in tableDict:

        writer.writerow("")
        writer.writerow("")
        writer.writerow("Table {}".format(i))


        for row in tableDict[i]:
            writer.writerow(row)


""""""""""""""""""""""""""""""""""""

