import scrapy


class MoviesSpider(scrapy.Spider):

    name = 'movies'
    start_urls = ['https://yts.mx/browse-movies']

    def parse(self, response, **kwargs):

        list_of_movies = response.css('div.browse-movie-wrap a::attr(href)').getall()
        yield from response.follow_all(list_of_movies, callback=self.parse_movie_details)

        next_page_url = response.css('ul.tsc_pagination li a:contains("Next")').get()
        if next_page_url:
            yield from response.follow_all(next_page_url, callback=self.parse)

    def parse_movie_details(self, response):

        yield {
            'movie_title': response.css('div.hidden-xs h1::text').get(),
            'release_year': response.css('div.hidden-xs h1 + h2::text').get(),
            'genre': response.css('div.hidden-xs h2 +h2::text').get(),
            'movie_rating': response.css('span[itemprop="ratingValue"]::text').get(),
            'plot_summary': response.css('#synopsis h3 + p::text').get(),
            'runtime': response.xpath('//span[@class="icon-clock"]//following-sibling::text()').get()
        }
