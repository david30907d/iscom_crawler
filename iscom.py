from KCM.__main__ import KCM
import json, sys, requests, os, pyprind
k = KCM('cht', './ptt', uri='mongodb://172.17.0.11:27017')
# k.removeDB()
# k.main()
name = json.load(open('name.json','r'))
name2add = json.load(open('台灣所有景點的地址.json', 'r'))

query = sys.argv[1]
tmp = [i for i in k.get(query, 10000) if i[0] in name and len(i[0]) > 2 ][:int(sys.argv[2])]

distance = []
for i in pyprind.prog_bar(tmp):
    try:
        if os.path.isfile(i[0]+'.json'):
            res = json.load(open(i[0]+'.json','r'))
        else:
            res = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key=AIzaSyB20qKjF1ePtq9t1luvFd-433J41anlDGU'.format(name2add[query], name2add[i[0]])).json()
            json.dump(res, open(i[0]+'.json','w'))
        if res['rows'][0]['elements'][0]['status'] == 'OK':
            distance.append((i[0], res['rows'][0]['elements'][0]['distance']['value']))
    except Exception as e:
        pass
distance = sorted(distance, key=lambda x:x[1])[:int(sys.argv[3])]
print(tmp[:int(sys.argv[3])])
print(distance)

hybrid = {}
for index, (i, j) in enumerate(zip(tmp, distance)):
    if i[0] == j[0]:
        hybrid[i[0]] = hybrid.setdefault(i[0], 0) + index
    else:
        hybrid[i[0]] = hybrid.setdefault(i[0], 0) + index*0.01
        hybrid[j[0]] = hybrid.setdefault(j[0], 0) + index*0.99

print(sorted(hybrid.items(), key=lambda x:-x[1])[:int(sys.argv[3])])