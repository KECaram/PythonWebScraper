#!/usr/bin/python
# Keith Caram
# INFO.305.061: Survey of Python, Perl, and PHP
# Assignment #5 - Python Web App
#											Program Summary
#This is a python web app that scrapes a number of pages from books.toscrape.com - a web scraping
#sandbox site - for the titles, prices, and ratings of the books displayed on the pages. The home
#page promts the user for the range of pages from the site that it would like to scrape data from,
#and the way that the user would like to have the data displayed on the results page. After 
#submitting the form, the app validates the form data, and if valid, scrapes the data from the desired
#pages at books.toscrape.com, stores it as session data in a json objectsends the user to the list 
#age where all of the scraped data is displayed on screen in a table. The user then is prompted to 
#save the data or search for a specific title in the list of displayed books. If the user decides to 
#save, they must enter a valid filepath and a file name - if both these are valid and the user submits
#the data, they are brought to a success screen. If the user chooses to search for a title, they are
#redirected to a new page with a success or failure message and then are prompted to either search
#for a new title or save the list. At any point the user can return to the homepage and start a new
#scrape.

from bs4 import BeautifulSoup as bs4
import requests
import os.path
import json
import pandas as pd 
from flask import Flask, request, render_template, url_for, session

app = Flask(__name__)
app.secret_key = "password"
	
#renders home page
@app.route("/")
def home():
	return render_template('index.html')

#calls scraper, handles, and renders information to display on list page
@app.route("/view", methods=['POST'])
def listView():
	session.clear()
	pg1 = request.form["pgs1"]
	pg2 = request.form["pgs2"]
	srt = request.form['sort']
	if(len(pg1) >= 1 and pg1.isdigit() and len(pg2) >= 1 and pg2.isdigit() ):
		df= scraper(pg1, pg2, srt)
		session['user'] = df.to_json()
		return render_template('list.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values, Title="Scraped Data")
	else:
		return render_template('index.html', Invalid="Invalid Entry. Please enter an Integer number of pages to search.")

#handles and renders appropriate save output
@app.route("/save", methods=['POST'])
def saveScrape():
	save = request.form['save']
	name = request.form['filename']
	if(os.path.exists(save) == False):
		return render_template('list.html', Validation="Invalid file path. Please enter a valid file path.", Title="Save Failed")
	elif "user" in session:
		data = session['user']
		with open(save + "/" + name + ".json", 'w') as output:
			json.dump(json.JSONDecoder().decode(data), output)
		return render_template("save.html", Path=save, FileName=name)
	else:
		pass

#handles and renders appropriate find page
@app.route("/find", methods=['POST'])
def findScrape():
	find = request.form['find']
	data = session['user']
	if(len(find) == 0):
		return render_template("search.html", Result="Title "+ find + " was not found.")
	elif find in data:
		return render_template("search.html", Result="Title "+ find + " was found.")
	else:
		return render_template("search.html", Result="Title "+ find + " was not found.")

#web scraper method
def scraper(pgs1, pgs2, srt):
	pages=[]
	prices=[]
	stars=[]
	titles=[]

	data= {'Title' : titles,
		'Price' : prices,
		'Rating' : stars}

	for numPgs in range(int(pgs1), int(pgs2)+1):
		url = ('http://books.toscrape.com/catalogue/category/books_1/page-{}.html'.format(numPgs))
		pages.append(url)
	for item in pages:
		page = requests.get(item)
		soup = bs4(page.text, 'html.parser')
		for iterA in soup.findAll('h3'):
			ttl=iterA.getText()
			titles.append(ttl)
		for iterB in soup.findAll('p', class_='price_color'):
			price= iterB.getText()
			prices.append(price)
		for iterC in soup.findAll('p', class_='star-rating'):
			for key, value in iterC.attrs.items():
				star =value[1]
				stars.append(star)

	if(srt == "title"):
		titles.sort()
	elif(srt == "price"):
		prices.sort()
	elif(srt == "rating"):
		stars.sort()

	df = pd.DataFrame(data=data)
	return df

if __name__ == '__main__':
	app.run()