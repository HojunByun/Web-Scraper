from bs4 import BeautifulSoup
import requests
import sys
import csv
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


#initializing html file
with open('test websites/test.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# print(soup.prettify())



table = soup.table
print(table.prettify(formatter = None))



headers = []
cells = table.find_all("td")
rows = table.find_all("tr")
tables = soup.find_all("table")

print(table.contents[0])
cells = [[] for i in range(len(rows)-1)]



#putting each cell into 2D array
for rowIndex in range(0, len(rows)):

    #all the print statements are there to help the programmer see for what row/column
    #the scraper organized the information into
    print("")
    print("00000000000000000000000000000000000000000000")
    print("")

    # no rowspan
    for cell in rows[rowIndex].find_all("td"):
        x = cell.span.extract().text
        if rowIndex == 0:
            headers.append(x)
            print(x)
        else:
            if x == "":
                cells[rowIndex-1].append("Empty")
                print("Empty")

            else:
                cells[rowIndex-1] += [x]
                print(x)

""""""""""""""""""""""""""""""




#creates csv file 
with codecs.open('csv files/csvTest1', 'w', 'utf-8-sig') as temp:
    writer = csv.writer(temp, delimiter = ',')


    writer.writerow(headers)
    writer.writerow("")

    for row in cells[1:]:
        writer.writerow(row)



""""""""""""""""""""""""""""""


