import billboard
from PyLyrics import PyLyrics
import os
import json

date = '2017'
chartname = 'hot-100-songs'

data = {}
print("Fetching chart..")
chart = billboard.ChartData(name=chartname, date=date, yearEnd=True)
errcount = 0
for entry in chart:

	print("Fetching data for {}".format(entry.title))
	key = ":".join([entry.artist, entry.title])

	if key not in data:
		data[key] = {
			'ranks': [],
			'fetched_lyrics': ''
		}

	data[key]['ranks'].append((entry.rank, chart.date))
	try:
		data[key]['fetched_lyrics'] = PyLyrics.getLyrics(entry.artist, entry.title)
	except:
		pass

	if data[key]['fetched_lyrics'] is None or len(data[key]['fetched_lyrics']) == 0:
		errcount += 1


print("{} song lyrics missing".format(errcount))
print("Writing data..")
with open('out.json', 'w') as f:
	f.write(json.dumps(data))
