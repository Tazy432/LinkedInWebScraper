# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# for easier storage and manipulation , we use items . 1 item is 1 job
class jobItem(scrapy.Item):
    job_url=scrapy.Field()
    job_title=scrapy.Field()
    job_company = scrapy.Field()
    job_nr_candidates = scrapy.Field()
    job_description=scrapy.Field()
    job_level=scrapy.Field()
    job_program_type=scrapy.Field()
    job_category = scrapy.Field()
    job_activity_sector=scrapy.Field()
