import sys
import unittest
from datetime import date, datetime
from unittest.mock import patch

from loan_calculation import loan_calculation


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "totalLoan": 5890123,
            "mrr": 8.25,
            "mrrInAccount": -4,
            "day": 25
        }

    @unittest.skip("test")
    def testSkip(self):
        pass

    @unittest.skipIf(date.today().year > 2020, "own_version")
    def testLoan(self):
        print("own version ")
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def testOnlyWins(self):
        print("Windows version ")
        pass

    @patch('datetime.date')
    def test_loan_calculation(self, mock_date):
        mock_date.today.return_value = date(2024, 6, 28)

        result = loan_calculation(self.payload)

        expected_value = 231.78724768518518
        print(f"result {result}")
        self.assertAlmostEqual(result, expected_value, places=2)

    @patch('datetime.datetime')
    @patch('datetime.date')
    def test_loan_calculation_fail(self, mock_date, mock_datetime):
        mock_date.today.return_value = date(2024, 7, 23)
        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)
        self.payload['totalLoan'] = -10000
        with self.assertRaises(ValueError):
            loan_calculation(self.payload)


if __name__ == '__main__':
    unittest.main()
