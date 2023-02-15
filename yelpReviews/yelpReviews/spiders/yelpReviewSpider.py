import scrapy


class yelpReviewSpider(scrapy.Spider):
    name = 'yelpReview'
    # Sort reviews by date
    sort_desc = '&sort_by=date_desc'
    start = '?start='
    # We need to collect url input from command line
    def __init__(self, *args, **kwargs):
        super(yelpReviewSpider,self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.initial_domain = self.start_urls[0]
    def parse(self, response):
        # Get the number of reviews to traverse pages correctly
        # This is also important to ignore invalid reviews that appear on yelp
        total_reviews = int(response.xpath('//html/body/yelp-react-root/div/div/div/div/div/div/div/div/span/a/text()').get().split()[0])
        # Traverse through urls and parse
        for review_count in range(total_reviews, -10, -10):
            new_url = self.initial_domain + self.start + str(review_count) + self.sort_desc
            yield scrapy.Request(new_url, callback=self.parse_page)

    def parse_page(self, response):
        # Remove instances of <br> so reviews arent broken up
        response = response.replace(body=response.body.replace(b'<br>', b''))
        # Following will query relevant data
        authors = response.css('.css-ux5mu6 .css-1m051bw::text').getall()
        content = response.xpath('//div/div/ul/li/div/div/p[contains(@class, "comment__09f24__gu0rG")]/span/text()').extract()
        ratings = response.xpath('//section/div/div/ul/li/div/div/div/div/span/div[contains(@role, "img")]/@aria-label').extract()
        dates = response.xpath('//div/div/ul/li/div/div/div/div/span[contains(@class, "css-chan6m")]/text()').extract()

        # Build out dictionary item of Yelp Review Content
        for item in zip(authors,content,ratings, dates):
            reviews = {
                    'author' : item[0],
                    'content' : item[1],
                    'rating' : item[2],
                    'date' : item[3],
            }
            yield reviews

        
        
