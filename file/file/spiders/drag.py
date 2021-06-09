import scrapy 
import json

class dataFile(scrapy.Spider):
    name = 'draw'
    allowed_domains = ['zdnet.com']
    page_number = 2
    start_urls = ['https://www.zdnet.com/reviews/1/#reviews']

    def parse(self, response):
        start = 'https://www.zdnet.com'
        for link in response.xpath("//article[@class='item']//h3/a/@href").getall():
            a = start + link
            yield response.follow(a, callback = self.parse_categories)


        next_page = 'https://www.zdnet.com/reviews/' + str(dataFile.page_number) + '/#reviews'
        if dataFile.page_number <= 442:
            dataFile.page_number +=1
            yield response.follow(next_page, callback = self.parse)


    def parse_categories(self, response):
        data = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        data1 = data[1]
        data1 = json.loads(data1)
        
        yield{
            'product name' : data1['name'],
            'product description' : data1['description'],
            'image url' : data1['image']['url'],
            'date published' : data1['image']['dateCreated'],
            'authors name' : data1['review']['author'][0]['name'],
            'review url' : data1['review']['url'],
        }

        
