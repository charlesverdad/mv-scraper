import json
import io

all_data = ''
with open('all_data.json') as f:
    all_data = json.loads(f.read())

for data in all_data:
    if data.get('yt_id'):
        with io.open('lyrics/{}.txt'.format(data['yt_id']), 'w', encoding='utf-8') as f:
            f.write(data['fetched_lyrics'])
            # f.write(data['fetched_lyrics'].encode('utf-8').decode())
    else:
        print('no yt_id found')