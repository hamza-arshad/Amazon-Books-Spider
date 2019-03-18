# -*- coding: utf-8 -*-
import scrapy
from ..items import BooksItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    start_urls = ['https://www.amazon.com/s?i=stripbooks&s=relevanceexprank&page=1&Adv-Srch-Books-Submit.x=37&Adv-Srch-Books-Submit.y=6&field-datemod=1&field-dateop=After&field-dateyear=2019&qid=1552770363&unfiltered=1']

    def parse(self, response):
        all_books = response.css('div.s-result-list>div')
        items = BooksItem()
        for book in all_books:
            title = book.css('.a-color-base.a-text-normal::text').extract_first()
            author = book.css('.a-color-secondary .a-size-base+ .a-size-base::text').extract_first()
            price = book.css('.a-spacing-top-small .a-price:nth-child(1) span::text').extract_first()
            image = book.css('.s-image::attr(src)').extract_first()

            if author is not None:
                author = author.strip()

            items['title'] = title
            items['author'] = author
            items['price'] = price
            items['image'] = image

            yield items

        next_page = response.css(".a-last a::attr(href)").extract_first()

        if next_page is not None:
            yield response.follow("https://www.amazon.com" + next_page, callback=self.parse)
