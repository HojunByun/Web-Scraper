# Web-Scrapper
A web scrapper in made with BeautifulSoup4 (work in progress)

This repository contains the code and HTML test cases used. Needs BeautifulSoup4 and csv modules to get it working. 

Background:
With the ludicrous amount of increase in information available on the internet, it is useful to have tools that can extract and organize data from web sites. HTML is used to create web pages and the language uses various "tags" to mark specific aspects of web pages. This web scrapper searches through information in tables created with HTML by using Python and BeautifulSoup4. The scrapper looks for the specific tags for tables, then searches for "header" tags in those tables and organizes the information pertaining to those headers into dictionaries using those headers as keys. This organization works for tables with a column for header, row for header, both for headers, and various other formats that HTML allows. These dictionaries are then placed onto a text file as "comma separated values" or csv. 

The next step is to integrate Artificial Intelligence with the scrapper by eliminating the need to search for the specific "header" tags that are not always present in web tables. If AI can be used to recognize headers and distinguish them from regular cells than the range of web tables that can be scrapped would increase tremendously.

The zip folder contains the 3 versions of the scrapper from "Extracting1" to "Extracting2" to "Extracting3" that show its course of development.
