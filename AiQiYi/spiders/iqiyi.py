# -*- coding: utf-8 -*-
import scrapy
from AiQiYi.items import AiqiyiItem
import re
import time

class IqiyiSpider(scrapy.Spider):
    name = 'iqiyi'
    allowed_domains = ['https://www.iqiyi.com']
    start_urls = ['http://so.iqiyi.com/so/q_决战中途岛']

    def clear_html_re(src_html):
        '''
        正则清除HTML标签
        :param src_html:原文本
        :return: 清除后的文本
        '''
        content = re.sub(r"</?(.+?)>", "", src_html)  # 去除标签
        # content = re.sub(r"&nbsp;", "", content)
        dst_html = re.sub(r"\s+", "", content)  # 去除空白字符
        return dst_html

    def parse(self, response):
        item = AiqiyiItem()

        print('【开始解析】')
        category_name = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/h3/span/text()').extract()[0]

        print(category_name)
        # 解析标题 "
        title = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/h3/a/@title').extract()[0]
        print(title)
        img_url = 'http:' + response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div/div/a/img/@src').extract()[0]
        print(img_url)
        desc = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[5]/span/text()').extract()[0]
        # desc = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[4]/span/text()').extract()[0]
        # desc = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[3]/span/text()').extract()[0]
        print(desc)

        # 解析作者
        authorList = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]')
        for author in authorList:
            author_name_arr = author.xpath(
                '//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/a/@title').extract()

        author_name_string = ''
        for author_name in author_name_arr:
            author_name_string = author_name_string + author_name + ' '

        print(author_name_string)

        # 解析发布时间
        publish_time = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/h3/em/text()').extract()[0]
        publish_time = publish_time + "-01-01 00:00:00"
        print(publish_time)

        if category_name == '电影':
            seriesArr = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[6]/div/span/a/@href').extract()[0]
            print(category_name)
            print(seriesArr)
        else:

            # 解析剧集
            # seriesList = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[4]/div/ul[2]/li')
            seriesList = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[5]/div/ul[2]/li')
            # seriesList = response.xpath('//*[@id="j-body"]/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[4]/div/ul[1]/li')
            print(seriesList)

            seriesArr = []
            i = 0
            for series in seriesList:
                i = i + 1

                # series_num = series.xpath("//*[@id='j-body']/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[4]/div/ul[2]/li["+str(i)+"]/a/text()").re("([\d]+)")[0]
                # series_url = series.xpath("//*[@id='j-body']/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[4]/div/ul[2]/li["+str(i)+"]/a/@href").extract()[0]

                series_num = series.xpath("//*[@id='j-body']/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[5]/div/ul[2]/li[" + str(i) + "]/a/text()").re("([\d]+)")[0]
                series_url = series.xpath("//*[@id='j-body']/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[5]/div/ul[2]/li[" + str(i) + "]/a/@href").extract()[0]

                #
                # series_num = series.xpath("//*[@id='j-body']/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[4]/div/ul[1]/li[" + str(i) + "]/a/text()").re("([\d]+)")[0]
                # series_url = series.xpath("//*[@id='j-body']/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[4]/div/ul[1]/li[" + str(i) + "]/a/@href").extract()[0]
                result = 'http' in series_url
                if result:
                    seriesArr.append([series_num, series_url])


        print("整理数据")
        if title and img_url and author_name_string and desc and publish_time and seriesArr:
            print('数据 【完整】')

            item['category_name'] = category_name
            item['title'] = title
            item['img_url'] = img_url
            item['author_name'] = author_name_string
            item['desc'] = desc
            item['publish_time'] = publish_time
            item['series'] = seriesArr
        else:
            print('数据 【不完整】')
            print('category_name')
            print(category_name)
            print('title')
            print(title)
            print('img_url')
            print(img_url)
            print('author_name')
            print(author_name)
            print('desc')
            print(desc)
            print('publish_time')
            print(publish_time)
            print('series')
            print(seriesArr)

            if category_name is None:
                print('category_name is None')

            if title is None:
                print('title is None')

            if img_url is None:
                print('img_url is None')

            if author_name_string is None:
                print('author_name_string is None')

            if desc is None:
                print('desc is None')

            if publish_time is None:
                print('publish_time is None')

            if seriesArr is None:
                print('seriesArr is None')


        return item

