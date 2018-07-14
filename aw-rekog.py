import subprocess
import json
from multiprocessing import Pool

def run_rekognition(fn):
    # starts label detection job and returns jobid
    # aws rekognition start-label-detection --video "S3Object={Bucket='awitiks',Name='vids/-2U0Ivkn2Ds.mp4'}" --region ap-northeast-1
    cmd = [
        'aws',
        'rekognition',
        'start-label-detection',
        '--video',
        'S3Object={Bucket="awitiks",Name="vids/%s"}' % fn,
        '--region',
        'ap-northeast-1'
    ]

    print(''.join(cmd))
    # cmd = "aws rekognition start-label-detection --video \"S3Object={Bucket='awitiks',Name='vids/{}'}\" --region ap-northeast-1".format(fn)
    resp = subprocess.check_output(cmd)
    # print(str(resp))
    # print(type(resp))
    # resp = json.loads(str(subprocess.check_output(cmd)))
    resp = json.loads(resp)
    return resp['JobId']


s3_ls = subprocess.check_output(['aws', 's3', 'ls', 'awitiks/vids/'])
names = str(s3_ls).split('\\n')
filenames = [name.split(' ')[-1] for name in names if len(name) > 2 ]

with open('filenames.json', 'w') as f:
    f.write(json.dumps(filenames))

p = Pool()
fn_rekognition_label_jobs = p.map(run_rekognition, filenames[:5])

with open('rekognition-labels-jobs.json', 'w') as f:
    f.write(json.dumps(fn_rekognition_label_jobs))

