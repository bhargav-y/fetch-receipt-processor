import unittest
from receipt_processor import compute_purchase_time_points, compute_item_description_points, compute_points

class TestPointCalculation(unittest.TestCase):

    def test_compute_purchase_time_points_in_range(self):
        time = '14:33'

        points = compute_purchase_time_points(time)
        self.assertEqual(points, 10)
    
    def test_compute_purchase_time_points_on_boundary(self):
        time = '14:00'
        
        points = compute_purchase_time_points(time)
        self.assertEqual(points, 10)

    def test_compute_purchase_time_points_outside(self):
        time = '17:30'

        points = compute_purchase_time_points(time)
        self.assertEqual(points, 0)

    def test_compute_item_description_points(self):
        items = [
            {"shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
            },{
            "shortDescription": "Emils Cheese Pizza",
            "price": "12.25"
            },{
            "shortDescription": "Knorr Creamy Chicken",
            "price": "1.26"
            },{
            "shortDescription": "Doritos Nacho Cheese",
            "price": "3.35"
            },{
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00"}
        ]

        points = compute_item_description_points(items)
        self.assertEqual(points, 6)

    def test_compute_points_simple(self):
        retailer = "Target" # points -> 6
        purchase_date = "2022-01-02" # points -> 0
        purchase_time = "13:13" # points -> 0
        items = [
            {"shortDescription": "Pepsi - 12-oz", 
             "price": "1.25"}
        ] # points -> 0
        total = "1.25" # points -> 25

        points = compute_points(retailer, total, purchase_date, purchase_time, items)
        self.assertEqual(points, 31)

    def test_compute_points_custom(self):
        # Test using unique data
        retailer = "Walmart" # points -> 7
        purchase_date = "2022-01-02" # points -> 0
        purchase_time = "15:22" # points -> 10
        items = [
            {"shortDescription": "   aaa ",
            "price": "3.45"
            },{
            "shortDescription": "bbbb",
            "price": "4.98"
            },{
            "shortDescription": "cccccc",
            "price": "7.23"}
        ] # points -> 1 + 2 + 5 = 8
        total = "6.00" # points -> 75 points

        points = compute_points(retailer, total, purchase_date, purchase_time, items)
        self.assertEqual(points, 100)

if __name__ == '__main__':
    unittest.main()
