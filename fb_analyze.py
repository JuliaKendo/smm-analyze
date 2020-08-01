import requests
import itertools
from tqdm import tqdm
from collections import Counter
from collections import defaultdict
from smm_lib import get_fb_api_parametrs, get_restriction_date, convert_to_timestamp


def get_user_id(comments):
    if 'from' in comments.keys():
        return comments['from']['id']
    elif 'id' in comments.keys():
        return comments['id']


def get_reactions_rating(reactions):
    list_reactions = Counter(reactions).most_common()
    return {reaction[0]: reaction[1] for reaction in list_reactions}


def fetch_fb_posts(params, group_id, total_posts=0):
    url = 'https://graph.facebook.com/v7.0/%s' % group_id
    params['fields'] = 'feed%s%s' % ('' if total_posts == 0 else f'.limit({total_posts})', '{id}')
    response = requests.get(url, params=params)
    response.raise_for_status()
    dict_data = response.json()
    yield [post['id'] for post in dict_data['feed']['data'] if dict_data['feed']['data']]


def get_post_commentators(params, post_id, restrict_date):

    url = 'https://graph.facebook.com/v7.0/%s/comments' % post_id
    response = requests.get(url, params=params)
    response.raise_for_status()
    dict_data = response.json()
    yield [get_user_id(comments) for comments in dict_data['data'] if convert_to_timestamp(comments['created_time']) > restrict_date]


def get_post_reactions(params, post_id):

    url = 'https://graph.facebook.com/v7.0/%s/reactions' % post_id
    response = requests.get(url, params=params)
    response.raise_for_status()
    dict_data = response.json()
    yield {reaction['id']: reaction['type'] for reaction in dict_data['data']}


def fetch_fb_commentators_rating(fb_token, fb_group, number_posts):
    fb_commenters = set()
    reactions = defaultdict(list)
    restrict_date = get_restriction_date(months=3)
    params = get_fb_api_parametrs(fb_token)
    fb_posts = itertools.chain(*fetch_fb_posts(params, fb_group, number_posts))
    for post in tqdm(fb_posts, desc="Обработанно", unit=" постов FB"):
        params = get_fb_api_parametrs(fb_token)
        commentators_id = set(itertools.chain(*get_post_commentators(params, post, restrict_date)))
        fb_commenters = fb_commenters.union(commentators_id)
        for post_reactions in get_post_reactions(params, post):
            for user_id, reaction in post_reactions.items():
                reactions[user_id].append(reaction)

    return {user_id: get_reactions_rating(reactions) for user_id, reactions in reactions.items() if user_id in fb_commenters}
