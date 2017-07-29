import requests

def get_address_location(address):
    address_string = '+'.join(address.split(' '))
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + address_string + "'")
    resp_json_payload = response.json()
    if resp_json_payload:
        location = resp_json_payload['results'][0]['geometry']['location']
        if location:
            if 'lat' in location and 'lng' in location:
                return (location['lat'], location['lng'])
            else:
                return None
