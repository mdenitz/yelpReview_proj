import scrapy
import re


class yelpReviewSpider(scrapy.Spider):
    """ FileObject contains file metadata and makes attempts to get mp3 genre with spotipy package. 

    Class Attributes:
        name (str): Name of the Crawler

    Attributes:
        start_urls (list): List of starting urls (contains only yelp biz review)
        initial_domain (str): Starting initial yelp restaurant url
        """
    name = 'yelpReview'
    # We need to collect url input from command line
    def __init__(self, *args, **kwargs):
        super(yelpReviewSpider,self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.initial_domain = self.start_urls[0]
    def parse(self, response):
        """Responsible for building out all the restaraunt review urls
        Args:
            response (str): the response to parse
        """
        # Get the number of reviews to traverse pages correctly
        # This is also important to ignore invalid reviews that appear on yelp
        review_str = response.xpath('//html/body/yelp-react-root/div/div/div/div/div/div/div/div/span/a/text()').get()

        total_reviews = int(re.findall(r'\d+', review_str)[0]) 
        # Traverse through urls and parse
        for review_count in range(0, total_reviews, 10):
            new_url = "{initial}?sort_by=date_desc&start={count}".format(
                    initial=self.initial_domain, count=str(review_count))
            if review_count == 0:
                new_url = "{initial}?sort_by=date_desc".format(
                        initial=self.initial_domain)
            yield scrapy.Request(new_url, callback=self.parse_page)

    def parse_page(self, response):
        """ Grabs relevant review data and yields into dictionary entry
        Args:
            response (str): the response to parse
        """

        # Remove instances of <br> so reviews arent broken up
        response = response.replace(body=response.body.replace(b'<br>', b''))
        # Following will query relevant data
        authors = response.css('.css-ux5mu6 .css-1m051bw::text').getall()
        content = response.xpath('//div/div/ul/li/div/div/p[contains(@class, "comment__09f24__gu0rG")]/span/text()').extract()
        ratings = response.xpath('//section/div/div/ul/li/div/div/div/div/span/div[contains(@role, "img")]/@aria-label').re(r'(\d+)(?=\s)')
        dates = response.xpath('//div/div/ul/li/div/div/div/div/span[contains(@class, "css-chan6m")]/text()').extract()

        # Build out dictionary item of Yelp Review Content
        for item in zip(authors,content,ratings, dates):
            yield {
                    'author' : item[0],
                    'content' : item[1],
                    'rating' : int(item[2]),
                    'date' : item[3],
            }

        
        
