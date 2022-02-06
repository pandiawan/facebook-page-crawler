#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import logging
import requests

from datetime import datetime, timedelta
from bs4 import BeautifulSoup


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class FacebookPage:
    def __init__(self):
        self.page_url = None
        self.page_id = None
        self.until_date = None

    @staticmethod
    def get_author(element):
        return element.find('img')['aria-label']

    @staticmethod
    def get_post_id(element):
        fb_id = element.find('div', {'data-testid': 'story-subtitle'})['id']
        return fb_id.split(';')[1]

    @staticmethod
    def get_date(element):
        return datetime.fromtimestamp(int(element.find('abbr')['data-utime']))

    @staticmethod
    def get_text(element):
        text = ''.join([i.text for i in element.find('div', {'data-testid': 'post_message'}).findAll('p')])
        return text

    @staticmethod
    def get_comment_count(element):
        return element[3][1]['__bbox']['result']['data']['feedback']['comment_count']['total_count']

    @staticmethod
    def get_share_count(element):
        return element[3][1]['__bbox']['result']['data']['feedback']['share_count']['count']

    @staticmethod
    def get_reactions(reactname, reactions):
        for react in reactions:
            if reactname in str(react):
                return react['reaction_count']
        return 0

    def get_page_id(self):
        max_try = 3
        i = 1
        while True:
            if i > max_try:
                break
            try:
                resp = requests.get(self.page_url)
                page_ids = re.findall('pageID\":\"(.*?)"', resp.text)
                self.page_id = page_ids[0]
                break
            except Exception as e:
                logging.debug(e)
            i += 1

    def parse_content(self, data):
        posts = {}
        soup = BeautifulSoup(data['domops'][0][3]['__html'], 'lxml')
        for element in soup.findAll('div', {'class': 'userContentWrapper'}):
            try:
                post_id = self.get_post_id(element)
                posts[post_id] = {
                    'id': post_id,
                    'author': self.get_author(element),
                    'date': self.get_date(element),
                    'text': self.get_text(element),
                    'link': 'https://www.facebook.com/{}/posts/{}/'.format(
                        self.page_id,
                        post_id
                    )
                }
            except Exception as e:
                del e
                pass

        # Posts
        for element in data['jsmods']['pre_display_requires']:
            try:
                post_id = element[3][1]['__bbox']['variables']['storyID'].split(':')[2]
                comment_count = element[3][1]['__bbox']['result']['data']['feedback']['comment_count']['total_count']
                share_count = element[3][1]['__bbox']['result']['data']['feedback']['share_count']['count']
                react_data = element[3][1]['__bbox']['result']['data']['feedback']['top_reactions']['edges']

                posts[post_id]['comment_count'] = comment_count
                posts[post_id]['share_count'] = share_count

                reactions = {
                    "like": self.get_reactions('LIKE', react_data),
                    "love": self.get_reactions('LOVE', react_data),
                    "haha": self.get_reactions('HAHA', react_data),
                    "wow": self.get_reactions('WOW', react_data),
                    "sad": self.get_reactions('SORRY', react_data),
                    "angry": self.get_reactions('ANGER', react_data),
                    "thankful": self.get_reactions('SUPPORT', react_data),
                    "pride": self.get_reactions('PRIDE', react_data)
                }
                posts[post_id]['reactions'] = reactions

            except Exception as e:
                logging.debug(e)
                pass

        # Videos
        for element in data['jsmods']['require']:
            try:
                post_id = element[3][2]['feedbacktarget']['targetfbid']
                comment_count = element[3][2]['feedbacktarget']['commentcount']
                share_count = element[3][2]['feedbacktarget']['sharecount']
                react_data = []

                posts[post_id]['comment_count'] = comment_count
                posts[post_id]['share_count'] = share_count

                reactions = {
                    "like": self.get_reactions('LIKE', react_data),
                    "love": self.get_reactions('LOVE', react_data),
                    "haha": self.get_reactions('HAHA', react_data),
                    "wow": self.get_reactions('WOW', react_data),
                    "sad": self.get_reactions('SORRY', react_data),
                    "angry": self.get_reactions('ANGER', react_data),
                    "thankful": self.get_reactions('SUPPORT', react_data),
                    "pride": self.get_reactions('PRIDE', react_data)
                }
                posts[post_id]['reactions'] = reactions

            except Exception as e:
                logging.debug(e)
                pass

        return posts

    # Crawl Page Posts
    def crawl(self):

        if self.page_id is None:
            self.get_page_id()

        results = []

        # check can crawl?
        if self.page_id is None:
            logging.info('Please set page_id or page_url')
            return []

        if self.until_date is None:
            self.until_date = datetime.now() - timedelta(days=1)
        else:
            self.until_date = datetime.strptime(self.until_date, '%Y-%m-%d')

        logging.info("Crawling data..")

        timeline_cursor = ''
        max_date = datetime.now()
        break_times = 0

        # request date and break loop when reach the goal
        while max_date > self.until_date:

            # request params
            url = 'https://web.facebook.com/pages_reaction_units/more/'
            params = {'page_id': self.page_id,
                      'cursor': str({"timeline_cursor": timeline_cursor,
                                     "timeline_section_cursor": '{}',
                                     "has_next_page": 'true'}),
                      'surface': 'www_pages_home',
                      'unit_count': 20,
                      '__a': '1'}

            try:
                resp = requests.get(url, params=params)
                data = json.loads(re.sub(r'for \(;;\);', '', resp.text))

                # parse data
                data = self.parse_content(data=data)
                for k, v in data.items():
                    results.append(v)
                    max_date = v['date']

                timeline_cursor = re.findall(
                    r'timeline_cursor\\u002522\\u00253A\\u002522(.*?)\\u002522\\u00252C\\u002522'
                    r'timeline_section_cursor', resp.text)[0]

            except Exception as e:
                logging.error(e)
                break_times += 1
                pass

            if break_times > 5:
                break

        logging.info("Get {} posts".format(len(results)))

        return results
