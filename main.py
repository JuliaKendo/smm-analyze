import os
import pprint
from insta_analysis import fetch_insta_commentators_rating


def main():
    top_insta_commenters, top_insta_commenters_by_posts = fetch_insta_commentators_rating(
        os.environ.get('INSTA_LOGIN'),
        os.environ.get('INSTA_PASSWORD'),
        'cocacolarus'
    )
    pprint.pprint(f'Comments Top: {top_insta_commenters}')
    pprint.pprint(f'Posts Top: {top_insta_commenters_by_posts}')


if __name__ == '__main__':
    main()
