from app import app
import unittest


class APITest(unittest.TestCase):

    def test_hello_world(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)
    
    def test_rate_valid_different_regions_ports(self):
        port_and_regions_queries = {
            "port_code_upper": "?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=IEDUB",
            "port_code__lower": "?date_from=2016-01-01&date_to=2016-01-10&origin=cnsgh&destination=iedub",
            "slug_upper": "?date_from=2016-01-01&date_to=2016-01-10&origin=POLAND_MAIN&destination=north_europe_main",
            "slug_lower": "?date_from=2016-01-01&date_to=2016-01-10&origin=scandinavia&destination=north_europe_main",
            "region_upper": "?date_from=2016-01-01&date_to=2016-01-10&origin=CHINA_MAIN&destination=NORTHERN_EUROPE",
            "region_lower": "?date_from=2016-01-01&date_to=2016-01-10&origin=baltic&destination=northern_europe"
        }

        tester = app.test_client(self)
        for k, v in port_and_regions_queries.items():
            response = tester.get(f"/rates{v}")
            status_code = response.status_code
            self.assertEqual(status_code, 200)

    def test_rate_invalid_parameter(self):
        ivalid_queries = {
            "missing_from_date": "?date_from=&date_to=2016-01-10&origin=CNSGH&destination=IEDUB",
            "missing_to_date": "?date_from=2016-01-01&date_to=&origin=poland_main&destination=iedub",
            "missing_origin": "?date_from=2016-01-01&date_to=2016-01-10&origin=&destination=north_europe_main",
            "missing_destination": "?date_from=2016-01-01&date_to=2016-01-10&origin=scandinavia&destination=",
            "incorrect_origin": "?date_from=2016-01-01&date_to=2016-01-10&origin=sopaq&destination=NORTHERN_EUROPE",
            "incorrect_destination": "?date_from=2016-01-01&date_to=2016-01-10&origin=china_main&destination=odsps"
        }

        tester = app.test_client(self)
        for k, v in ivalid_queries.items():
            response = tester.get(f"/rates{v}")
            status_code = response.status_code
            self.assertEqual(status_code, 400)

if __name__ == "__main__":
    unittest.main()