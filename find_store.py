#! /usr/bin/env python
"""
Find Store
  find_store will locate the nearest store (as the vrow flies) from
  store-locations.csv, print the matching store address, as well as
  the distance to that store.

Usage:
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]

Options:
  --zip=<zip>          Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address=<address>  Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)      Display units in miles or kilometers [default: mi]
  --output=(text|json) Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]
  -v, --version               shows the version

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
"""

import csv
import sys

from docopt import docopt

from geocoder import get_address_location
from distance import closest
from pprint import pprint
from vincenty import vincenty

stores = []
store_locations = []
zip_codes = {}

def read_stores():
    with open('store-locations.csv', 'rU') as csvfile:
        fieldnames = ['Store Name', 'Store Location', 'Address', 'City', 'State', 'Zip Code', 'Latitude', 'Longitude',
                      'County']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for i, row in enumerate(reader):
            if i > 0:
                stores.append({
                    'Store Name': row['Store Name'],
                    'Store Location': row['Store Location'],
                    'Address': row['Address'],
                    'City': row['City'],
                    'State': row['State'],
                    'Zip Code': row['Zip Code'],
                    'County': row['County'],
                })
                store_locations.append((float(row['Latitude']), float(row['Longitude'])))

def read_zip_codes():
    with open('zip-codes.csv', 'rU') as csvfile:
        fieldnames = ['Zip Code', 'Latitude', 'Longitude']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for i, row in enumerate(reader):
            if i > 0:
                zip_codes[int(row['Zip Code'])] = (float(row['Latitude']), float(row['Longitude']))

def print_store(store, distance_str):
    print 'Store Name: {}\n' \
          'Store Location: {}\n' \
          'Address: {}\n' \
          'City: {}\n' \
          'State: {}\n' \
          'Zip Code: {}\n' \
          'Distance: {}'.format(store['Store Name'],
                                  store['Store Location'],
                                  store['Address'],
                                  store['City'],
                                  store['State'],
                                  store['Zip Code'],
                                  distance_str)

def get_closes_store_idx(location):
    store_location = closest(store_locations, location)
    return store_locations.index(store_location)

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0')
    read_stores()
    if args['--address']:
        location = get_address_location(args['--address'])
        if not location:
            print "Usage: --address=<address> must be valid address string."
            sys.exit(1)


    if args['--zip']:
        try:
            input_zip_code = int(args['--zip'])
        except ValueError:
            print "Usage: --zip=<zip> must be a valid integer zipcode."
            sys.exit(1)
        read_zip_codes()
        try:
            location = zip_codes[input_zip_code]
        except KeyError:
            # Get closest known zip code
            zip_code = min(zip_codes.keys(), key=lambda x:abs(x-input_zip_code))
            location = zip_codes[input_zip_code]

    store_idx = get_closes_store_idx(location)

    if args['--units'] == 'km':
        distance = vincenty(location, store_locations[store_idx])
        distance_str = '{} kilometers'.format(distance)
    else:
        distance = vincenty(location, store_locations[store_idx], miles=True)
        distance_str = '{} miles'.format(distance)

    if args['--output'] == 'json':
        store_json = dict(stores[store_idx])
        store_json.update({'Distance': distance})
        if args['--units'] == 'km':
            store_json.update({'Distance Units': 'km'})
        else:
            store_json.update({'Distance Units': 'mi'})
        pprint(store_json)
    else:
        print_store(stores[store_idx], distance_str)
