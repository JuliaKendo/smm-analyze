import os
import pprint
import argparse
from dotenv import load_dotenv
from insta_analysis import fetch_insta_commentators_rating
from vk_analysis import fetch_vk_commentators_rating
from fb_analysis import fetch_fb_commentators_rating


def create_parser():
    parser = argparse.ArgumentParser(description='Параметры запуска скрипта')
    parser.add_argument('instagram', action='store_false', help='Выдача для Instagram')
    parser.add_argument('vk', action='store_false', help='Выдача для VK')
    parser.add_argument('facebook', action='store_false', help='Выдача для facebook')
    parser.add_argument('-p', '--posts', default=10, help='Количество анализируемых постов', type=int)
    parser.add_argument('-l', '--log', help='Путь к каталогу с log файлом')

    return parser


def main():
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    if args.instagram or not (args.instagram and args.vk and args.facebook):
        top_insta_commenters, top_insta_commenters_by_posts = fetch_insta_commentators_rating(
            os.getenv('INSTA_LOGIN'),
            os.getenv('INSTA_PASSWORD'),
            'cocacolarus'
        )
        pprint.pprint(f'Comments Top: {top_insta_commenters}')
        pprint.pprint(f'Posts Top: {top_insta_commenters_by_posts}')

    if args.vk or not (args.instagram and args.vk and args.facebook):
        top_vk_commenters = fetch_vk_commentators_rating(os.getenv('VK_ACCESS_TOKEN'), args.posts)
        pprint.pprint(top_vk_commenters)

    if args.facebook or not (args.instagram and args.vk and args.facebook):
        top_fb_commenters = fetch_fb_commentators_rating(os.getenv('FB_ACCESS_TOKEN'), os.getenv('FB_GROUP_ID'), args.posts)
        pprint.pprint(top_fb_commenters)


if __name__ == '__main__':
    main()
