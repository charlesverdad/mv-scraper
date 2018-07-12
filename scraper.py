import billboard
from pylyrics3 import get_song_lyrics
from PyLyrics import PyLyrics
from lyricsgenius import Genius
import os

date = '2017'
chartname = 'hot-100-songs'
# genius_access_token = os.environ.get('GENIUS_CLIENT_ACCESS_TOKEN')
# genius_api = Genius(genius_access_token)

data = {}
print("Fetching chart..")
chart = billboard.ChartData(name=chartname, date=date, yearEnd=True)
errcount = 0
for entry in chart[:10]:

	print("Fetching data for {}".format(entry.title))
	key = (entry.artist, entry.title)

	if key not in data:
		data[key] = {
			'ranks': [],
			'fetched_lyrics': ''
		}

	data[key]['ranks'].append((entry.rank, chart.date))
	try:
		# data[key]['fetched_lyrics'] = get_song_lyrics(entry.artist, entry.title)
		data[key]['fetched_lyrics'] = PyLyrics.getLyrics(entry.artist, entry.title)
		# data[key]['fetched_lyrics'] = genius_api.search_song(entry.title, entry.artist, take_first_result=True, remove_section_headers=True).lyrics
	except:
		pass

	if data[key]['fetched_lyrics'] is None or len(data[key]['fetched_lyrics']) == 0:
		errcount += 1


print(data)
print(errcount)