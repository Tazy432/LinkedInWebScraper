import scrapy

from linkedInJobScraper.items import jobItem

# Hello and welcome to the linkedInSpider . This spider's purpose is to return 25 jobs from LinkedIn
# ( keyword=Data , location ='Cluj-Napoca') as .json files in the LinkedInJobs.json file ,
#  and to save those records in a 'Jobs' MySql database . In my next project ill make one
# that can go over far more jobs , after discovering an hidden Api that allows me to iterate over jobs waay faster.It
# all started with :https://www.youtube.com/watch?v=mBoX_JCKZTE&t=6306s&ab_channel=freeCodeCamp.org

class LinkedinspiderSpider(scrapy.Spider):
    #the name of the spider
    name = "linkedInSpider"

    # the domains our spider is allowed to travel . we don't want to surf all over the internet by accessing links to
    # other websites posted on our targeted page
    allowed_domains = ["www.linkedin.com","ro.linkedin.com"]

    # the starting point (link/url) of the spider. Here is where our spider 'crawls' first time when running the program
    start_urls = ["https://www.linkedin.com/jobs/search?keywords=Data&location=Cluj-Napoca%2C%20Cluj%2C%20Rom%C3%A2nia&geoId=102471438&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"]

    # this is the first method that is triggered when enetering the command in the terminal:scrapy crawl linkedInSpider
    def parse(self, response):

        # this xpath selector is used to retrive all the links of the 25 jobs , on our starting page.
        # We need to acces those links in order to find more information about the job
        jobs_link_list = response.xpath(
            "//a[@class='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]']/@href").getall()

        # this for is used to iterate through all newly found links and open them , using the callback method
        # the links are accesed and 'parse_job_page' is now used to retrieve information from the page
        for job_link in jobs_link_list:
            yield response.follow(job_link, callback=self.parse_job_page)

    # this is the method that is triggered when accessing a job's webpage .
    # When accesed we simply scrape all the contect that we need and store it into a jobItem object, for easier storage.
    def parse_job_page(self ,response):
        job=jobItem()

        #here we save the info from a 'ul' tag that has a lot of usefull info ..
        # (job_level,job_program_type,job_category,job_activity_sector)
        detalii_job = response.xpath("//span[@class='description__job-criteria-text description__job-criteria-text--criteria']/text()").getall()

        # we retrive all the info directly from the webpage , and the array above
        job['job_url']=response.url
        job['job_title']=response.xpath("//h1[@class='top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title']/text()").get()
        job['job_company']=response.xpath("//a[@class='topcard__org-name-link topcard__flavor--black-link']/text()").get()
        job['job_nr_candidates']=response.xpath("//span[@class='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet']/text()").get()
        job['job_description']=response.xpath("//div[contains(@class, 'show-more-less-html__markup') and contains(@class, 'show-more-less-html__markup--clamp-after-5') and contains(@class, 'relative') and contains(@class, 'overflow-hidden')]").get()
        job['job_level']=detalii_job[0]
        job['job_program_type']=detalii_job[1]
        job['job_category']=detalii_job[2]
        job['job_activity_sector']=detalii_job[3]
        # we save all the fields in the job object
        yield job
