from difflib import SequenceMatcher
from urllib.parse import urljoin

import atoma
import requests
from settings import settings


def get_post_url_list():
    url = 'https://nueleanu.com/sitemap.json'
    response = requests.get(url)

    return response.json()


def get_medium_user_id():
    url = 'https://api.medium.com/v1/me'

    response = requests.get(url, headers={
        'Authorization': f'Bearer {settings.medium_token}'
    })

    json = response.json()

    return json['data']['id']


def get_medium_titles():
    url = 'https://medium.com/feed/@dotmethod'
    response = requests.get(url)
    feed = atoma.parse_rss_bytes(response.content)

    titles = [post.title for post in feed.items if post.title]
    return titles


def create_medium_article(user_id: str, post_url: str, title: str, content: str):
    url = f'https://api.medium.com/v1/users/{user_id}/posts'
    headers = {
        'Authorization': f'Bearer {settings.medium_token}'
    }

    data = {
        "title": title,
        "contentFormat": "markdown",
        "content": content,
        "canonicalUrl": post_url,
        "publishStatus": "public"
    }

    response = requests.post(url, headers=headers, data=data)
    json = response.json()
    return json['data']


def sync_blog_to_medium():
    print("Running sync_blog_to_medium...")
    user_id = get_medium_user_id()
    medium_post_titles = get_medium_titles()
    posts = get_post_url_list()

    for post in posts:
        post_url = urljoin("https://nueleanu.com/posts/", post['slug'])
        title = post['title']

        exists = False
        for t in medium_post_titles:
            if SequenceMatcher(None, t, title).ratio() > 0.9:
                exists = True
                break

        if not exists:
            try:
                create_medium_article(user_id, post_url, title, post['content'])
                print(f'Created new medium article. Title: {title} / Original URL: {post_url}')
            except Exception as e:
                print(f'Failed creating medium article, {e}')
