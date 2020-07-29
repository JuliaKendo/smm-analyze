import datetime
import dateutil.relativedelta
from instabot import Bot
from collections import Counter
from collections import defaultdict


def get_restriction_date():
    current_time = datetime.datetime.today()
    current_date = current_time.combine(current_time.date(), current_time.min.time())
    restrict_date = current_date - dateutil.relativedelta.relativedelta(months=3)
    return restrict_date.timestamp()


def fetch_insta_commentators_rating(login, password, account):
    bot = Bot()
    bot.login(username=login, password=password)
    total_medias = bot.get_total_user_medias(account)
    commenters = []
    commenters_by_posts = defaultdict(set)
    restrict_date = get_restriction_date()
    for media_id in total_medias:
        media_comments = bot.get_media_comments_all(media_id)
        for comment in media_comments:
            if comment['created_at'] <= restrict_date:
                continue
            commenters.append(comment['user_id'])
            commenters_by_posts[comment['user_id']].add(media_id)

    rated_users = Counter(commenters).most_common()
    top_commenters = {user_id: rating for user_id, rating in rated_users if rating > 1}
    top_commenters_by_posts = {user_id: len(posts) for user_id, posts in commenters_by_posts.items() if len(posts) > 1}
    return top_commenters, top_commenters_by_posts
