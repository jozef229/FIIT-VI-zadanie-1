import scrapy


class CsfdSpider(scrapy.Spider):
    name = "csfd_spider"
    download_delay = 0.2
    allowed_domains = ['csfd.cz'] 
    start_urls = []
    # start_urls = ['https://www.csfd.cz/podrobne-vyhledavani/?type%5B%5D=0&genre%5Btype%5D=2&genre%5Binclude%5D%5B%5D=&genre%5Bexclude%5D%5B%5D=&origin%5Btype%5D=2&origin%5Binclude%5D%5B%5D=&origin%5Bexclude%5D%5B%5D=&year_from=2000&year_to=2000&rating_from=&rating_to=&actor=&director=&composer=&screenwriter=&author=&cinematographer=&production=&edit=&sound=&scenography=&mask=&costumes=&tag=&ok=Hledat&_form_=film']
    for i in range(1,21): 
            for j in range(2000,2020):  
                start_urls.append('https://www.csfd.cz/podrobne-vyhledavani/strana-' + str(i) + '/?type%5B0%5D=0&genre%5Btype%5D=2&genre%5Binclude%5D%5B0%5D=&genre%5Bexclude%5D%5B0%5D=&origin%5Btype%5D=2&origin%5Binclude%5D%5B0%5D=&origin%5Bexclude%5D%5B0%5D=&year_from=' + str(j) + '&year_to=' + str(j) + '&rating_from=&rating_to=&actor=&director=&composer=&screenwriter=&author=&cinematographer=&production=&edit=&sound=&scenography=&mask=&costumes=&tag=&ok=Hledat&_form_=film')
    
    def parse(self, response): 
        # film_url = 'https://www.csfd.cz/film/227786-interstellar/prehled/'
        # yield response.follow(film_url, callback=self.parse_film)
        SET_SELECTOR = '.name'
        for filmset in response.css(SET_SELECTOR):
            FILM_SELECTOR = 'a ::attr(href)'
            film_url = 'https://www.csfd.cz/' + filmset.css(FILM_SELECTOR).extract_first()
            yield response.follow(film_url, callback=self.parse_film)
       
    def parse_film(self, response):  
        
        film_length = ""
        administration = ''
        scenario = ''
        camera = ''
        music = ''
        actors = ''
        on_bluray = []
        on_dvd = []
        in_cinema = []  

        try:
            film_length = response.css('p.origin::text').extract()[1].replace(', ','').replace(' min','')
        except:
            print("An exception occurred") 

        array_content = response.xpath('//*[@id="plots"]/div[2]/ul/li[1]/div[1]/text()[2]').getall()
        for i, element in enumerate(array_content):
            array_content[i] = element.replace('\t','').replace('\n','')
 
        for i in range(10): 
            x1_name = response.xpath('//*[@class="creators"]/div[' + str(i+1) + ']/h4/text()').get() 
            if x1_name == 'Režie:':
                administration = response.xpath('//*[@class="creators"]/div[' + str(i+1) + ']/span[1]/a/text()').getall()
            if x1_name == 'Scénář:':
                scenario = response.xpath('//*[@class="creators"]/div[' + str(i+1) + ']/span[1]/a/text()').getall()
            if x1_name == 'Kamera:':
                camera = response.xpath('//*[@class="creators"]/div[' + str(i+1) + ']/span[1]/a/text()').getall()
            if x1_name == 'Hudba:':
                music = response.xpath('//*[@class="creators"]/div[' + str(i+1) + ']/span[1]/a/text()').getall()
            if x1_name == 'Hrají:':
                actors = response.xpath('//*[@class="creators"]/div[' + str(i+1) + ']/span[1]/a/text()').getall()
            pass 

        release_name = response.css('.ct-related th::text').getall()
        release_date = response.css('.ct-related .date ::text').getall()
        
        for i, element in enumerate(release_name):    
            release_name[i] = element.replace('\t','').replace('\n','') 

        alt_data = response.css('.ct-related th img').xpath('@alt').getall()
             
        for i, element in enumerate(release_date):  
            help_element = element.replace('\t','').replace('\n','').replace(' ', '#', 1)
            if release_name[i * 2 + 1] == 'V kinech od:': 
                in_cinema.append((alt_data[i] + '#' + help_element).split('#',2))  
            if release_name[i * 2 + 1] == 'Na DVD od:':
                on_dvd.append((alt_data[i] + '#' + help_element).split('#',2))  
            if release_name[i * 2 + 1] == 'Na Blu-ray od:':
                on_bluray.append((alt_data[i] + '#' + help_element).split('#',2))  
            pass

        yield {
            'film_name': response.css('h1::text').get().replace('\t','').replace('\n',''), 
            'film_genre': response.css('.genre::text').extract_first().split(' / '),
            'film_origin': response.css('.origin::text').extract_first().replace(', ','').split(' / '),
            'film_length': film_length, 
            'film_year': response.css('span[itemprop="dateCreated"]::text').get(), 
            'film_average': response.css('.average::text').get().replace('%',''),
            'film_director': response.css('span[itemprop="director"] a::text').getall(),
            'film_tags': response.css('div.tags a::text').getall(),
            'film_content': array_content,
            'film_administration': administration,
            'film_camera': camera,
            'film_scenario': scenario,
            'film_music': music,
            'film_actors': actors,
            'film_in_cinema': in_cinema,
            'film_on_dvd': on_dvd,
            'film_on_bluray': on_bluray
        }

 

        