from KCM.__main__ import KCM
import json, sys
k = KCM('cht', './ptt', uri='mongodb://172.17.0.11:27017')
# k.removeDB()
# k.main()
name = json.load(open('name.json','r'))

tmp = [i for i in k.get(sys.argv[1], 10000) if i[0] in name and len(i[0]) > 2 ][:15]
touristSpot2location = json.load(open('景點2地址.json', 'r'))
if sys.argv[1] not in touristSpot2location:
	print(tmp)
else:
	city = touristSpot2location[sys.argv[1]]
	result = []
	for i in tmp:
		if i[0] in touristSpot2location and touristSpot2location[i[0]] == city:
			result.append(i)
	for i in tmp:
		if i not in result:
			result.append(i)
	print(result)
