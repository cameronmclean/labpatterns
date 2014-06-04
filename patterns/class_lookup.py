import urllib2
import json
import os
from pprint import pprint
import urllib
import copy

REST_URL = "http://data.bioontology.org"
API_KEY = ""

def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + '3d7b2a70-8c4f-4a1e-a1a3-222fdb0be786' )]
    return json.loads(opener.open(url).read())


def lookup(search_terms):
	
	#############################################################################
	# lookup takes a dict of lists as input   search_terms [force name]:[list of terms, .., ... ]
	# returns a horribly nested dict of dicts of dicts (and then some) [forcename]: {[term]: {nsbo JSON}}
	# nesting is complicated mainly due to ncbo JSON object - which we convert to more nested dicts....
	#############################################################################

	# create dict to store and return the results - will actually be a dict of dicts
	matches = {}
				
	# create a temp dict list to store all the results for each force term 
	search_values = {}

	# the following code is verbose and maybe a bit slow, but i left it this way after having to do
	# some crazy debugging 

	forces = search_terms.keys()

	for force in forces:
	#	print "back at top of loop"
		search_values.clear()
	#	print "clearing search_terms list for new force"
	#	print 'force = ' + force
		termList = search_terms[force]
		
	#	print "see whats already in the matches dict at top of loop.."
	#	for a, b in matches.iteritems():
	#		print "at top of loop, matches already contains key .. " + a
	#		for x, y in b.iteritems():
	#			print "at top o floop values in matches currently include .... " + x


		for item in termList:
			lookupResult = {}
			lookupResult.clear()
			print "looking up item " + item
			lookupResult = (get_json(REST_URL + "/search?q=" + urllib.quote_plus(item)))
#			print 'saving result in dict'
			search_values[item] = lookupResult
#			for k, v in search_values.iteritems():
#				print "search value keys are currenty " + k

	#	print "see whats already in the matches dict .."
	#	for a, b in matches.iteritems():
	#		print "matches already contains key .. " + a
	#		for x, y in b.iteritems():
	#			print "values in matches currently include .... " + x

		print "saving dict within dict for matches"
		valuesToSave = copy.deepcopy(search_values)
		matches[force] = valuesToSave

#		for q, w in matches.iteritems():
#			print "matches now has keys " + q
#			for d, f in w.iteritems():
#				print "with terms ..." + d


	return matches


	
	#for force, terms in search_terms.iteritems():
	#	# reset the dict for each force
	#	search_values.clear()
	#	for term in terms:
	#		print "Searching NCBO for " + term
	#		lookupResults = (get_json(REST_URL + "/search?q=" + urllib.quote_plus(term)))
	#		search_values.update({term:lookupResults})
	#	#	for k, v in search_values.iteritems():
	#	#		print "look up search_value key = " + k
	#	#		print type(v)
#	#
#	#	print "we are now outside the term list for loop, and storing the results dict within a dict"
	#	matches.update({force:search_values})

	#print "checking what's being stored in matches"
	
	#for k, v in matches.iteritems():
	#	print "stored match force = " + k
	#	print type(v)
	#	print "above is the type of value in mathches dict"
	#	for item, value in v.iteritems():
	#		print item

		
	#for k, v in matches.iteritems():
	#	print "force matches = " + k
	#	for key, value in v.iteritems():
	#		print "matches search key = " + key


	#for k, v in search_terms.iteritems():
	#	#reset the list, and resuts dict for each force
	#	search_values.clear()
	#	del search_results_list[:]
	#	for word in v:
	#		print "Searching NCBO for " + word
	#		lookupResults = (get_json(REST_URL + "/search?q=" + urllib.quote_plus(word)))
	#		search_values[word] = lookupResults
	#		search_results_list.append(search_values)
	#	matches[k] = search_results_list 

	# loop through the search_terms passes to the funciton
	#for force, word_list in search_terms.items():
	#	# store the foce name as a key in the temp dict, whoes value is an empty dict.
	#	search_results[force] = {}
	#	# for each term, look it up, and append it to the dict whoes key value is the current force name
	#	for item in word_list:
	#		print "Searching NCBO for " + item
	#		search_results[force] = (get_json(REST_URL + "/search?q=" + urllib.quote_plus(item)))
	#	#combine all the results in a new dict of dict to return		
	#	matches = search_results
	
	#print json.dumps(matches, sort_keys=True, indent=4)

#	return matches

#for line in terms_file:
#    terms.append(line)

# Do a search for every term
#search_results = []
#for term in terms:
#    search_results.append(get_json(REST_URL + "/search?q=" + term)["collection"])

# Print the results
#	for result in search_results:
#    	pprint(result)