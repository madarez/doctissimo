# -*- coding: utf-8 -*-
#!/usr/bin/env python3

#out=response.xpath("//body/div[@id='container']/div[@class='containerforum']/div[@class='content-du-forum']/div[@style='padding-right: 5px;']/div[@align='left']/a/@href").extract()

"""
Created on Fri Sep 22 22:45:42 2017

@author: rez
"""

'''

'''


import scrapy
import uuid
import re
from lxml import etree

class DoctissimoSpider(scrapy.Spider):
    name = "docSpidy"
    
    def start_requests(self):
        #page = 'http://forum.doctissimo.fr/psychologie/couples-relations/parents-veulent-vacances-sujet_252475_1.htm'

        forums = ['http://forum.doctissimo.fr/top_topics/grossesse-bebe/',
                   'http://forum.doctissimo.fr/top_topics/mode/',
                   'http://forum.doctissimo.fr/top_topics/forme-beaute/',
                   'http://forum.doctissimo.fr/top_topics/nutrition/',
                   'http://forum.doctissimo.fr/top_topics/psychologie/',
                   'http://forum.doctissimo.fr/top_topics/doctissimo/',
                   'http://forum.doctissimo.fr/top_topics/loisirs/',
                   'http://forum.doctissimo.fr/top_topics/people-stars/',
                   'http://forum.doctissimo.fr/top_topics/medicaments/',
                   'http://forum.doctissimo.fr/top_topics/forme-sport/',
                   'http://forum.doctissimo.fr/top_topics/viepratique/',
                   'http://forum.doctissimo.fr/top_topics/animaux/',
                   'http://forum.doctissimo.fr/top_topics/famille/',
                   'http://forum.doctissimo.fr/top_topics/cuisine/',]
        for page in [s + str(year) + '/' + str(month).zfill(2) + '/' for year in range(2015,2016) for month in range(1,13) for s in forums]:
            yield scrapy.Request(page)
        #yield scrapy.Request(page, self.discussionScraper)
        
        
    #start_urls = []

    def parse(self, response):
        def adeqReply(discussion):
            replies = discussion.xpath('./td[@class="sujetCase7"]/text()').extract_first()
            try:
                return int(replies) >= 3
            except:
                return True
                
        def undeletedOP(discussion):
            return discussion.xpath('./td[contains(@class,"sujetCase6")]/text()').extract_first() != "Profil supprimé"
        
        for discussion in response.xpath('//*[@id="block_topics_list"]/tbody/tr'):
            if adeqReply(discussion) and undeletedOP(discussion):
                href = discussion.xpath('./td[@class="sujetCase3"]/a/@href').extract_first()
                #hxs = HtmlXPathSelector(response)
                yield response.follow(href, self.discussionScraper)

#        # follow pagination links
#        for href in response.css('li.next a::attr(href)'):
#            yield response.follow(href, self.parse)

    def discussionScraper(self, response):
        dialog = etree.Element("s")
        words = 0
        turns = 0
        utterances = 0
        
        for post in response.xpath('//div[@id="container"]/div[@class="containerforum"]/div[@class="content-du-forum"]/div/div[@id="lesforums"]/div[@class="container"]/div[@class="mesdiscussions"]/td/div[@id="topic"]/table[@id]/tr[1]'):
            # List containing each username in the conv. as a string 
            user = post.xpath('./td[@class="messCase1"]/div[2]/b[@class="s2"]/descendant-or-self::*[last()]/text()').extract_first()
            # Make a UUID using a SHA-1 hash of a namespace UUID and a name
            # uuid.NAMESPACE_DNS = When this namespace is specified, the name string is a fully-qualified domain name
            uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, user))
            
            # List containing each utterance in order of appearance from the conv. 
            utt = post.xpath('./td[@class="messCase2"]/div[@class="post_content"]/div[not(@class="edited") and not(@class="clear")]/text() | ./td[@class="messCase2"]/div[@class="post_content"]/div[not(@class="edited") and not(@class="clear")]/p/text()').extract()
            if all([u.isspace() for u in utt]) or utt==[]:
                continue
            
            utt_node = etree.SubElement(dialog, 'utt', attrib={'uid' : uid})
            utterances += 1
            
#            print('UTT=',utt.extract_first())
            for br in utt:
                if br.isspace() or br==[]:
                    continue
                paragraph = etree.SubElement(utt_node, 'br')
                paragraph.text = br
                words += len(re.findall('[a-zA-ZÀ-û0-9_]+', br))
#                print(paragraph.text)

        users=response.xpath('//div[@id="container"]/div[@class="containerforum"]/div[@class="content-du-forum"]/div/div[@id="lesforums"]/div[@class="container"]/div[@class="mesdiscussions"]/td/div[@id="topic"]/table[@id]/tr[1]').extract()
        turns += sum([j!=i for i, j in zip(users[:-1], users[1:])])
        with open('Stats.txt', 'a') as stats:
            stats.write(str(words) + ',' + str(turns) + ',' + str(utterances) + "\n")
#        print(etree.tostring(root, pretty_print=True, encoding='unicode')) 
        
        with open('GreyJay_fre.xml', 'a', encoding='utf-8') as f:
            f.write(etree.tostring(dialog, pretty_print=True, encoding='unicode'))

#        yield {
#            'name': extract_with_css('h3.author-title::text'),
#            'birthdate': extract_with_css('.author-born-date::text'),
#            'bio': extract_with_css('.author-description::text'),
#        }
