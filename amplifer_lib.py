import re
import datetime
import dateutil.relativedelta
from collections import Counter


def get_restriction_date(**kwargs):

    current_time = datetime.datetime.today()
    current_date = current_time.combine(current_time.date(), current_time.min.time())
    if 'weeks' in kwargs.keys():
        restrict_date = current_date - dateutil.relativedelta.relativedelta(weeks=kwargs['weeks'])
    elif 'months' in kwargs.keys():
        restrict_date = current_date - dateutil.relativedelta.relativedelta(months=kwargs['months'])
    else:
        restrict_date = current_date

    return restrict_date.timestamp()


def get_vk_api_parametrs(vk_token, **kwargs):
    params = {
        'access_token': vk_token,
        'v': '5.120'
    }
    for key in kwargs.keys():
        params[key] = kwargs[key]

    return params


def get_fb_api_parametrs(fb_token, **kwargs):
    params = {
        'access_token': fb_token,
    }
    for key in kwargs.keys():
        params[key] = kwargs[key]

    return params


def get_reactions_rating(reactions):
    list_reactions = Counter(reactions).most_common()
    return {reaction[0]: reaction[1] for reaction in list_reactions}


def convert_to_timestamp(date):
    date = re.findall('^(.*?)[T]', date)[0]
    return datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()


def get_user_id(comments):
    if 'from' in comments.keys():
        return comments['from']['id']
    elif 'id' in comments.keys():
        return comments['id']
