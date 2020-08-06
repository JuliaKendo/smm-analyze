import requests
from tqdm import tqdm
from collections import Counter
from collections import defaultdict
from smm_lib import get_restriction_date, convert_to_timestamp


def get_common_reactions(reactions):
    common_reactions = Counter(reactions).most_common()
    return common_reactions


def fetch_fb_posts(params, group_id, total_posts=0):
    url = 'https://graph.facebook.com/v7.0/%s' % group_id
    posts_limit = '' if total_posts == 0 else f'.limit({total_posts})'
    params['fields'] = 'feed%s%s' % (posts_limit, '{id}')
    response = requests.get(url, params=params)
    response.raise_for_status()
    fb_posts = response.json()
    yield from [post['id'] for post in fb_posts['feed']['data'] if fb_posts['feed']['data']]


def get_post_commentators(params, post_id, restriction_date):

    url = 'https://graph.facebook.com/v7.0/%s/comments' % post_id
    response = requests.get(url, params=params)
    response.raise_for_status()
    post_comments = response.json()
    yield from [comment['from']['id'] for comment in post_comments['data'] if convert_to_timestamp(comment['created_time']) > restriction_date and 'from' in comment]


def get_post_reactions(params, post_id):

    url = 'https://graph.facebook.com/v7.0/%s/reactions' % post_id
    response = requests.get(url, params=params)
    response.raise_for_status()
    post_reactions = response.json()
    yield from [post_reaction for post_reaction in post_reactions['data']]


def fetch_fb_commentators_rating(fb_token, fb_group, posts_number):
    fb_commentators = set()
    fb_reactions = defaultdict(list)
    restriction_date = get_restriction_date(months=3)
    params = {'access_token': fb_token}
    fb_posts = fetch_fb_posts(params, fb_group, posts_number)
    for post in tqdm(fb_posts, desc="Обработано", unit=" постов FB"):
        params = {'access_token': fb_token}
        for post_commentator in get_post_commentators(params, post, restriction_date):
            fb_commentators.add(post_commentator)
        for post_reaction in get_post_reactions(params, post):
            fb_reactions[post_reaction['id']].append(post_reaction['type'])

    return {commentator_id: get_common_reactions(reactions) for commentator_id, reactions in fb_reactions.items() if commentator_id in fb_commentators}
