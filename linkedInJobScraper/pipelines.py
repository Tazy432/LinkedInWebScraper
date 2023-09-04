# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import re
from bs4 import BeautifulSoup
import mysql.connector


class LinkedinjobscraperPipeline:
    def process_item(self, item, spider):
        # Cleaning all the data's  fields ( get rid of the white spaces ),
        # except the description part where white spaces are needed.
        # ex:          Hello friend           -->Hello friend
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for fieldName in field_names:
            if fieldName != 'job_description':
                value = adapter.get(fieldName)
                if value is not None:
                    adapter[fieldName] = value.strip()
        # Cleaning the data for job_nr_candidates item field.
        # ex:154 participants-->154
        nrCandidates = adapter.get('job_nr_candidates')
        if nrCandidates is not None:
            match = re.search(r'^\d+', nrCandidates)
            if match:
                first_digits = match.group(0)
                adapter['job_nr_candidates'] = first_digits
            else:
                adapter['job_nr_candidates'] = 0
        else:
            adapter['job_nr_candidates'] = 0
        # Cleaning the job_description field .It is still in a html form ,
        # so we can clean it easily with bs4
        soup = BeautifulSoup(adapter['job_description'], 'html.parser')
        plain_text = soup.get_text()
        adapter['job_description']=plain_text
        return item


import mysql.connector
# this class is used to place items into the database . It creates the table if nonexistent , and then adds the item
# a database is required !!! . See down below 'database='Jobs''
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='Jobs'
        )
        # a cursor is needed to execute the commands
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id int NOT NULL auto_increment,
            job_url VARCHAR(800),
            job_title VARCHAR(300),
            job_company VARCHAR(300),
            job_nr_candidates INTEGER,
            job_description TEXT,
            job_level VARCHAR(300),
            job_program_type VARCHAR(300),
            job_category VARCHAR(300),
            job_activity_sector VARCHAR(300),
            PRIMARY KEY (id)
        )
        """)
    # a method designed to add items to the database
    def process_item(self, item, spider):
        # Define the insert statement
        self.cur.execute("""
        INSERT INTO jobs (
            job_url,
            job_title,
            job_company,
            job_nr_candidates,
            job_description,
            job_level,
            job_program_type,
            job_category,
            job_activity_sector
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )""", (
            item["job_url"],
            item["job_title"],
            item["job_company"],
            item["job_nr_candidates"],
            item["job_description"],
            item["job_level"],
            item["job_program_type"],
            item["job_category"],
            item["job_activity_sector"]
        ))

        self.conn.commit()
        return item
    # when the spider closes , the connection and cursor are closed . No need to waste precious memory
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
