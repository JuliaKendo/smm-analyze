import os
import pprint
from dotenv import load_dotenv
from insta_analysis import fetch_insta_commentators_rating
from vk_analysis import fetch_vk_commentators_rating


def main():
    load_dotenv()

    top_insta_commenters, top_insta_commenters_by_posts = fetch_insta_commentators_rating(
        os.getenv('INSTA_LOGIN'),
        os.getenv('INSTA_PASSWORD'),
        'cocacolarus'
    )
    pprint.pprint(f'Comments Top: {top_insta_commenters}')
    pprint.pprint(f'Posts Top: {top_insta_commenters_by_posts}')
    top_vk_commenters = fetch_vk_commentators_rating(os.getenv('VK_ACCESS_TOKEN'), 10)
    pprint.pprint(top_vk_commenters)


if __name__ == '__main__':
    main()
