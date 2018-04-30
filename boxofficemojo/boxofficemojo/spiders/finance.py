# script to collect movie financial data from the-numbers

import scrapy


class MovieSpider(scrapy.Spider):

    # name for crawl
    name = 'financial_data'

    # set spider settings
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    # iterate through pages to scrape from
    start_urls = []
    #start_urls = ['https://www.the-numbers.com/movie/budgets/all']

    for num in range(1, 5601, 100):
        start_urls.append(f'https://www.the-numbers.com/movie/budgets/all/{num}')

    # function to select distributor links from year webpage
    def parse(self, response):

        f = open('movie_list.csv', 'rU')
        text = f.readlines()
        f.close()

        movie_list = [s.rstrip('\n') for s in text]

        count = 0

        # iterate through movie links on page
        for href in response.xpath('//td/b/a/@href').extract():

            # check if movie is in movie_list
            if response.xpath('//td/b/a/text()').extract()[count] in movie_list:

                # complete full hyperlink
                main = 'https://www.the-numbers.com'
                url = main + href

                # call scrapy on movie
                yield scrapy.Request(url=url, callback=self.parse_movie, meta={'url': href})

            # increase count for each movie on page
            count += 1


    # function to select movie data from movie webpage
    def parse_movie(self, response):

        # moviepage url
        url = response.request.meta['url']


        # retrieve data from each movie page

        # movie title
        title = response.xpath('//h1/text()').extract()[0]

        # domestic gross
        dom_gross = response.xpath('//table[@id="movie_finances"]/tr/td/text()').extract()[0]

        # worldwide gross (total)
        intl_gross = response.xpath('//table[@id="movie_finances"]/tr/td/text()').extract()[2]

        # home disc sales
        disc_gross = response.xpath('//table[@id="movie_finances"]/tr/td/text()').extract()[5]

        # budget
        budget = response.xpath('//div[@id="summary"]/table/tr/td/text()').extract()[0]

        # release date
        release_date = response.xpath('//div[@id="summary"]/table/tr/td/text()').extract()[1]



        # yeild movie data values
        yield {
            'title': title,
            'budget': budget,
            'dom_gross': dom_gross,
            'intl_gross': intl_gross,
            'disc_gross': disc_gross,
            'release_date': release_date,
        }
