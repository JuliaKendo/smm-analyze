from tqdm import tqdm
from instabot import Bot
from collections import Counter
from collections import defaultdict
from amplifer_lib import get_restriction_date


def fetch_insta_commentators_rating(login, password, account):
    bot = Bot()
    bot.login(username=login, password=password)
    total_medias = bot.get_total_user_medias(account)
    commenters = []
    commenters_by_posts = defaultdict(set)
    restrict_date = get_restriction_date(months=3)
    for media_id in tqdm(total_medias, desc="Обработанно", unit=" постов instagram"):
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
