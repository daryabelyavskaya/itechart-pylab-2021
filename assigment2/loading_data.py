import json
import re
import time

import requests as req
import uuid1
from bs4 import BeautifulSoup

from utils import Logger

logger_page = Logger('page logger')
logger_page.set_logger_level('INFO')
HEADERS = {'User-Agent': 'Mozilla/5.0'}


class ElementsIdConstants:
    POST_TAG_CSS_SELECTOR = "a.SQnoC3ObvgnGjWt90zD9Z._2INHSNB8V5eaWp4P0rY_mE"
    USER_TAG_CSS_SELECTOR = "a._2tbHP6ZydRpjI44J3syuqC._23wugcdiaj44hdfugIAlnX.oQctV4n0yUb0uiHDdGnmE"
    USER_KARMA_TAG_ID = "profile--id-card--highlight-tooltip--karma"
    USER_CAKE_DAY_TAG_ID = "profile--id-card--highlight-tooltip--cakeday"
    NUMBER_OF_VOTES_TAG_CLASS = "_1rZYMD_4xY3gRcSS3p8ODO"
    POST_DATE_TAG_CLASS = "_3jOxDPIQ0KaOWpzvSQo-1s"
    POST_CATEGORY_TAG_CLASS = "_19bCWnxeTjqzBElWZfIlJb"
    NUMBER_OF_COMMENTS_TAG_CLASS = "FHCV02u6Cp2zYL0fhQPsO"




def load_page_data(parser, link, limit):
    posts = []
    parser.driver_get_link(link)
    logger_page.logger_info_message(f'get page link {link}')
    time.sleep(1)
    offset = 0
    while len(posts) < 3:
        elements = parser.find_elements_by_css_selector(ElementsIdConstants.POST_TAG_CSS_SELECTOR)
        users = parser.find_elements_by_css_selector(ElementsIdConstants.USER_TAG_CSS_SELECTOR)
        elements_links = parser.get_links(elements)
        users_links = parser.get_links(users)
        logger_page.logger_info_message('find all posts and their links')
        logger_page.logger_info_message('find all users and their links')
        usernames = [users_links[i][28:-1] for i in range(len(users_links))]
        for el in range(offset, len(elements_links) - 1):
            if len(posts) == 3:
                break
            user = users_links[el]
            post_page = req.get(elements_links[el], headers=HEADERS)
            user_page = req.get(user, headers=HEADERS)
            if user_page.status_code == 502 or post_page.status_code == 502:
                continue
            soup_post = BeautifulSoup(post_page.text, 'html.parser')
            soup_user = BeautifulSoup(user_page.text, 'html.parser')
            logger_page.logger_info_message(
                'user data received')
            logger_page.logger_info_message('post data received')
            post_karma, comment_karma = get_tooltip(soup_user, parser)
            reddit_post = {**post_data(soup_post), **user_page_data(soup_user), 'postUrl': elements_links[el],
                           'username': usernames[el], 'postKarma': post_karma, 'commentKarma': comment_karma,
                           'uniqueId': uuid1.uuid1()}
            posts.append(reddit_post)
            logger_page.logger_info_message(f'the link #{el + 1} are valid')
        parser.scroll()
        offset+= len(elements_links)-offset
    parser.close()
    return posts


def get_text(soup_element):
    if soup_element:
        return soup_element.text

    return ''


def user_page_data(soup):
    return {
        'userKarma': get_text(soup.find('span', id=ElementsIdConstants.USER_KARMA_TAG_ID)),
        'userCakeDay': get_text(soup.find('span', id=ElementsIdConstants.USER_CAKE_DAY_TAG_ID))
    }


def post_data(soup):
    return {
        'numberOfVotes': get_text(soup.find('div', class_=ElementsIdConstants.NUMBER_OF_VOTES_TAG_CLASS)),
        'postDate': get_text(soup.find('a', class_=ElementsIdConstants.POST_DATE_TAG_CLASS)),
        'postCategory': get_text(soup.find('span',
                                           class_=ElementsIdConstants.POST_CATEGORY_TAG_CLASS)),
        'numberOfComments': get_text(
            soup.find('div').find('span', class_=ElementsIdConstants.NUMBER_OF_COMMENTS_TAG_CLASS))
    }


def get_tooltip(soup, parser):
    karma = soup.find('script', id='data').string
    json_text = re.search(r'window.___r = ({.*?})\s*;',
                          karma, flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    flat_dict = json_treating(data)
    return flat_dict['postKarma'], flat_dict['commentKarma']


def json_treating(json_data):
    flat_dict = {}
    if isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, (list, dict)):
                flat_dict.update(json_treating(item))
        return flat_dict
    for key, value in json_data.items():
        if isinstance(value, (list, dict)):
            flat_dict.update(json_treating(value))
        else:
            flat_dict[key] = value
    return flat_dict
