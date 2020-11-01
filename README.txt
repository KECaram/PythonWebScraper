***These are all the packages that need to be installed in order to run my app. You may have to replace 'python' with 'python3' or 'pip' with 'pip3' depending on your aliases, so if you're having trouble with any of the commands try that alteration first.***

python -m pip install --user --upgrade pip
python -m pip install --user virtualenv

***After installing pip and virtualenv travel to the 'WebScraper' directory and execute the script "source env/bin/activate" to activate the virtual environment and install packages below.***

sudo apt-get install python3-bs4
pip install beautifulsoup4
pip install requests
pip install pandas
pip install flask

***I may have changed my program so that these packages are no longer needed. Install them in your virtualenv just in case.***

pip install xmls
pip install html5lib

***After installing all packages executing the command "python WebScraper.py" should launch the app and you should be able to access the home page by typing "localhost:5000" into your preferred web browser.***

***I chose to keep this app as a sandbox scraper as I am new to scraping, I know the site data will stay consistent therefore the app's results will be consistent in its results, and I know that the host of the site will not get mad at me for scraping their data. In the future I would definitely like totry this type of app on a more complex site.***
