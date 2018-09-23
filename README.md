# Web-Scrapper
A web scrapper in made with BeautifulSoup4 (work in progress)

This repository contains the code and HTML test cases used. Needs BeautifulSoup4 and csv modules to get it working. 

Background:
With the ludicrous amount of increase in information available on the internet, it is useful to have tools that can extract and organize data from web sites. HTML is used to create web pages and the language uses various "tags" to mark specific aspects of web pages. This web scrapper searches through information in tables created with HTML with BeautifulSoup4 by looking for the specific tags for tables, then searches for "header" tags in those tables and organizes that information with dictionaries using those headers as keys. This organization works for tables with a column for header, row for header, both for headers, and various other formats that HTML allows. These dictionaries are then placed onto a text file as "comma separated values" or csv. 

