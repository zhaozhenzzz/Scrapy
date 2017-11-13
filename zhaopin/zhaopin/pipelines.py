# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from zhaopin import settings

class ZhaopinPipeline(object):
    def __init__(self, ):
        self.conn = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            use_unicode=False)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.insertData(item)
        return item

    def insertData(self, item):
        sql = "insert into shenzhen(jobname,salary,company_name,job_require,address,experience,company_size,head_count,education_require,release_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        params = (item['jobname'],item['salary'],item['comany_name'],item['job_require'],item['address'],item['experience'],item['comany_size'],item['head_count'],item['education_require'],item['release_date'])
        self.cursor.execute(sql, params)
        self.conn.commit()

        # sql = "insert into zhaopin(jobname, salary, address,company_name,experience,company_size,head_count,education_require,job_require,release_date) VALUES(%s, %s, %s, %s,%s,%s, %s, %s,%s,%s);"
        # params = (item['jobname'], item['salary'], item['address'],item['comany_name'],item['experience'], item['comany_size'], item['head_count'],item['education_require'],item['job_require'], item['release_date'])