```
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
  --address            Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)      Display units in miles or kilometers [default: mi]
  --output=(text|json) Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]

Example
  find_store --address="1770 Union St, San Francisco, CA 94123"
  find_store --zip=94115 --units=km
```

This find_store command line will taken in either address string or zip code and get the location point (lat, lng) by
querying Google geocoder API or by looking up zip code location csv. It will then get the closest store location in
store-locations.csv by using the Haversine formula. With the closest store, it will then use Vincenty's formulae
to get the distance in miles or kilometers to print or provide json output for.

Output:
python find_store.py --address='1770 Union St, San Francisco, CA' --units=km
Store Name: San Francisco West
Store Location: SEC Geary Blvd. and Masonic Avenue
Address: 2675 Geary Blvd
City: San Francisco
State: CA
Zip Code: 94118-3400
Distance: 2.393868 kilometers

python find_store.py --address='1770 Union St, San Francisco, CA' --output=json
{'Address': '2675 Geary Blvd',
 'City': 'San Francisco',
 'County': 'San Francisco County',
 'Distance': 1.48748,
 'Distance Units': 'mi',
 'State': 'CA',
 'Store Location': 'SEC Geary Blvd. and Masonic Avenue',
 'Store Name': 'San Francisco West',
 'Zip Code': '94118-3400'}

Test:
python tests.py

Runs tests for distance, closest, get_address_location, vincenty.