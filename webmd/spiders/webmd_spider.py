from scrapy import Spider, Request
from webmd.items import WebmdItem
import re


class WebmdSpider(Spider):
    name = 'webmd_spider'
    allowed_urls = ['https://www.webmd.com']
    # start_urls = ['https://www.webmd.com/drugs/drugreview-64439-Abilify+oral.aspx?drugid=64439&drugname=Abilify+oral&pageIndex=0&sortby=3&conditionFilter=-1']
    start_urls = ['https://www.webmd.com/drugs/2/index']

    def parse(self,response):
        result_urls = response.xpath('//*[@id="ContentPane30"]/div[2]/ul/li/a[2]/@href').extract()
        for half_url in result_urls:
            url = 'https://www.webmd.com' + half_url + '&pageIndex=0&sortby=3&conditionFilter=-1'
            yield Request(url = url, callback = self.parse_result_pages, meta = {'u':url}, dont_filter = True)

    def parse_result_pages(self, response):
        beginningUrl = response.meta['u']
        newUrls = re.sub('&pageIndex=0&sortby=3&conditionFilter=-1','', beginningUrl)
        text = response.xpath('//*[@id="ratings_fmt"]/div[3]/div[2]/text()').extract_first()
        num_reviews = int(re.findall('\d+', text)[-1])
        if (num_reviews % 5 == 0):
            num_pages = num_reviews // 5
        else:
            num_pages = num_reviews // 5 + 1
        review_urls = [newUrls + '&pageIndex={}&sortby=3&conditionFilter=-1'.format(i) for i in range(num_pages+1)]
        for url in review_urls:
            yield Request(url = url, callback = self.parse_review_pages)

    def parse_review_pages(self, response):
        drugFullText = response.xpath('//*[@id="header"]/div/h1/text()').extract_first()
        drug = re.sub('User Reviews & Ratings - ', '', drugFullText)

        conditions = response.xpath('//*[@id="ratings_fmt"]/div/div[1]/div[1]/text()').extract()
        for i in range(len(conditions)):
            div_num = str(4 + i)

            conditionFullText = response.xpath('//*[@id="ratings_fmt"]/div[' + div_num + ']/div[1]/div[1]/text()').extract_first().strip()
            condition = re.sub("Condition: ", "", conditionFullText)
            
            effectiveR = response.xpath('//*[@id="ratings_fmt"]/div[' + div_num + ']/div[2]/div[1]/p[2]/span/text()').extract_first().strip()
            effectiveness = int(re.findall('\d+', effectiveR)[0])

            easeR = response.xpath('//*[@id="ratings_fmt"]/div[' + div_num + ']/div[2]/div[2]/p[2]/span/text()').extract_first().strip()
            easeOfUse = int(re.findall('\d+', easeR)[0])

            satisR = response.xpath('//*[@id="ratings_fmt"]/div[' + div_num + ']/div[2]/div[3]/p[2]/span/text()').extract_first().strip()
            satisfaction = int(re.findall('\d+', satisR)[0])
            
            commentField = response.xpath('//*[@id="comFull' + str(i + 1) + '"]/text()').extract()
            if (commentField == []):
                comment = ''
            else:
                comment = commentField[0]

            dateAndTime = response.xpath('//*[@id="ratings_fmt"]/div[' + div_num + ']/div[1]/div[2]/text()').extract_first()
            date = re.findall('\d+/\d+/\d+',dateAndTime)[0]
            
            reviewerInfo = response.xpath('//*[@id="ratings_fmt"]/div[' + div_num + ']/p[1]/text()').extract_first()
            if (re.findall('\d+\s\w+ale', reviewerInfo) == []):
                sex = ""
            else:
                s = re.findall('\d+\s\w+ale', reviewerInfo)[0]
                sex = re.findall('\D+',s)[0].strip()

            if (re.findall('\d+-\d+', reviewerInfo) == []):
                age = ""
            else:
                age = re.findall('\d+-\d+', reviewerInfo)[0]

            if (re.findall('Treatment for [\w\s]+',reviewerInfo) == []):
                timeUsed = ""
            else:
                treatmentFor = re.findall('Treatment for [\w\s]+',reviewerInfo)[0].strip()
                timeUsed = re.sub('Treatment for ', '', treatmentFor)
            
            item = WebmdItem()
            item['drug'] = drug
            item['condition'] = condition
            item['effectiveness'] = effectiveness
            item['easeOfUse'] = easeOfUse
            item['satisfaction'] = satisfaction
            item['comment'] = comment
            item['date'] = date
            item['sex'] = sex
            item['age'] = age
            item['timeUsed'] = timeUsed
            yield item

            print(condition)
            print(effectiveness)
            print(easeOfUse)
            print(satisfaction)
            print(comment)
            print(date)
            print(sex)
            print(age)
            print(timeUsed)
            print('-' * 50)

            

        # conditions = response.xpath('//*[@id="ratings_fmt"]/div/div[1]/div[1]/text()').extract()
        # effective = response.xpath('//*[@id="ratings_fmt"]/div/div[2]/div[1]/p[2]/span/text()').extract()
        # ease = response.xpath('//*[@id="ratings_fmt"]/div/div[2]/div[2]/p[2]/span/text()').extract()
        # sat = response.xpath('//*[@id="ratings_fmt"]/div/div[2]/div[3]/p[2]/span/text()').extract()
        # comments = response.xpath('//*[@id="ratings_fmt"]/div/p[3]/text()').extract()
        # dAndt = response.xpath('//*[@id="ratings_fmt"]/div/div[1]/div[2]/text()').extract()
        # reviewers = response.xpath('//*[@id="ratings_fmt"]/div/p[1]/text()').extract()

        # for i in range(len(conditions)):
        #     item = WebmdItem()

        #     conditionFullText = conditions[i]
        #     condition = re.sub("Condition: ", "", conditionFullText).strip()
            
        #     effectiveR = effective[i]
        #     effectiveness = int(re.findall('\d+', effectiveR)[0])

        #     easeU = ease[i]
        #     easeOfUse = int(re.findall('\d+', easeU)[0])

        #     satisR = sat[i]
        #     satisfaction = int(re.findall('\d+', satisR)[0])

        #     comment = comments[i]

        #     dateAndTime = dAndt[i]
        #     date = re.findall('\d+/\d+/\d+',dateAndTime)[0]

        #     reviewerInfo = reviewers[i]
        #     if (re.findall('\d+\s\w+ale', reviewerInfo) == []):
        #         sex = ""
        #     else:
        #         s = re.findall('\d+\s\w+ale', reviewerInfo)[0]
        #         sex = re.findall('\D+',s)[0].strip()

        #     if (re.findall('\d+-\d+', reviewerInfo) == []):
        #         age = ""
        #     else:
        #         age = re.findall('\d+-\d+', reviewerInfo)[0]

        #     if (re.findall('Treatment for [\w\s]+',reviewerInfo) == []):
        #         timeUsed = ""
        #     else:
        #         treatmentFor = re.findall('Treatment for [\w\s]+',reviewerInfo)[0].strip()
        #         timeUsed = re.sub('Treatment for ', '', treatmentFor)

        #     print(condition)
        #     print(effectiveness)
        #     print(easeOfUse)
        #     print(satisfaction)
        #     print(comment)
        #     print(date)
        #     print(sex)
        #     print(age)
        #     print(timeUsed)
        #     print('*' * 50)

        print('\n\n')
        print('*' * 50)
        print('\n\n')