from scrapy import Request
from scrapy import Spider
from scrapy.selector import Selector
from test1.items import Test1Item
from urllib.parse import urljoin
import re


class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["www.goodreads.com"]
    start_urls = [
        "https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=1&per_page=30",
    ]

    def parse(self, response):
        books = Selector(response).xpath(
            "//*[contains(@class , 'bookTitle')]/@href").extract()
        for book in books:
            book_id = re.search('/book/show/(.+?)-', book)
            if book_id:
                book_id = book_id.group(1)

            url = urljoin(response.url, book)
            yield Request(url, callback=self.parse_info, meta={'book_id': book_id, 'link': url})

    def parse_info(self, response):
        info = Selector(response).xpath('//div[@class="last col"]')
        reviews = Selector(response).xpath(
            '//div[@id="bookReviews"]/div[@class="friendReviews elementListBrown"]')

        item = Test1Item()
        item['book_id'] = response.meta['book_id']
        item['link'] = response.meta['link']
        item['Title'] = info.xpath(
            'h1[@class="gr-h1 gr-h1--serif"]/text()').extract_first().strip()
        item['Author'] = info.xpath(
            'div[@id="bookAuthors"]/span/div/a/span/text()').extract_first()
        item['Rate'] = info.xpath(
            'div[@class="uitext stacked"]/span[@itemprop="ratingValue"]/text()').extract_first().strip()
        item['Description'] = info.xpath(
            'div[@id="descriptionContainer"]/div[@class="readable stacked"]/span/text()').extract_first()

        comments = []

        for review in reviews:
            name = review.xpath(
                'div/div/div/div[@class="reviewHeader uitext stacked"]/span/a[@class="user"]/text()').extract_first()

            get_user_id = review.xpath(
                'div/div/div/div[@class="reviewHeader uitext stacked"]/span/a[@class="user"]/@href').extract_first()
            user_id = get_user_id[11:19]

            rate = len(review.xpath(
                'div/div/div/div[@class="reviewHeader uitext stacked"]/span[@class=" staticStars notranslate"]/span[@class="staticStar p10"]'))

            date = review.xpath(
                'div/div/div/div/a[@class="reviewDate createdAt right"]/text()').extract_first()

            review_content = review.xpath(
                'div/div/div/div[@class="reviewText stacked"]/span/span/text()').extract_first()

            comments.append({'ID User': user_id,
                             'Name User': name,
                             'Rate': rate,
                             'Review content': review_content,
                             'Date post': date,
                             })
        item['Reviews'] = comments

        yield item

    def get_comment(self, response):
        comments = Selector(response).xpath(
            '//div[@id="comment_list"]/div[@class="comment u-anchorTarget"]')
        list_comment = []
        for comment in comments:
            info_comment = comment.xpath(
                '//div[@class="mediumText reviewText"]//text()').extract()
            for element in info_comment:
                if len(element.strip()):
                    list_comment.append(element.strip())
        yield {
            "List comments": list_comment
        }
