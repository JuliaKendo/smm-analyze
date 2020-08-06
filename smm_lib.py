import re
import datetime
import dateutil.relativedelta


def get_restriction_date(**kwargs):

    current_time = datetime.datetime.today()
    current_date = current_time.combine(current_time.date(), current_time.min.time())
    if 'weeks' in kwargs:
        restrict_date = current_date - dateutil.relativedelta.relativedelta(weeks=kwargs['weeks'])
    elif 'months' in kwargs:
        restrict_date = current_date - dateutil.relativedelta.relativedelta(months=kwargs['months'])
    else:
        restrict_date = current_date

    return restrict_date.timestamp()


def convert_to_timestamp(date):
    date = re.findall(r'^(.*?)[T]', date)[0]
    return datetime.datetime.strptime(date, "%Y-%m-%d").timestamp()
