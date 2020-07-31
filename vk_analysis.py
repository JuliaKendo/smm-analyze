import time
import itertools
import requests
from tqdm import tqdm
from amplifer_lib import get_vk_api_parametrs, get_restriction_date


def fetch_vk_posts(params, total_posts=0):
    step = 100
    url = 'https://api.vk.com/method/wall.get'
    for offset in itertools.count(0, step):
        if offset > total_posts:
            break
        params['domain'] = 'cocacola'
        params['offset'] = offset
        params['count'] = min(step, total_posts - offset) if total_posts > 0 else step
        response = requests.get(url, params=params)
        response.raise_for_status()
        dict_data = response.json()
        total_posts = total_posts if total_posts > 0 else dict_data['response']['count']
        yield [(post['id'], post['owner_id']) for post in dict_data['response']['items'] if dict_data['response']['items']]


def get_post_commentators(params, restrict_date):
    step = 100
    total_comments = step
    url = 'https://api.vk.com/method/wall.getComments'
    for offset in itertools.count(0, step):
        time.sleep(0.3)
        if offset > total_comments:
            break
        params['sort'] = 'desc'
        params['offset'] = offset
        params['count'] = min(step, total_comments - offset)

        response = requests.get(url, params=params)
        response.raise_for_status()
        dict_data = response.json()
        total_comments = dict_data['response']['count']
        yield [comments['from_id'] for comments in dict_data['response']['items'] if comments['date'] > restrict_date]


def get_vk_likers(params):
    step = 100
    total_likers = step
    url = 'https://api.vk.com/method/likes.getList'
    for offset in itertools.count(0, step):
        time.sleep(0.3)
        if offset > total_likers:
            break
        params['type'] = 'post'
        params['filter'] = 'likes'
        params['offset'] = offset
        params['count'] = min(step, total_likers - offset)

        response = requests.get(url, params=params)
        response.raise_for_status()
        dict_data = response.json()
        total_likers = dict_data['response']['count']
        yield [likers for likers in dict_data['response']['items']]


def fetch_vk_commentators_rating(vk_token, number_posts):
    top_vk_commentators = set()
    params = get_vk_api_parametrs(vk_token)
    vk_posts = list(itertools.chain(*fetch_vk_posts(params, number_posts)))
    restrict_date = get_restriction_date(weeks=2)
    for post in tqdm(vk_posts, desc="Обработанно", unit=" постов VK"):
        try:
            post_id, owner_id = post
            params = get_vk_api_parametrs(vk_token, owner_id=owner_id, post_id=post_id)
            commentators = set(itertools.chain(*get_post_commentators(params, restrict_date)))
            params = get_vk_api_parametrs(vk_token, owner_id=owner_id, item_id=post_id)
            likers = set(itertools.chain(*get_vk_likers(params)))
            top_vk_commentators = top_vk_commentators.union(commentators.intersection(likers))
        except (KeyError, TypeError, ValueError):
            continue

    return top_vk_commentators
