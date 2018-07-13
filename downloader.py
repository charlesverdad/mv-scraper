# downloads youtube videos and (maybe) upload them to s3
from pytube import YouTube
import json

from multiprocessing import Pool

def downloadvid(url):
	print("Downloading {}".format(url))

	try:
	    yt = YouTube(url)

	    id_idx = url.find('watch?v=') + 8
	    vid_id = url[id_idx:].rstrip('/')

	    yt.streams.filter(mime_type='video/mp4', res='360p').first().download(output_path='vids/', filename=vid_id)
	except Exception as e:
		print("Exception while downloading {}\n{}".format(url, e))

def downloadvids_path(jsonpath):
	data = ''
	with open(jsonpath) as f:
		data = json.loads(f.read())

	urls = [e['youtube_link'] for e in data]

	print("Starting to download vids from {}".format(jsonpath))
	print("urls")
	p = Pool()
	p.map(downloadvid, urls[:10])



if __name__ == '__main__':

	years = range(2010, 2018)
	formats = [
		'{year}_data.json',
		'{year}_non_billboard_data.json'
	]

	for year in years:
		for item in formats:
			fn = item.format(year=str(year))
			downloadvids_path('dataset/' + fn)

		break





