import scrapy 
import json

class dataFile(scrapy.Spider):
    name = 'draw'
    allowed_domains = ['zdnet.com']
    page_number = 2
    start_urls = ['https://www.zdnet.com/reviews/1/#reviews']

    def parse(self, response):
        for link in response.xpath("//article[@class='item']//h3/a/@href").getall():
            yield response.follow(link, callback = self.parse_categories)


        next_page = 'https://www.zdnet.com/reviews/' + str(dataFile.page_number) + '/#reviews'
        if dataFile.page_number <= 15:
            dataFile.page_number +=1
            yield response.follow(next_page, callback = self.parse)

    
    def parse_categories(self, response):
        try:
            data = response.xpath('//script[@type="application/ld+json"]/text()').getall()
            data1 = data[1]
            data1 = json.loads(data1)

            data0 = data[0]
            data0 = json.loads(data0)

            pros_link = response.xpath("//ul[@class='pros']//li//text()").getall()
            symbol = "\u2713"
            for pros in pros_link:
                if pros == symbol:
                    pros_link.remove(symbol)
            
            cons_link = response.xpath("//ul[@class='cons']//li//text()").getall()
            symbol2 = "\u2715"
            for cons in cons_link:
                if cons == symbol2:
                    cons_link.remove(symbol2)

            yield{
                'product name' : data1['name'],
                'product description' : data1['description'],
                'image url' : data1['image']['url'],
                'date published' : data1['image']['dateCreated'],
                'authors name' : data1['review']['author'][0]['name'],
                'review url' : data1['review']['url'],
                'category name' : data0['itemListElement'][1]['name'],
                'pros' : pros_link,
                'cons' : cons_link,
            }
        except KeyError:
            pass
        
