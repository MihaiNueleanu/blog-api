import json
from asyncio.tasks import sleep
from difflib import SequenceMatcher
from urllib.parse import urljoin

import requests
from settings import settings
from .medium_query import medium_query


def get_post_url_list():
    url = 'https://dotmethod.me/sitemap.json'
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
    url = 'https://dotmethod.medium.com/_/graphql'
    variables = {
        "id": "9585a11eb753",
        "homepagePostsLimit": 25,
        "includeDistributedResponses": True
    }

    data = {
        'query': medium_query,
        'variables': variables
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    result = requests.post(
        url=url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers
    )

    posts = result.json()[
        'data']['userResult']['homepagePostsConnection']['posts']
    titles = [post['title'] for post in posts]
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


async def sync_blog_to_medium():
    print("Running sync_blog_to_medium...")
    await sleep(30)

    user_id = get_medium_user_id()
    medium_post_titles = get_medium_titles()
    posts = get_post_url_list()

    for post in posts:
        post_url = urljoin("https://dotmethod.me/posts/", post['slug'])
        title = post['title']

        exists = False
        for t in medium_post_titles:
            if SequenceMatcher(None, t, title).ratio() > 0.9:
                exists = True
                break

        if not exists:
            try:
                create_medium_article(
                    user_id, post_url, title, post['content'])
                print(
                    f'Created new medium article. Title: {title} / Original URL: {post_url}')
            except Exception as e:
                print(f'Failed creating medium article, {e}')
