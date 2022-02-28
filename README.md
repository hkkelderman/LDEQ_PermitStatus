## LA DEQ Permit Status Database Scraper

#### Introduction

This is a series of Python scripts written to check for permit status updates from [LDEQ's Check Permit Status Search](https://internet.deq.louisiana.gov/portal/ONLINESERVICES/CHECK-PERMIT-STATUS) page. 
This script downloads the entire Excel spreadsheet and compares it to a previous version of the spreadsheet. It's then sorted to look for only the AI numbers we care about here at EIP. The updates are then sent in an email to the invidiual tracking these updates.

#### In this repository
1. **dataDifferencesAlert.py** - The Python file that scrapes the new data, compares it to the old, and then sends the updates. The file generates three CSVs:
	- **temp_file.csv** - A CSV of the newly scraped permit database
	- **DataUpdates.csv** - A CSV of the permit updates made to specific AIs
	- **old_file.csv** - Overwrites the existing `old_file.csv` at the end of the script
2. **functions.py** - This is a python file that contains all the functions used in the `dataDifferencesAlert.py` file.
3. **LA_AIs** - A CSV file containing all the AI numbers we care about at EIP. This can be changed/added to when new projects are added.
4. **old_file.csv** - An initial download of the permit database.
5. **requirements.txt** - This is a text file of the package requirements in order to run the app.