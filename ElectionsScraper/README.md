# Elections Scraper

Elections Scraper is a Python web scraper script for getting Czech Republic parliamentary elections data from provided county.
Script can be used for elections from year 1996 up to today. 
https://volby.cz/

## Requirements

Required packages are listed in requirements.txt.
But you will need to install:

```bash
Python 3+
pip install beautifulsoup4
pip install requests
```

## Usage

Script needs to be provided with 2 arguments in the correct order/format -> url and filename.csv (filename can have whole os path to specify save destination)

For url - Choose year for ,,Poslanecká sněmovna Parlamentu ČR" at https://volby.cz/

Then select ,,Výsledky hlasování za územní celky" then find desired county and click on link in column ,,Výběr
obce" then you can use that url for the script
```bash
python electionsscraper.py "https://volby.cz/pls/ps2010/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205" "hodonin2010.csv" 
python electionsscraper.py "https://volby.cz/pls/ps2010/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6205" "c:\hodonin2010.csv" 
```
Example output is attached - look for .csv file
