# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from test_2.items import Test2Item
def change_num(strs):
    '''
    对页面上的乱码加密解密
    :param strs:
    :return:
    '''
    num_dic = {
        '麣': '2',
        '驋': '1',
        '齤': '9',
        '閏': '0',
        '餼': '7',
        '鑶': '8',
        '龥': '5',
        '龒': '4',
        '龤': '3',
        '鸺': '6',
    }
    change_str = str(strs).strip().replace('麣', num_dic['麣']).replace('驋', num_dic['驋']).replace('齤',
                                                                                                 num_dic['齤']).replace(
        '閏', num_dic['閏']).replace('餼', num_dic['餼']).replace('鑶', num_dic['鑶']).replace('龥', num_dic['龥']).replace('龒',
                                                                                                                    num_dic[
                                                                                                                        '龒']).replace(
        '鸺', num_dic['鸺']).replace('龤', num_dic['龤'])
    return change_str

class TestSpider(RedisCrawlSpider):
    name = 'test'
    # allowed_domains = ['https://bj.58.com/chuzu/']
    # start_urls = ['https://bj.58.com/chuzu/']
    redis_key = 'chuzu'
    link = LinkExtractor(allow=r'/pn\d+/')
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        rent_type = '无'
        rent_title = '无'
        house_type = '无'
        house_size = '无'
        money = '无'
        li_list = response.xpath('//ul[@class="listUl"]/li')
        # div_list = response.xpath('//div[@class="des"]')
        # money_list = response.xpath('//div[@class="listliright"]')
        # print(money_list)
        # print(div_list.extract())
        for li in li_list:
            money = li.xpath('./div[@class="listliright"]/div[@class="money"]/b/text()').extract_first()
            money = change_num(money)
            title = li.xpath('./div[@class="des"]/h2/a/text()').extract_first()
            title = change_num(title)
            type = li.xpath("./div[@class='des']/p[@class='room strongbox']/text()").extract_first()
            type = change_num(type)
            try:
                house_type = type.replace(' ', ',').split(',')[0]
                house_size = type.replace(' ', ',').split(',')[-1].strip()
                rent_type = title.split('|')[0]
                rent_title = title.split('|')[1]
            except Exception as e:
                pass
            item = Test2Item()
            item['rent_type'] = rent_type
            item['rent_title'] = rent_title
            item['house_type'] = house_type
            item['house_size'] = house_size
            item['money'] = money
            # print(money)
            yield item
