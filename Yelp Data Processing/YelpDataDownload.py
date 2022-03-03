#!/usr/bin/env python

from yelpapi import YelpAPI
import csv
import json

yelp_api = YelpAPI("<API_KEY>")

result = {}
categoryValue = "mexican, All" # Update category value to whichever category you require here

ofset = 0
limit = 50
while limit + ofset <= 1000:
    response = yelp_api.search_query(term='restaurants', location='Manhattan', categories=categoryValue, limit=limit, offset=ofset)
    ofset +=50
    for elem in response['businesses']:
        if elem['id'] not in result:
            result[elem['id']] = elem
            
f = open("mexican.json", "w") # Update the output file name based on category
json.dump(list(result.values()), f)
f.close()


