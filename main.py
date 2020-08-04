import os
import pprint
import logging
import argparse
import requests
from dotenv import load_dotenv
from insta_analyze import fetch_insta_commentators_rating
from vk_analyze import fetch_vk_commentators_rating
from fb_analyze import fetch_fb_commentators_rating

logger = logging.getLogger('smm_analyze')


def initialize_logger(log_path):
    if log_path:
        output_dir = log_path
    else:
        output_dir = os.path.dirname(os.path.realpath(__file__))
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(output_dir, 'log.txt'), "a")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def create_parser():
    parser = argparse.ArgumentParser(description='Параметры запуска скрипта')
    parser.add_argument('-i', '--instagram', action='store_true', help='Выдача для Instagram')
    parser.add_argument('-v', '--vk', action='store_true', help='Выдача для VK')
    parser.add_argument('-f', '--facebook', action='store_true', help='Выдача для facebook')
    parser.add_argument('-p', '--posts', default=0, help='Количество анализируемых постов', type=int)
    parser.add_argument('-l', '--log', help='Путь к каталогу с log файлом')

    return parser


def main():
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    initialize_logger(args.log)
    all_media = not args.instagram and not args.vk and not args.facebook

    if args.instagram or all_media:
        try:
            top_insta_commenters, top_insta_commenters_by_posts = fetch_insta_commentators_rating(
                os.getenv('INSTA_LOGIN'),
                os.getenv('INSTA_PASSWORD'),
                os.getenv('INSTA_ACCOUNT'),
                args.posts
            )

        except(requests.exceptions.HTTPError, KeyError, ValueError, TypeError) as error:
            logger.exception(f'Ошибка получения данных с instagram: {error}')

        else:
            pprint.pprint(f'Comments Top: {top_insta_commenters}')
            pprint.pprint(f'Posts Top: {top_insta_commenters_by_posts}')

    if args.vk or all_media:
        try:
            top_vk_commenters = fetch_vk_commentators_rating(
                os.getenv('VK_ACCESS_TOKEN'),
                os.getenv('VK_ACCOUNT'),
                args.posts
            )

        except(requests.exceptions.HTTPError, KeyError, ValueError, TypeError) as error:
            logger.exception(f'Ошибка получения данных с VK: {error}')

        else:
            pprint.pprint(top_vk_commenters)

    if args.facebook or all_media:
        try:
            top_fb_commenters = fetch_fb_commentators_rating(
                os.getenv('FB_ACCESS_TOKEN'),
                os.getenv('FB_GROUP_ID'),
                args.posts
            )

        except(requests.exceptions.HTTPError, KeyError, ValueError, TypeError) as error:
            logger.exception(f'Ошибка получения данных с facebook: {error}')

        else:
            pprint.pprint(top_fb_commenters)


if __name__ == '__main__':
    main()
