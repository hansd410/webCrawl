# -*- coding: utf-8 -*-
import re
import uuid
import scrapy
from scrapy.linkextractor import LinkExtractor
import w3lib.url

import argparse
import os

class GooglecloudSpider(scrapy.Spider):
	name = 'webMT'
	saveDir = ""
	allowed_domains = []
#	allowed_domains = ['cloud.google.com']
	
	def start_requests(self):
		self.saveDir = self.dir+"/"+self.folder
		self.allowed_domains.append(self.allowed)

		for mw in self.crawler.engine.scraper.spidermw.middlewares:
			if isinstance(mw, scrapy.spidermiddlewares.offsite.OffsiteMiddleware):
				mw.spider_opened(self)

		if not os.path.exists(self.saveDir):
			os.makedirs(self.saveDir)

		#start_urls = ['http://cloud.google.com', 'http://cloud.google.com/?hl=ko']
		start_urls = [self.url_en,self.url_ko]

		fid = str(uuid.uuid4())
		depth = 0
		#yield scrapy.Request(url=start_urls[1],callback=self.parse_once,meta={'filename':fid+"_ko",'depth':depth})
		yield scrapy.Request(url=start_urls[0],callback=self.parse,meta={'filename':fid,'depth':depth,'lang':'en'})
		depth = 0
		yield scrapy.Request(url=start_urls[1],callback=self.parse,meta={'filename':fid,'depth':depth,'lang':'ko'})

	def parse(self, response):
		links = LinkExtractor(canonicalize=True,unique=True).extract_links(response)

		fid = response.meta.get('filename')
		depth = response.meta.get('depth')
		lang= response.meta.get('lang')
		print (depth)
		if (depth <=int(self.depth)):
			flog = open(self.saveDir+"/log.txt",'a')
			if(lang=='en'):
				fout = open(self.saveDir+"/"+fid,'wb')
				flog.write("en\t"+response.url+"\n")
			else:
				fout = open(self.saveDir+"/"+fid+"_ko",'wb')
				flog.write("ko\t"+response.url+"\n")
			fout.write(str.encode(response.url+"\n"))
			fout.write(response.body)

			print("============ "+response.url+" done ==================")

			for link in links:
				fid = str(uuid.uuid4())
				# change url to korean!
				#link_ko=w3lib.url.add_or_replace_parameter(link.url,'hl','ko')
				#yield response.follow(link_ko,self.parse_once,meta={'filename':fid+"_ko"})
				depth = depth+1
				yield response.follow(link,self.parse,meta={'filename':fid,'depth':depth,'lang':lang})

	def parse_once(self, response):
		fid = response.meta.get('filename')
		fout = open(self.saveDir+"/"+fid,'wb')
		fout.write(str.encode(response.url+"\n"))
		fout.write(response.body)
		flog = open(self.saveDir+"/log.txt",'a')
		flog.write(response.url+"\n")

		print("============ "+response.url+" done ==================")
