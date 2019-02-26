# -*- coding: utf-8 -*-
import re
import uuid
import scrapy
from scrapy.linkextractor import LinkExtractor
import w3lib.url

class GooglecloudSpider(scrapy.Spider):
	name = 'googleCloud2'
	allowed_domains = ['cloud.google.com']
	
	def start_requests(self):
		start_urls = ['http://cloud.google.com',
					'http://cloud.google.com/?hl=ko',
					]
		fid = str(uuid.uuid4())
		depth = 0
		yield scrapy.Request(url=start_urls[1],callback=self.parse_once,meta={'filename':fid+"_ko",'depth':depth})
		yield scrapy.Request(url=start_urls[0],callback=self.parse,meta={'filename':fid,'depth':depth})

	def parse(self, response):
		#links = response.css('a::attr(href)').getall())
		links = LinkExtractor(canonicalize=True,unique=True).extract_links(response)

		fid = response.meta.get('filename')
		depth = response.meta.get('depth')+1
		print("depth : "+str(depth))
		if (depth <=4):
			fout = open("../data/crawled/"+fid,'wb')
			fout.write(str.encode(response.url+"\n"))
			fout.write(response.body)
			print("============ "+response.url+" done ==================")

			for link in links:
				fid = str(uuid.uuid4())
				# change url to korean!
				link_ko=w3lib.url.add_or_replace_parameter(link.url,'hl','ko')

				yield response.follow(link_ko,self.parse_once,meta={'filename':fid+"_ko"})
				yield response.follow(link,self.parse,meta={'filename':fid,'depth':depth})

	def parse_once(self, response):
		#links = response.css('a::attr(href)').getall())
		fid = response.meta.get('filename')
		fout = open("../data/crawled/"+fid,'wb')
		fout.write(str.encode(response.url+"\n"))
		fout.write(response.body)
		print("============ "+response.url+" done ==================")
