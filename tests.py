import unittest
from distance import distance, closest
from geocoder import get_address_location
from vincenty import vincenty

class FindStoreTestCase(unittest.TestCase):

    def test_distance(self):
        assert distance(39.7612992, -86.1519681, 39.7622290, -86.1519750) == 0.10339070310220466

    def test_closest(self):
        tempDataList = [(39.7612992, -86.1519681),
                        (39.762241, -86.158436),
                        (39.7622292, -86.1578917)]
        v = (39.7622290, -86.1519750)
        assert closest(tempDataList, v) == (39.7612992, -86.1519681)

    def test_get_address_location(self):
        assert get_address_location('1770 Union St, San Francisco, CA') == (37.79823040000001, -122.4284337)

    def test_vincenty_miles(self):
        assert vincenty((37.79823040000001, -122.4284337), (37.7820964,-122.4464697), miles=True) == 1.48748

    def test_vincenty_km(self):
        assert vincenty((37.79823040000001, -122.4284337), (37.7820964, -122.4464697)) == 2.393868

if __name__ == '__main__':
    unittest.main()