
import json


years = range(2010, 2018)

collated_data = []
for year in years:
    fn = 'dataset/{}_data.json'.format(year)
    with open(fn) as f:
        data = json.loads(f.read())
        collated_data.extend(data)
    fn = 'dataset/{}_non_billboard_data.json'.format(year)
    with open(fn) as f:
        data = json.loads(f.read())
        collated_data.extend(data)
print(collated_data[:10])
print(len(collated_data))

for i in range(len(collated_data)):
    if collated_data[i]['youtube_link']:
        id_idx = collated_data[i]['youtube_link'].find('watch?v=') + 8
        vid_id = collated_data[i]['youtube_link'][id_idx:].rstrip('/')
        collated_data[i]['yt_id'] = vid_id

with open('all_data.json', 'w') as f:
    f.write(json.dumps(collated_data))