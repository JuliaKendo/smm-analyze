import time
import itertools
import requests
from tqdm import tqdm
from smm_lib import get_restriction_date


def fetch_vk_posts(params, total_posts=0):
    step = 100
    url = 'https://api.vk.com/method/wall.get'
    for offset in itertools.count(step=step):
        if offset > total_posts:
            break
        params['offset'] = offset
        params['count'] = min(step, total_posts - offset) if total_posts > 0 else step
        response = requests.get(url, params=params)
        response.raise_for_status()
        vk_posts = response.json()
        total_posts = total_posts if total_posts > 0 else vk_posts['response']['count']
        yield from [(post['id'], post['owner_id']) for post in vk_posts['response']['items'] if vk_posts['response']['items']]


def get_post_commentators(params, restriction_date):
    step = 100
    total_comments = step
    url = 'https://api.vk.com/method/wall.getComments'
    for offset in itertools.count(step=step):
        if offset > total_comments:
            break
        time.sleep(0.3)
        params['offset'] = offset
        params['count'] = min(step, total_comments - offset)
        response = requests.get(url, params=params)
        response.raise_for_status()
        post_comments = response.json()
        total_comments = post_comments['response']['count']
        yield from [comment['from_id'] for comment in post_comments['response']['items'] if comment['date'] > restriction_date and 'from_id' in comment]


def get_post_likers(params):
    step = 100
    total_likers = step
    url = 'https://api.vk.com/method/likes.getList'
    for offset in itertools.count(step=step):
        if offset > total_likers:
            break
        time.sleep(0.3)
        params['offset'] = offset
        params['count'] = min(step, total_likers - offset)
        response = requests.get(url, params=params)
        response.raise_for_status()
        post_likers = response.json()
        total_likers = post_likers['response']['count']
        yield from [likers for likers in post_likers['response']['items']]


def fetch_vk_commentators_rating(vk_token, vk_account, posts_number):
    vk_commentators, vk_likers = set(), set()
    restriction_date = get_restriction_date(weeks=2)
    params = {'access_token': vk_token, 'domain': vk_account, 'v': '5.120'}
    vk_posts = fetch_vk_posts(params, posts_number)
    for post_id, owner_id in tqdm(vk_posts, desc="Обработано", unit=" постов VK"):
        params = {
            'access_token': vk_token, 'owner_id': owner_id,
            'post_id': post_id, 'sort': 'desc', 'v': '5.120'
        }
        for post_commentator in get_post_commentators(params, restriction_date):
            vk_commentators.add(post_commentator)

        params = {
            'access_token': vk_token, 'owner_id': owner_id, 'item_id': post_id,
            'type': 'post', 'filter': 'likes', 'v': '5.120'
        }
        for post_liker in get_post_likers(params):
            vk_likers.add(post_liker)

    return vk_commentators.intersection(vk_likers)
