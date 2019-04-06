
import json
import csv
import sys

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


with open("Location History.json") as f:
    x= json.load(f)
    
header = ['timestampMs', 'latitudeE7', 'longitudeE7', 'velocity', 'altitude', 'verticalAccuracy', 'heading', 'accuracy','activityId']

out=open("Loc.csv","w")
fw = csv.writer(out)
fw.writerow(header)

headerA= ['activityId','timestampMs','extraId','subActivityId']
outA=open("Act.csv","w")
fwA = csv.writer(outA)
fwA.writerow(headerA)

headerE= ['extraId','type','name','intVal']
outE=open("Extra.csv","w")
fwE = csv.writer(outE)
fwE.writerow(headerE)

headerSA= ['subActivityId','confidence','type']
outSA=open("SubAct.csv","w")
fwSA = csv.writer(outSA)
fwSA.writerow(headerSA)

actId=0
subActId=0
extraId=0

for i in range(len(x['locations'])):
    s=[]
    for h in header:
        if h in x['locations'][i].keys():
            s.append(x['locations'][i][h])
        else:
            if h !='activityId':
                s.append('')
    if 'activity' in x['locations'][i].keys():
        actId+=1
        s.append(actId)
        for act in x['locations'][i]['activity']:
            ac=[]
            ac.append(actId)
            ac.append(act['timestampMs'])
            if 'extra' in act.keys():
                extraId+=1
                ac.append(extraId)
                ex=[]
                ex.append(extraId)
                ex.append(act['extra'][0]['type'])
                ex.append(act['extra'][0]['name'])
                ex.append(act['extra'][0]['intVal'])
                fwE.writerow(ex)
            else:
                ac.append('')
            if 'activity' in act.keys():
                subActId+=1
                ac.append(subActId)
                for sact in act['activity']:
                    sa=[]
                    sa.append(subActId)
                    sa.append(sact['confidence'])
                    sa.append(sact['type'])
                    fwSA.writerow(sa)
            else:
                ac.append('')
            fwA.writerow(ac)
    else:
        s.append('')
    progress(i,len(x['locations']),'On it')
    fw.writerow(s)

progress(len(x['locations']),len(x['locations']),'Done')

out.close()