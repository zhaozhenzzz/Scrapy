


from zhaopin.items import ZhaopinItem
from scrapy import Spider,Request
from bs4 import BeautifulSoup
import  re
class ZhaopinSpider(Spider):
    name = 'zhaopin'

    allowed_domains = ['www.zhaopin.com']
    start_urls = ['http://www.zhaopin.com/']
    #start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7&kw=java%E5%B7%A5%E7%A8%8B%E5%B8%88&sm=0&sg=720f662a0e894031b9b072246ac2f919&p=1']

    def start_requests(self):
        #for num in (1,60):
        url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=java%E5%B7%A5%E7%A8%8B%E5%B8%88&sm=0&isadv=0&sg=cc9fe709f8cc4139afe2ad0808eb7983&p=42'
            #.format(num)
        #yield Request(url,callback=self.parse)
        yield Request(url,callback=self.parse)

    def parse(self, response):
        #self.log('page url is ' + response.url)
        wbdata = response.text
        soup = BeautifulSoup(wbdata, 'lxml')
        job_name = soup.select("table.newlist > tr > td.zwmc > div > a:nth-of-type(1)")
        salary = soup.select("table.newlist > tr > td.zwyx")
        #company_name = soup.select("table.newlist > tr > td.gsmc > div > a:nth-of-type(2)")
        times = soup.select("table.newlist > tr > td.gxsj > span")
        for name,salary,time in zip(job_name,salary,times):
            item = ZhaopinItem()
            item["jobname"] = name.get_text()
            url= name.get('href')
            #print("职位"+name.get_text()+"工资"+salary.get_text()+"发布日期"+time.get_text()+"连接"+url)
            item["salary"] = salary.get_text()
            item["release_date"] = time.get_text()
            # item["comany_name"] = company     _name.get_text()
            #yield item

            yield Request(url=url, meta={"item": item}, callback=self.parse_moive,dont_filter=True)



    def parse_moive(self, response):
        #item = ZhaopinItem()
        jobdata = response.body
        require_data = response.xpath(
            '//body/div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]/p').extract()
        require_data_middle = ''
        for i in require_data:
            i_middle = re.sub(r'<.*?>', r'', i, re.S)
            require_data_middle = require_data_middle + re.sub(r'\s*', r'', i_middle, re.S)
        jobsoup = BeautifulSoup(jobdata, 'lxml')
        item = response.meta['item']
        item['job_require'] = require_data_middle
        item['experience'] = jobsoup.select('div.terminalpage-left strong')[4].text.strip()
        item['comany_name']  = jobsoup.select('div.fixed-inner-box h2')[0].text
        item['comany_size']  = jobsoup.select('ul.terminal-ul.clearfix li strong')[8].text.strip()
        item['head_count']  = jobsoup.select('div.terminalpage-left strong')[6].text.strip()
        item['address'] = jobsoup.select('ul.terminal-ul.clearfix li strong')[11].text.strip()
        item['education_require'] = jobsoup.select('div.terminalpage-left strong')[5].text.strip()
        yield item