import re
import datetime
import dateutil.relativedelta


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


def get_api_parameters(vk_token, **kwargs):
    params = {
        'access_token': vk_token
    }
    for key in kwargs.keys():
        params[key] = kwargs[key]

    return params


def convert_to_timestamp(date):
    date = re.findall('^(.*?)[T]', date)[0]
    return datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()
