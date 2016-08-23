import os
import googlemaps
import pandas as pd

DATA_DIR = '~/Documents/dc-data/data/'
DIR 	 = '~/Documents/dc-data/grocery-store/'

gmaps = googlemaps.Client(key = os.environ.get('GOOGLE_MAPS_TOKEN'))

# read in data from CSV
data = pd.read_csv(DIR + 'inter/block-centroid-with-pops-1.csv')
data['store-name-0'] = 'store-name'
data['store-id-0'] = 'id'
data['store-longitude-0'] = 'store-longitude'
data['store-latitude-0'] = 'store-latitude'
data['store-vicinity-0'] = 'vicinity'
data['store-name-1'] = 'store-name'
data['store-id-1'] = 'id'
data['store-longitude-1'] = 'store-longitude'
data['store-latitude-1'] = 'store-latitude'
data['store-vicinity-1'] = 'vicinity'
data['store-name-2'] = 'store-name'
data['store-id-2'] = 'id'
data['store-longitude-2'] = 'store-longitude'
data['store-latitude-2'] = 'store-latitude'
data['store-vicinity-2'] = 'vicinity'
# data['types'] = []

data = data[:5]

# look through rows, extract top 3 search results from google for a given location
# how can we make this faster?
my_type = 'grocery_or_supermarket'
my_language = 'en'

for i in range(5):
	my_location = (data.get_value(i, 'latitude'), data.get_value(i, 'longitude'))
	results = gmaps.places_nearby(my_location, language=my_language, open_now=False, rank_by='distance', type=my_type)

	for j in range(3):
		data = data.set_value(i, 'store-name-' + str(j), results['results'][j]['name'].encode('ascii', 'ignore'))
		data = data.set_value(i, 'store-id-' + str(j), results['results'][j]['id'])
		data = data.set_value(i, 'store-latitude-' + str(j), results['results'][j]['geometry']['location']['lat'])
		data = data.set_value(i, 'store-longitude-' + str(j), results['results'][j]['geometry']['location']['lng'])
		data = data.set_value(i, 'store-vicinity-' + str(j), results['results'][j]['vicinity'].encode('ascii', 'ignore'))

