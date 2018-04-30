# script to collect movie data from boxofficemojo

import scrapy


class MovieSpider(scrapy.Spider):

    # name for crawl
    name = 'movie_data'

    # set spider settings
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    # start scraping at studios list page for each year
    start_urls = []

    for year in range(2008, 2018):
        start_urls.append(f'http://www.boxofficemojo.com/studio/?view=company&view2=yearly&yr={year}&p=.htm')


    # function to select distributor links from year webpage
    def parse(self, response):

        # iterate through each studio link
        for href in response.xpath('//a[starts-with(@href, "/studio/chart")]/@href').extract():

            # complete full hyperlink
            main = 'http://www.boxofficemojo.com'
            url = main + href

            # call scrapy on each distributor
            yield scrapy.Request(url=url, callback=self.parse_distro, meta={'url': href})


    # function to select movie links from distributor webpage
    def parse_distro(self, response):

        # iterate through each movie link
        for href in response.xpath('//font[@size="2"]/a[starts-with(@href, "/movies/?id")]/@href').extract():

            # complete full hyperlink
            main = 'http://www.boxofficemojo.com'
            url = main + href

            # call scrapy on each movie
            yield scrapy.Request(url=url, callback=self.parse_movie, meta={'url': href})


    # function to retrieve movie data from movie webpage
    def parse_movie(self, response):

        # moviepage url
        url = response.request.meta['url']


        # retrieve data from each movie page

        # movie title
        title = response.xpath('//font[@face="Verdana"]/b/text()').extract()

        # domestic gross
        dom_gross = response.xpath('//font[@size="4"]/b/text()').extract()[0]

        # distributor
        distributor = response.xpath('//td[@valign="top"]/b/a/text()').extract()[0]

        # release date
        release_date = response.xpath('//td[@valign="top"]/b/nobr/a/text()').extract()[0]

        # genre
        genre = response.xpath('//td[@valign="top"]/b/text()').extract()[0]

        # runtime
        runtime = response.xpath('//td[@valign="top"]/b/text()').extract()[1]

        # mpaa rating
        mpaa_rating = response.xpath('//td[@valign="top"]/b/text()').extract()[2]

        # budget
        budget = response.xpath('//td[@valign="top"]/b/text()').extract()[3]

        # worldwide gross
        intl_gross = response.xpath('//td[@width="35%"]/b/text()').extract()[1]

        # number of theaters
        num_theaters = response.xpath('//div[@class="mp_box_content"]/table/tr/td[contains(text(), "Widest")]/following-sibling::td/text()').extract()

        # days in release
        num_days = response.xpath('//div[@class="mp_box_content"]/table/tr/td[contains(text(), "In Release")]/following-sibling::td/text()').extract()

        # director
        director = response.xpath('//a[starts-with(@href, "/people/chart/?view=Director")]/text()').extract()

        # actors
        actors = response.xpath('//a[starts-with(@href, "/people/chart/?view=Actor")]/text()').extract()


        # yeild movie data values
        yield {
            'title': title,
            'distributor': distributor,
            'dom_gross': dom_gross,
            'intl_gross': intl_gross,
            'release_date': release_date,
            'genre': genre,
            'runtime': runtime,
            'mpaa_rating': mpaa_rating,
            'budget': budget,
            'num_theaters': num_theaters,
            'num_days': num_days,
            'director': director,
            'actors': actors
        }
