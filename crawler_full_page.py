import scrapy

numberpage = 0


class CsfdSpiderFull(scrapy.Spider):
    name = "csfd_spider_full"
    download_delay = 1.2
    allowed_domains = ['csfd.cz']
    start_urls = []
    for i in range(1, 21):
        for j in range(2000, 2013):
            start_urls.append('https://www.csfd.cz/podrobne-vyhledavani/strana-' + str(i) + '/?type%5B0%5D=0&genre%5Btype%5D=2&genre%5Binclude%5D%5B0%5D=&genre%5Bexclude%5D%5B0%5D=&origin%5Btype%5D=2&origin%5Binclude%5D%5B0%5D=&origin%5Bexclude%5D%5B0%5D=&year_from=' +
                              str(j) + '&year_to=' + str(j) + '&rating_from=&rating_to=&actor=&director=&composer=&screenwriter=&author=&cinematographer=&production=&edit=&sound=&scenography=&mask=&costumes=&tag=&ok=Hledat&_form_=film')

    def parse(self, response):
        SET_SELECTOR = '.name'
        for filmset in response.css(SET_SELECTOR):
            FILM_SELECTOR = 'a ::attr(href)'
            film_url = 'https://www.csfd.cz/' + \
                filmset.css(FILM_SELECTOR).extract_first()
            yield response.follow(film_url, callback=self.parse_film)

    def parse_film(self, response):
        global numberpage
        numberpage = numberpage + 1
        page = str(numberpage)
        filename = 'page-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
