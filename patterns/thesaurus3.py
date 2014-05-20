
# Modified From https://gist.github.com/hugorodgerbrown/3134709

'''
Command line script used to grab synonyms off the web using a thesaurus api.

The words come from the "Big Huge Thesaurus", and I make no claims about the 
results. In order to use this script you will need a valid API key, which is
available, for free (up to 10,000 calls / day), from here - http://words.bighugelabs.com/getkey.php
If you're really lazy, you can just use my key - eb4e57bb2c34032da68dfeb3a0578b68
but I'd rather you didn't. Thanks.

Examples:

python thesaurus.py sad
python thesaurus.py sad happy
python thesaurus.py sad --out file.txt
python thesaurus.py sad --key eb4e57bb2c34032da68dfeb3a0578b68

Created: 17-July-2012
Author: Hugo Rodger-Brown

'''
import sys
import json
import requests
import argparse
from os import path

API_KEY = 'b03a851ef1f9ac808b34836729d570d6' # API key is available from here - http://words.bighugelabs.com/getkey.php
URL_MASK = 'http://words.bighugelabs.com/api/2/{1}/{0}/json'
RELATIONSHIP_ABBR = {'syn':'Synonyms','ant':'Antonyms','rel':'Related terms','sim':'Similar terms','usr':'User suggestions'}
VALID_FILE_EXTENSIONS = ['.txt','.csv','.json','.js']

def lookup_word(word):
    ''' Performs the lookup of a given word against the thesaurus API 

    :param word: the word to look up
    :returns: all matching synonyms, related terms, similar terms as a combined list
    
    '''

    url = URL_MASK.format(word, API_KEY)

    r = requests.get(url)
    # check to see if r is empty/doesnt exist - i.e hte url request returned no text. if r is empty/non existent, create and return a blank dict
    if not r:
      j = {}
      print 'no matches for %s found' % word
      return j


    j = json.loads(r.text)


    return j

#parser = argparse.ArgumentParser(description='Use online thesaurus to look up synonyms, antonyms etc.')
#parser.add_argument('words', action='store', help='words to look up in the thesaurus (space delimited)', nargs='+')
#parser.add_argument('--out','-o', action='store', help='If set then the output will be written to a file. Output format is set from the file extension [.json|.csv]')
#parser.add_argument('--key','-k', action='store', help='If set will override the API_KEY value in the script, and be used to authenticate API calls.')
#args = parser.parse_args()

#if args.key:
#    API_KEY = args.key
#elif API_KEY == '<your_key_goes_here>':
#    raise Exception('Invalid API_KEY - test keys are available from http://words.bighugelabs.com/getkey.php')
#    sys.exit()

def get_all(input_string):
    # need to parse input_string space delim, sore as list, then iterate over list.
    all_words = input_string.split(" ")
    total_words_of_interest = []
    term = {}
    for word in all_words:
        print '\nLooking up words related to \'{0}\'\n'.format(word)
        term = lookup_word(word)
        #get all the keys to the dict - 'adjective, 'noun' etc....
        key = term.keys()
        syn = []
        sim = []
        rel = []
        #for every key in the dict (noun, adjective etc...) check to see if there is a list similar, synonym, or related words. if so, store them in a list.
        for item in key:
            if 'syn' in term[item]:
                syn = term[item]['syn']
            if 'sim' in term[item]:
                sim = term[item]['sim']
            if 'rel' in term[item]:
                rel = term[item]['rel']
        #print syn, sim, rel
        # add together the lists of related words
        related_words = syn+sim+rel
        # append related terms for each word in the initial term/query
        total_words_of_interest = total_words_of_interest+related_words
        #print total_words_of_interest
    return total_words_of_interest

