## Yelp Review quick synopsis


#### State goal to start: 
 Whenever I am in an area where I would like to try a new restaurant, I play culinary detective.. scrounging through yelp/google reviews in an effort to determine a restaurant’s worthiness.  

 #### Methodology:  

* My method is to search within the “best” reviews (4 or 5 stars) to determine the prevalent positive features of the restaurant.This translates into the discovery of the restaurant’s “secret sauce” (the pull factor).
* On the flip-side I search within negative reviews  as well (1 or 2 stars); determine what are the restaurant's deterrents (why I might steer clear).
* Although when looking at high star and low star reviews, I consider that these reviewers opinions are potentially skewed. i.e people getting paid to write a review or on the other end someone having a bad day. 3 star reviews for this reason are especially valuable.```

It is important to mention that even if the above assessment is made and a restaurant is determined to be a viable option, there are several other factors which can lead to the restaurant not being chosen. Trying to determine what cuisine I am in the mood for, whether I have a preference for ambience (indoor or outdoor seating), or how far I am willing to travel are all conundrums that unless perfectly aligned can be grounds for vetoing a restaurant that passes a review check. All the more reason to come up with an improved solution.

#### Proposition:
**Automate the review portion of my restaurant decision process as it is the most arduous and time consuming.**  
* I/O seating, cuisine type and distance are shallow requirements that can be handled with some filtering.

### Implementation:
 Use some sort of web scraping implementation to parse yelp review data into JSON format. Process the reviews using NLP, more specifically a sentiment analysis model in order to collect information on what customers feel positively and negatively about. Aggregate data to generate a summary of findings. Iterate and refine algorithm/sentiment analysis.



#### Data:
1. User: number of reviews (take into account)
2. Review: Rating ( if low we can assure negativity with higher confidence
3. Content: what users report positively or negatively about  



  
### Steps Listed out by ChatGPT
1. First, I would research and choose a web scraping library that is suitable for the task at hand. Some popular libraries in Python include BeautifulSoup and Scrapy. I would then use this library to extract the reviews from the Yelp website.


2. Next, I would preprocess the data by cleaning and normalizing it. This would involve removing any irrelevant information such as special characters, stop words, and converting the text to lowercase.
After that, I would perform sentiment analysis on the reviews using natural language processing techniques such as tokenization, stemming and using a pre-trained sentiment analysis model such as NLTK's VaderSentiment or TextBlob.

3. Once the sentiment analysis is complete, I would conduct a statistical analysis on the data to yield a summary of the restaurant. This would include calculating the average sentiment score, identifying the most frequently used words and phrases, and identifying any patterns or trends in the data.

4.  Finally, I would use the insights gained from the sentiment analysis to understand why customers are choosing to come back and why customers might be deterred. This would involve identifying any specific reasons why customers have positive or negative feedback, and using this information to make recommendations for improving the restaurant's customer experience.

5. I would also consider visualizing the data using libraries such as matplotlib, seaborn, or Plotly to help better understand the results and present them in an easy-to-understand way.
6. I would then test the code and fix any bugs if any, and make it ready for deployment.
7. Finally, I would document the code, the steps followed, and the insights gained during the process, to make it easy for others to understand and continue working on the project if needed.



```Interesting note: could add an option to check for “deal breakers”. For instance if cleanliness is often negatively reviewed then that’s a deal breaker.```


# Progress Updates
## Review Scraping:
I decided to go with scrapy it was reviewed as the more robust and up to date web scraping tool.

One if not the most key elements when web scraping is trying to identify a consistent website structure so that we can programmatically scrape the site. 
In the case of yelp, based on my research it seems like it was a bit more easier in the past (~2018) to scrape.
Reviews used to have a pretty simple “review” class name along with authors of the reviews while currently reviews look a little more complicated.
So far not impossible.

It is important that we query the reviews ordered by most recent reviews first (descending). This will ensure stable/consistent results.
This can be done by appending the sort_by=date_desc query to our url.
##### The following are selectors I generated to gather the relevant review data:


* **Review Content:**  response.xpath('//div/div/ul/li/div/div/p[contains(@class, "comment__09f24__gu0rG")]/span/text()').extract()
* **Author:** response.css('.css-ux5mu6 .css-1m051bw::text').getall()
* **Rating:** response.xpath('//section/div/div/ul/li/div/div/div/div/span/div[contains(@role, "img")]/@aria-label').extract() 
* **Date:** response.xpath('//div/div/ul/li/div/div/div/div/span[contains(@class, "css-chan6m")]/text()').extract()

##### Now that we have collected the review data for the page we need to traverse the pages.
Pages turn over every 10 items so we need to visit each 10 at a time.
In order to this we will need to grab the total reviews from the page and
traverse the pages in increments of 10.

EX.  
Page 1: https://www.yelp.com/biz/example-res?sort_by=date_desc  
Page 2: https://www.yelp.com/biz/example-res?start=10&sort-by=date_desc

##### Pagination Implementation
To properly traverse the review pages I decided to first collect the total
number of reviews on the page.

**Number of Reviews:** int(response.xpath('//html/body/yelp-react-root/div/div/div/div/div/div/div/div/span/a[contains(@href, "#reviews")]/text()').get().split()[0])

Once we have the total number of reviews we can iterate over our reviews in
orders of 10 since we have 10 reviews per page.


##### Calling from comand Line
We can call our program from the command line:  

```scrapy crawl yelpReview -a start_url='https://www.yelp.com/biz/$restaraunt$' -o $file$.json```

## ToDo

1. Just discovered recent bug resulting in no output generated
2. Configure spider to feed data into sentiment analysis model

