'''
Purpose: Takes a list of centroid points and calls GoogleMaps API to get a list of N
		 closest grocery stores to it. Saves this data to a CSV.
'''

import os
import sys
import googlemaps
import progressbar
import time
import pandas as pd

if len(sys.argv) < 2:
	print 'Usage: '
	print '\t python {} <folder/filename>'.format(sys.argv[0])
	exit()

try:
	gmaps = googlemaps.Client(key = os.environ.get('GOOGLE_MAPS_TOKEN'))
except ValueError:
	print 'User Error: must load GOOGLE_MAPS_TOKEN'
	exit()

DIR = os.getcwd()
bar = progressbar.ProgressBar()
number_stores = 3

# read in data from CSV
data = pd.read_csv(DIR + '/' + sys.argv[1])

for j in range(number_stores):
	data['storename-' + str(j)] = 'store-name'
	data['storeid-' + str(j)] = 'id'
	data['storelongitude-' + str(j)] = 'store-longitude'
	data['storelatitude-' + str(j)] = 'store-latitude'
	data['storevicinity-' + str(j)] = 'vicinity'

# look through rows, extract top N search results from google for a given location
my_type = 'grocery_or_supermarket'
my_language = 'en'

print 'status bar:'
for i in bar(range(data.shape[0])):
	my_location = (data.get_value(i, 'latitude'), data.get_value(i, 'longitude'))
	results = gmaps.places_nearby(my_location, language=my_language, open_now=False, radius=200*10, rank_by='prominence', type=my_type)

	for j in range(number_stores):
		data = data.set_value(i, 'storename-' + str(j), results['results'][j]['name'].encode('ascii', 'ignore'))
		data = data.set_value(i, 'storeid-' + str(j), results['results'][j]['id'])
		data = data.set_value(i, 'storelatitude-' + str(j), results['results'][j]['geometry']['location']['lat'])
		data = data.set_value(i, 'storelongitude-' + str(j), results['results'][j]['geometry']['location']['lng'])
		data = data.set_value(i, 'storevicinity-' + str(j), results['results'][j]['vicinity'].encode('ascii', 'ignore'))

	time.sleep(0.1)

file_name = DIR + '/inter/stores-near-block-centroid-' + sys.argv[1][-5:]
data.to_csv(file_name, sep = ',')
