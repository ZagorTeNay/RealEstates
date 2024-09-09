# Web crawler for real estate website in Serbia

This is a small web crawler made with BeautifulSoup and Python for crawling of real estate websites, so that the data can be used in the future for 
data analysis of the market.

Currently only Nekretnine.rs website is supported.

## Using the scraper

Simply run the scrape.py script, which will output 'out.csv' file which will contain all info I deemed necessary from real estates on the website.

**Beware, currently if something fails while crawling, only websites until that point will be saved into output file.** 
It is now not possible to continue crawling from the point of failure, if run again it will simply start from the beginning of the links.


## TO DO

- Crawl whole website in one point in time and save outputed csv file
- Do data analysis on the crawled data 
- Separate execution into multiple processes for different use
- A process for saving links of estates into the database, in which case we could run script multiple times and add any new estates
- A process for reading uncrawled links from the database and crawl them
- A process for saving crawled data into database
- Add support for different websites
