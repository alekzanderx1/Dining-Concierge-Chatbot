import json

with open('japanese.json') as json_data: 		#change input filename here based on category
	items = json.load(json_data)
	with open('japaneseJSON.json', 'w') as f: 	# change output filename here based on category
		for item in items:
			res = {}
			res["_index"] = "restaurants"
			res["_id"] = item['id']
			res2 = {}
			res2["index"] = res
			f.write(json.dumps(res2))
			f.write('\n')
			doc = {}
			doc['category'] = "japanese" 		# change category here
			doc['RestaurantID'] = item['id']
			f.write(json.dumps(doc))
			f.write('\n')

