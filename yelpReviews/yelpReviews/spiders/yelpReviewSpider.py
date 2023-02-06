import scrapy


class yelpReviewSpider(scrapy.Spider):
    name = 'yelpReview'
    allowed_domains = ['https://www.yelp.com/biz/*']
    start_urls = ['https://www.yelp.com/biz/hide-sushi-japanese-restaurant-los-angeles?&sort_by=date_desc']
    sort_desc = '?&sort_by=date_desc'
    

#    def process_request(self, request, spider):
#        if '?&sort_by=date_desc' in request.url:
#            pass
#        new_url += '?&sort_by=date_desc'
#        request = request.replace(url=new_url)
#        return request
    def parse(self, response):
        # Remove instances of <br> so reviews arent broken up
        response = response.replace(body=response.body.replace(b'<br>', b''))
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
