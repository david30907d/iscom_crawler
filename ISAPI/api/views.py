from KCM.__main__ import sF
from django.http import JsonResponse
from ISAPI.settings import uri
import json, requests, os
from ngram import NGram

k = sF('cht', './ptt', uri=uri)

name2add = json.load(open('台灣所有景點的地址.json', 'r'))
header = json.load(open('交通局class.json', 'r'))
searchNgram = NGram(name2add.keys())

def api(request):
    query = request.GET['query']
    number = request.GET['number']
    
    def hybrid(ratioX, ratioY):
        hybridResult = {}
        for index, (i, j) in enumerate(zip(tmp, distance)):
            if i[0] == j[0]:
                hybridResult[i[0]] = hybridResult.setdefault(i[0], 0) + index
            else:
                hybridResult[i[0]] = hybridResult.setdefault(i[0], 0) + index * ratioX / (ratioX + ratioY)
                hybridResult[j[0]] = hybridResult.setdefault(j[0], 0) + index * ratioY / (ratioX + ratioY)
        return hybridResult

    kcmResult = k.sz(query, 10000)
    if not kcmResult:
        kcmResult = k.sz(searchNgram.find(query), 10000)
    tmp = [i for i in kcmResult if i[0] in name2add and len(i[0]) > 2 ][:200]
    distance = []
    for i in tmp:
        try:
            if os.path.isfile('json/' + query + '-' + i[0]+'.json'):
                res = json.load(open('json/' + query + '-' + i[0]+'.json','r'))
            else:
                res = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key=AIzaSyB20qKjF1ePtq9t1luvFd-433J41anlDGU'.format(name2add[query], name2add[i[0]])).json()
                if res['rows'][0]['elements'][0]['status'] == 'OK':
                    json.dump(res, open('json/' + query + '-' + i[0]+'.json','w'))
            if res['rows'][0]['elements'][0]['status'] == 'OK':
                distance.append((i[0], res['rows'][0]['elements'][0]['distance']['value']))
        except Exception as e:
            pass
    distance = sorted(distance, key=lambda x:x[1])[:int(number)]

    result = hybrid(2, 8)
    result = sorted(result.items(), key=lambda x:-x[1])[:int(number)]

    if result == []:
        result = tmp[:10]
    return JsonResponse([(i[0], header.get(i[0], '未知')) for i in result], safe=False)

def findRoot(request):
    type = request.GET['type']
    city = request.GET['city']
    result = [i for i in k.sz(type, 10000) if i[0] in name2add and len(i[0]) > 2 and city in name2add[i[0]] ][:20]
    print(result)
    return JsonResponse(result, safe=False)
