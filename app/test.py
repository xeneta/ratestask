from app import app
import unittest


class APITest(unittest.TestCase):

    def test_hello_world(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)
    
    def test_rate_1(self):
        tester = app.test_client(self)
        response = tester.get("/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main")
        status_code = response.status_code
        print(response.data)
        self.assertEqual(status_code, 200)

if __name__ == "__main__":
    unittest.main()