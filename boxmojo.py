import scrapy
class FirstSpider(scrapy.Spider):
    name = 'Movie_Scrape'

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }
    # All the yearly charts
    start_urls = ['http://www.boxofficemojo.com/yearly/chart/?yr=' + str(x) + '&p=.htm' for x in range(1980,2018)]

    def parse(self, response):
        yield scrapy.Request(
                url = response.request.url,
                callback = self.parse_page,
                meta = {'url':response.request.url}
                )
        #nextLinks corresponds to 1-100,101-200, 201-300, etc..
        nextLinks = response.xpath('//div[@id="body"]/table[3]/tr/td/center[2]/font/b//a/@href').extract()
        for i in range(len(nextLinks)):
            yield scrapy.Request(
                    url = 'http://www.boxofficemojo.com' + nextLinks[i],
                    callback = self.parse_page,
                    meta = {'url': 'http://www.boxofficemojo.com' + nextLinks[i]}
            )
        #This parses a page of movie titles.
    def parse_page(self, response):
        movieLinks = response.xpath('//div[@id="body"]/table[3]//table//table//b//a/@href').extract()
        movieNames = response.xpath('//div[@id="body"]/table[3]//table//table//b//a/text()').extract()
        for i in range(len(movieLinks)):
            yield scrapy.Request(
                    url = 'http://www.boxofficemojo.com' + movieLinks[i],
                    callback = self.parse_movie,
                    meta = {'url': 'http://www.boxofficemojo.com' + movieLinks[i], 'name': movieNames[i]}
                    )
        #This parses a movie pages
    def parse_movie(self, response):
        name = response.request.meta['name']
        url = response.request.meta['url']
        theats = (response.xpath('//div[@class="mp_box_content"]//td//*[contains(text(),"theaters")]//text()').extract())
        box1 = (response.xpath('//div[@class="mp_box_content"]//td//text()').extract())
        b = response.xpath('//div[@id="body"]//table//table//tr//tr//table//td//text()').extract()
        boxInfo = response.xpath('//div[@class="mp_box_content"]//font[@size="2"]//text()').extract()
        try:
            totalDomesticGross = b[b.index('Domestic Total Gross: ') + 1]
        except(ValueError, IndexError):
            totalDomesticGross = 'Missing'
        try:
            noTheaters = (''.join(theats[0].split(' theaters')[0].split(' ')[-1].split(',')))
        except(IndexError):
            noTheaters = 'NaN'
        try:
            avOpGrossPTheater = (''.join(theats[0].split(' average')[0].split('$')[-1].split(',')))
        except(IndexError):
            avOpGrossPTheater = 'NaN'
        try:
            OpGross = ''.join((''.join(box1).split('Weekend:')[1].split('$')[1].split('\n')[0].split(',')))
        except(ValueError, IndexError):
            OpGross = 'NaN'
        try:
            Genre = b[b.index('Genre: ') + 1]
        except(ValueError, IndexError):
            Genre = 'Missing'
        try:
            Rating = b[b.index('MPAA Rating: ') + 1]
        except(ValueError, IndexError):
            Rating = 'Missing'
        try:
            Distributor = b[b.index('Distributor: ') + 1]
        except(ValueError, IndexError):
            Distributor = 'Missing'
        try:
            ReleaseDate = b[b.index('Release Date: ') + 1]
        except(ValueError, IndexError):
            ReleaseDate = 'Missing'
        try:
            RunTime = b[b.index('Runtime: ') + 1]
        except(ValueError, IndexError):
            RunTime = 'Missing'
        try:
            Budget = b[b.index('Production Budget: ') + 1]
        except(ValueError, IndexError):
            Budget = 'Missing'
        try:
            director = boxInfo[boxInfo.index('Director:') + 1]
        except(ValueError, IndexError):
            director = 'Missing'
        try:
            writer = boxInfo[boxInfo.index('Writer:') + 1]
        except(ValueError, IndexError):
            writer = 'Missing'
        try:
            actor = boxInfo[boxInfo.index('Actors:') + 1]
        except(ValueError, IndexError):
            actor = 'Missing'
        try:
            composer = boxInfo[boxInfo.index('Composer:') + 1]
        except(ValueError, IndexError):
            composer = 'Missing'
        yield {
            'url': url,
            'name': name,
            'totalDomesticGross': totalDomesticGross,
            'noTheaters': noTheaters,
            'avOpGrossPTheater': avOpGrossPTheater,
            'OpGross': OpGross,
            'Genre': Genre,
            'Rating': Rating,
            'Distributor': Distributor,
            'ReleaseDate': ReleaseDate,
            'RunTime': RunTime,
            'Budget': Budget,
            'director': director,
            'writer': writer,
            'actor': actor,
            'composer': composer
        }
        
        
        
        
        