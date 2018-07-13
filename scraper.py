import os
import json
from multiprocessing import Pool

import billboard
import datetime
from PyLyrics import PyLyrics
from yt import get_stats


def get_data(params):
    artist, title, rank, year = params
    print("Fetching data for {}:{}".format(rank,title))
    data = {
        'artist': artist,
        'title': title,
        'year': year,
        'rank': rank,
        'fetched_lyrics': None,
        'youtube_link': None,
        'views': None,
        'likes': None,
        'dislikes': None,
        'updated': str(datetime.datetime.now()),
        'complete': False
    }

    try:
        data['fetched_lyrics'] = PyLyrics.getLyrics(artist, title)
    except:
        pass
    try:
        # get youtube stats
        data.update(get_stats(artist, title))
    except:
        pass

    # set complete if all data is present
    if all([data[k] for k in data if k != 'complete']):
        data['complete'] = True

    return data

    
def get_data_for_date(date, chartname='hot-100-songs'):

    print("Fetching chart {} {}..".format(date, chartname))\

    chart = billboard.ChartData(name=chartname, date=date, yearEnd=True)
    params = [(e.artist, e.title, e.rank, date) for e in chart]
    p = Pool()
    return p.map(get_data, params)

if __name__ == '__main__':

    years = range(2010, 2018)
    for year in years:
        data = get_data_for_date(str(year))
        with open('{}_data.json'.format(year), 'w') as f:
            f.write(json.dumps(all_data))

