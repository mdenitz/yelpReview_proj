import scrapy
import re
import json
from datetime import datetime

class yelpReviewSpider(scrapy.Spider):
     """ FileObject contains file metadata and makes attempts to get mp3 genre with spotipy package. 

    Class Attributes:
        name (str): Name of the Crawler

        """
    name = 'yelpReview'

    def start_requests(self):
        url = getattr(self, 'url', None)
        if url:
            yield scrapy.Request(url, self.parse_reviews)

    def parse_reviews(self, response):
        """Responsible for building out all the restaraunt review urls
        Args:
            response (str): the response to parse
        """
        review_str = response.xpath('//html/body/yelp-react-root/div/div/div/div/div/div/div/div/span/a/text()').get()
        total_reviews = int(re.findall(r'\d+', review_str)[0])

        for review_count in range(0, total_reviews, 10):
            new_url = "{initial}?sort_by=date_desc&start={count}".format(
                initial=response.url, count=str(review_count))
            if review_count == 0:
                new_url = "{initial}?sort_by=date_desc".format(initial=response.url)
            yield scrapy.Request(new_url, callback=self.parse_review_page)

    def parse_review_page(self, response):
        """ Grabs relevant review data and yields into dictionary entry
        Args:
            response (str): the response to parse
        """
        response = response.replace(body=response.body.replace(b'<br>', b''))

        json_text = response.xpath("//script[@type='application/ld+json']/text()").getall()
        dict_text = {}
        input_format = "%Y-%m-%dT%H:%M:%S%z"
        output_format = "%m/%d/%Y"
        for text in json_text:
            dict_text = json.loads(text)
            if not 'review' in dict_text:
                continue
            for item in dict_text['review']:
                # Parse the input date string into a datetime object
                date_obj = datetime.strptime(item['datePublished'], input_format)
                # Convert the datetime object to the desired output format
                output_date = date_obj.strftime(output_format)
                yield {
                    'author': item['author'],
                    'content': item['description'],
                    'rating': int(item['reviewRating']['ratingValue']),
                    'date': output_date,
                }
                    
      
      
