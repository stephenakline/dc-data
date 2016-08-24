import os
import googlemaps
import progressbar
import time
import pandas as pd

DIR   = os.getcwd()
gmaps = googlemaps.Client(key = os.environ.get('GOOGLE_MAPS_TOKEN'))
bar = progressbar.ProgressBar()
number_stores = 3

# read in data from CSV
data = pd.read_csv(DIR + '/inter/block-centroid-with-pops-1.csv')

for j in range(number_stores):
	data['store-name-' + str(j)] = 'store-name'
	data['store-id-' + str(j)] = 'id'
	data['store-longitude-' + str(j)] = 'store-longitude'
	data['store-latitude-' + str(j)] = 'store-latitude'
	data['store-vicinity-' + str(j)] = 'vicinity'

data = data[:75]

# look through rows, extract top 3 search results from google for a given location
# how can we make this faster?
my_type = 'grocery_or_supermarket'
my_language = 'en'

print 'status bar:'
for i in bar(range(75)):
	my_location = (data.get_value(i, 'latitude'), data.get_value(i, 'longitude'))
	results = gmaps.places_nearby(my_location, language=my_language, open_now=False, rank_by='distance', type=my_type)

	for j in range(number_stores):
		data = data.set_value(i, 'store-name-' + str(j), results['results'][j]['name'].encode('ascii', 'ignore'))
		data = data.set_value(i, 'store-id-' + str(j), results['results'][j]['id'])
		data = data.set_value(i, 'store-latitude-' + str(j), results['results'][j]['geometry']['location']['lat'])
		data = data.set_value(i, 'store-longitude-' + str(j), results['results'][j]['geometry']['location']['lng'])
		data = data.set_value(i, 'store-vicinity-' + str(j), results['results'][j]['vicinity'].encode('ascii', 'ignore'))

	time.sleep(0.1)

file_name = DIR + '/inter/stores-near-block-centroid-1.csv'
data.to_csv(file_name, sep = ',')
