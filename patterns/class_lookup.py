import urllib2
import json
import os
from pprint import pprint
import urllib

REST_URL = "http://data.bioontology.org"
API_KEY = ""

def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + '3d7b2a70-8c4f-4a1e-a1a3-222fdb0be786' )]
    return json.loads(opener.open(url).read())


def lookup(search_terms):
	
	# lookup takes a dict of lists as input search_terms[force name][list of terms]

	# create dict to store and return the results - will actually be a dict of dicts
	matches = {}
				
	# create a temp dict to store the results
	search_results = {}
	# loop through the search_terms passes to the funciton
	for force, word_list in search_terms.iteritems():
		# store the foce name as a key in the temp dict, whoes value is an empty dict.
		search_results[force] = {}
		# for each term, look it up, and append it to the dict whoes key value is the current force name
		for item in word_list:
			print "Searching NCBO for " + item
			search_results[force] = (get_json(REST_URL + "/search?q=" + urllib.quote_plus(item)))
		#combine all the results in a new dict of dict to return		
		matches = search_results
	
	#print json.dumps(matches, sort_keys=True, indent=4)

	return matches

#for line in terms_file:
#    terms.append(line)

# Do a search for every term
#search_results = []
#for term in terms:
#    search_results.append(get_json(REST_URL + "/search?q=" + term)["collection"])

# Print the results
#	for result in search_results:
#    	pprint(result)