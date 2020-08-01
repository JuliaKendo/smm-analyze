import time
import itertools
import requests
from tqdm import tqdm
from smm_lib import get_api_parametrs, get_restriction_date


def fetch_vk_posts(params, total_posts=0):
    step = 100
    url = 'https://api.vk.com/method/wall.get'
    for offset in itertools.count(0, step):
        if offset > total_posts:
            break
        params['offset'] = offset
        params['count'] = min(step, total_posts - offset) if total_posts > 0 else step
        response = requests.get(url, params=params)
        response.raise_for_status()
        dict_data = response.json()
        total_posts = total_posts if total_posts > 0 else dict_data['response']['count']
        yield [(post['id'], post['owner_id']) for post in dict_data['response']['items'] if dict_data['response']['items']]


def get_post_commentators(params, restriction_date):
    step = 100
    total_comments = step
    url = 'https://api.vk.com/method/wall.getComments'
    for offset in itertools.count(0, step):
        if offset > total_comments:
            break
        time.sleep(0.3)
        params['sort'] = 'desc'
        params['offset'] = offset
        params['count'] = min(step, total_comments - offset)

        response = requests.get(url, params=params)
        response.raise_for_status()
        dict_data = response.json()
        total_comments = dict_data['response']['count']
        yield [comments['from_id'] for comments in dict_data['response']['items'] if comments['date'] > restriction_date]


def get_post_likers(params):
    step = 100
    total_likers = step
    url = 'https://api.vk.com/method/likes.getList'
    for offset in itertools.count(0, step):
        if offset > total_likers:
            break
        time.sleep(0.3)
        params['type'] = 'post'
        params['filter'] = 'likes'
        params['offset'] = offset
        params['count'] = min(step, total_likers - offset)

        response = requests.get(url, params=params)
        response.raise_for_status()
        dict_data = response.json()
        total_likers = dict_data['response']['count']
        yield [likers for likers in dict_data['response']['items']]


def fetch_vk_commentators_rating(vk_token, vk_account, number_posts):
    vk_commentators = set()
    params = get_api_parametrs(vk_token, domain=vk_account, v='5.120')
    vk_posts = itertools.chain(*fetch_vk_posts(params, number_posts))
    restriction_date = get_restriction_date(weeks=2)
    for post in tqdm(vk_posts, desc="Обработанно", unit=" постов VK"):
        post_id, owner_id = post

        params = get_api_parametrs(vk_token, owner_id=owner_id, post_id=post_id, v='5.120')
        commentators = set(itertools.chain(*get_post_commentators(params, restriction_date)))

        params = get_api_parametrs(vk_token, owner_id=owner_id, item_id=post_id, v='5.120')
        likers = set(itertools.chain(*get_post_likers(params)))

        vk_commentators = vk_commentators.union(commentators.intersection(likers))

    return vk_commentators
