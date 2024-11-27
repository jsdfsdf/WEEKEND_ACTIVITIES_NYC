import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class ActivitySpider(scrapy.Spider):
    name = "activities"
    start_urls = ['https://www.timeout.com/newyork/things-to-do/things-to-do-in-nyc-this-weekend']
 
    def parse(self, response):
        # this works but need to change the last numbers etc
        # for article in response.css('div.articleContent._articleContent_161ki_244'): # somehow this get 100 now just 20
        
        # below two ar ethe same right now
        for article in response.css('div.articleContent'): # might include one more
        # for article in response.xpath("//div[contains(@class, 'articleContent') and contains(concat(' ', normalize-space(@class), ' '), ' _articleContent')]"):
        # for article in response.css('div[class^="articleContent._articleContent_"]'):# doesnt work
        # for article in response.css('div[class*="articleContent"]'): # still 20 seems need infinete scrolling I dont want to bother
 
        # for article in response.css('div[class*="_articleContent"]'): # still 25 top
        # for article in response.xpath('//div[contains(@class, "_articleContent")]'):  # xpath only 25 top
            title = article.css('h3._h3_70r6w_1::text').get().strip()
            # description_parts = article.xpath('.//div[contains(@class, "_summaryContainer_")]/div/p/text()').getall() # work
            description_parts = article.xpath('.//div[contains(@class, "_summary_")]//p//text()').getall()   # // consider span inside p
            description = ' '.join([part.strip() for part in description_parts])
            yield {
                'title': title,
                'description': description,
            }

def get_cur_time():
    # Get the current date and time
    now = datetime.now()

    # Format the date and time for the filename
    filename_timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    return filename_timestamp

def scrape_data():
    '''return the json stored'''

    filename_timestamp = get_cur_time()
    # Create the filename
    filename = f"data/scrape/data_{filename_timestamp}.json"

    process = CrawlerProcess(settings={
        "FEEDS": {
            filename: {"format": "json", "overwrite": True},
        },

    })
    process.crawl(ActivitySpider)
    process.start()
    return filename


