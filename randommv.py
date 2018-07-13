import datetime
import requests
from multiprocessing import Pool
import random
import json


from bs4 import BeautifulSoup
from scraper import get_data
import billboard

HEADERS = {
    'User-Agent': 'yt.py'
}

def downloadHTML(url, timeout=25):
    """Downloads and returns the webpage with the given URL.
    Returns an empty string on failure.
    """
    assert url.startswith('http')
    req = requests.get(url, headers=HEADERS, timeout=timeout)
    req.encoding = 'utf-8'
    if req.status_code == 200:
        return req.text
    else:
        print(req.status_code)
        return ''

def scrape_vids(params):
    '''
    Returns list of artist, title tuple scraped from the given 
    year and page number
    '''
    year, page = params
    print("Scraping year {} page {}".format(year, page))
    url = 'http://imvdb.com/calendar/{}?page={}'.format(year, page)
    html = downloadHTML(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    table = soup.find('table', {'class', 'imvdbTable'})
    rows = table.find_all('tr')

    out = []

    for row in rows:
        title = row.find('h3').find('a').contents[0].strip()[:-6].strip()
        artist = row.find('h4').find('a').contents[0].strip()
        out.append((artist, title))

    return out

def get_mvs_by_year(year, limit=120):
    # returns an array of (artist, title)
    # of music videos released in the given year.


    url = 'http://imvdb.com/calendar/{}?page=1'.format(year)
    html = downloadHTML(url)
    soup = BeautifulSoup(html, 'html.parser')

    # print(html)
    # with open('blah.html', 'w') as f:
    #     f.write(str(soup))

    num_vids = soup.find('h3', {'class', 'rack_title'}).contents[0].split(' ')[-1]
    num_vids = int(num_vids[1:-1].replace(',', ''))

    table = soup.find('table', {'class', 'imvdbTable'})
    rows = table.find_all('tr')

    # num_pages = num_vids // len(rows) + 1
    num_pages = 10
    params = []
    for i in range(1, num_pages + 1):
        params.append((year, i))

    p = Pool()
    batches = p.map(scrape_vids, params)
    vids = []
    for batch in batches:
        vids.extend(batch)

    random.shuffle(vids)

    return vids[:limit]

def fetch_mvs_data(vids, year):
    # given a list of vids, fetch needed data
    # skip songs that are in the hot-100 year-end chart of billboard
    print(vids)
    print("Fetching video data")
    chart = billboard.ChartData(name='hot-100-songs', date=str(year), yearEnd=True)
    billboard_titles = set([e.title.lower() for e in chart])

    # params is an array of tuple: (artist, title, rank, year)
    params = [(vid[0], vid[1], 0, year) for vid in vids if vid[1] not in billboard_titles]

    p = Pool()
    return p.map(get_data, params)




if __name__ == '__main__':

    years = range(2010, 2018)
    for year in years:
        print("Processing year {}".format(year))
        vids = get_mvs_by_year(year)
        data = fetch_mvs_data(vids, year)
        with open('{}_non_billboard_data.json'.format(year), 'w') as f:
            f.write(json.dumps(data))



