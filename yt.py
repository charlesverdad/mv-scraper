'''
dirty youtube stats parser
'''

from bs4 import BeautifulSoup
import requests
import re

HEADERS = {
    'User-Agent': 'yt.py'
}

def downloadHTML(url, timeout=25):
    """Downloads and returns the webpage with the given URL.
    Returns an empty string on failure.
    """
    assert url.startswith('http://')
    req = requests.get(url, headers=HEADERS, timeout=timeout)
    req.encoding = 'utf-8'
    if req.status_code == 200:
        return req.text
    else:
        return ''

def searchmv(artist, title, n=5):
    '''
    returns the top n search results.
    '''
    query = artist + ' ' + title + 'official music video'
    query = ''.join([c for c in query if c.isalnum or c == ' '])
    query.replace(' ', '+')
    url = 'http://www.youtube.com/results?search_query={}'.format(query)

    html = downloadHTML(url)
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', {'class': 'yt-lockup-content'})

    links = []
    for result in results[:n]:
        a = result.find('a', {'class': 'yt-uix-tile-link'}, href=True)
        link = a['href'][1:]
        if link.startswith('watch'):
            links.append(link)

    return links

import io
def to_int(text):
    return int(text.replace(',', ''))

def scrapeVid(link):
    url = ''
    if link.startswith('http'):
        url = link
    elif link.startswith('watch'):
        url = 'http://youtube.com/{}'.format(link)
    else:
        raise Exception('invalid link provided')

    html = downloadHTML(url)
    soup = BeautifulSoup(html, 'html.parser')

    views = to_int(soup.find('div', {'class', 'watch-view-count'}).contents[0].strip().split(' ')[0])

    stats = soup.find('span', {'class', 'like-button-renderer'})
    # print(stats)
    buttons = stats.find_all('button')

    likes = None
    dislikes = None

    for button in buttons:
        if "Gusto ko ito" in str(button):
            likes = to_int(button.find('span').contents[0].strip())
        if "Hindi ko ito gusto" in str(button):
            dislikes = to_int(button.find('span').contents[0].strip())

    # year_uploaded = int(soup.find('strong', {'class', 'watch-time-text'}).contents[0].strip().split(' ')[-1])
    data ={
        'youtube_link': url,
        'views': views,
        'likes': likes,
        'dislikes': dislikes
    }

    return data
    # with io.open('video.html', 'w', encoding='utf-8') as f:
    #     f.write(soup.encode('utf-8').decode())

def get_stats(artist, title):
    return scrapeVid(searchmv(artist, title, 1)[0])
