Project: Network Services that are Available in your area.

This project will extend to search by zip code to search for the services
available (cable, phone, Internet) to customers with a Charter
Communications.

Description: This project is made for interview purposes and I wanted
to try something that is related to network connectivity.
So, with the idea of showing how backend API will work for this topic I want to
illustrate it using this location base search.

Installation: I wrote this quick one-page application in FastApi and Unicorn in Pycharm IDE.
URL to test is http://127.0.0.1:8000/ as set on my local machine/server. 

To set up the environment we need to pip-install the following

Fast api
Unicorn
Venv
SQLite
SQL Alchemy

and I chose to do it in a Virtual environment because I believe it is more secure and isolated. 
Then I made small test APIs using manually entering items/categories to describe services and try to test the project.
I connected it to Sqlite db using Alchemy and modify the code accordingly.
I committed the initial commit in the git too and then modified the version with the connectivity.


I chose my table items to be
Id,
zipcode,
City,
price,
category.


Usage/Vision: when some come to the webpage enter their id or zip to search for the service provided to their place 
and compare the price. This project can be extended to the next phase by creating front end page and searching the city
name when the zip code is entered.

Project Structure:
Database.py: It has all the SQLAlchemy configurations.
Main.py: It is the main coding page where all the classes and objects are created along with CRUD API.
Models.py: it has all the table items that represent items of the table.
Readme: Documentation.
Scraper.py: I created to retrieve the Charter communication API but upon digging in the legal documentation I notice its
not allowed, so I chose my own.
Service_app.db: it is an auto generated Sqlite db from Main.py and its done automatically in FastApi.
Test_server.py: I created a script for manually testing for API for all the CRUD operations.


I used Postman to fill the database entries. ALso, created a simple script to generate few entries with the name of 
dataentery.py.

Documentation:
Here are the links to the documents I referred
FastApi: https://fastapi.tiangolo.com/tutorial/
Sqlite: https://www.sqlite.org/docs.html
Git: https://git-scm.com/doc
Postman: https://www.postman.com/

Acknowledgment: Thank you for the time to check my work. I enjoy doing this short exercise and hope to keep
enhancing this code for future reference. It was a fun exercise and hope you enjoyed it reading too. Looking forward to
speaking to you regarding this and more related topics.

Developed by Shallu Abbi
6/4/2023
