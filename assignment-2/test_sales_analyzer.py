import unittest
import tempfile
import os
from datetime import datetime
from sales_analyzer import SalesAnalyzer, SalesRecord


class TestSalesAnalyzer(unittest.TestCase):
    """Test cases for SalesAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SalesAnalyzer()
        
        # Create temporary CSV file
        self.test_csv_data = """order_id,date,customer_id,customer_name,product_category,product_name,quantity,unit_price,total_price,region,payment_method
1001,2024-01-15,C001,John Smith,Electronics,Laptop,1,1200.00,1200.00,North,Credit Card
1002,2024-01-16,C002,Emma Johnson,Clothing,Jacket,2,89.99,179.98,South,PayPal
1003,2024-01-16,C003,Michael Brown,Electronics,Smartphone,1,799.99,799.99,East,Credit Card
1004,2024-01-17,C001,John Smith,Books,Python Programming,3,45.50,136.50,North,Credit Card
1005,2024-01-18,C004,Sarah Davis,Home & Garden,Coffee Maker,1,79.99,79.99,West,Debit Card
1006,2024-01-19,C005,James Wilson,Electronics,Headphones,2,149.99,299.98,North,Credit Card
1007,2024-01-20,C002,Emma Johnson,Books,Data Science Guide,1,55.00,55.00,South,PayPal
1008,2024-01-21,C006,Lisa Anderson,Clothing,Dress,1,120.00,120.00,East,Credit Card
1009,2024-01-22,C003,Michael Brown,Electronics,Tablet,1,499.99,499.99,East,Debit Card
1010,2024-01-23,C007,Robert Taylor,Home & Garden,Blender,2,59.99,119.98,West,Credit Card"""
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file.write(self.test_csv_data)
        self.temp_file.close()
        
        # Load data
        self.analyzer.load_data(self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_data(self):
        """Test data loading."""
        self.assertEqual(len(self.analyzer.sales_data), 10)
        self.assertIsInstance(self.analyzer.sales_data[0], SalesRecord)
    
    def test_calculate_total_revenue(self):
        """Test total revenue calculation using reduce."""
        total_revenue = self.analyzer.calculate_total_revenue()
        self.assertAlmostEqual(total_revenue, 3491.41, places=2)
    
    def test_calculate_average_order_value(self):
        """Test average order value calculation."""
        avg_order_value = self.analyzer.calculate_average_order_value()
        self.assertAlmostEqual(avg_order_value, 349.141, places=2)
    
    def test_get_total_sales_by_category(self):
        """Test sales aggregation by category."""
        sales_by_category = self.analyzer.get_total_sales_by_category()
        
        self.assertIsInstance(sales_by_category, dict)
        self.assertEqual(len(sales_by_category), 4)
        self.assertIn('Electronics', sales_by_category)
        self.assertIn('Clothing', sales_by_category)
        self.assertIn('Books', sales_by_category)
        self.assertIn('Home & Garden', sales_by_category)
        
        # Electronics should have highest sales
        self.assertGreater(sales_by_category['Electronics'], 2700.0)
    
    def test_get_total_sales_by_region(self):
        """Test sales aggregation by region."""
        sales_by_region = self.analyzer.get_total_sales_by_region()
        
        self.assertIsInstance(sales_by_region, dict)
        self.assertEqual(len(sales_by_region), 4)
        self.assertIn('North', sales_by_region)
        self.assertIn('South', sales_by_region)
        self.assertIn('East', sales_by_region)
        self.assertIn('West', sales_by_region)
    
    def test_get_order_count_by_payment_method(self):
        """Test order counting by payment method."""
        order_count = self.analyzer.get_order_count_by_payment_method()
        
        self.assertIsInstance(order_count, dict)
        self.assertIn('Credit Card', order_count)
        self.assertIn('PayPal', order_count)
        self.assertIn('Debit Card', order_count)
        
        # Verify counts add up to total
        self.assertEqual(sum(order_count.values()), 10)
    
    def test_get_top_customers(self):
        """Test top customers by spending using sorting."""
        top_customers = self.analyzer.get_top_customers(3)
        
        self.assertIsInstance(top_customers, list)
        self.assertLessEqual(len(top_customers), 3)
        
        # Verify sorted in descending order
        if len(top_customers) > 1:
            for i in range(len(top_customers) - 1):
                self.assertGreaterEqual(top_customers[i][1], top_customers[i + 1][1])
        
        # John Smith should be top customer
        self.assertEqual(top_customers[0][0], "John Smith")
    
    def test_get_top_products_by_quantity(self):
        """Test top products by quantity using lambda for sorting."""
        top_products = self.analyzer.get_top_products_by_quantity(5)
        
        self.assertIsInstance(top_products, list)
        self.assertLessEqual(len(top_products), 5)
        
        # Verify sorted in descending order
        if len(top_products) > 1:
            for i in range(len(top_products) - 1):
                self.assertGreaterEqual(top_products[i][1], top_products[i + 1][1])
    
    def test_get_top_products_by_revenue(self):
        """Test top products by revenue."""
        top_products = self.analyzer.get_top_products_by_revenue(5)
        
        self.assertIsInstance(top_products, list)
        self.assertLessEqual(len(top_products), 5)
        
        # Laptop should be #1
        self.assertEqual(top_products[0][0], "Laptop")
        self.assertAlmostEqual(top_products[0][1], 1200.00, places=2)
    
    def test_get_monthly_revenue(self):
        """Test monthly revenue aggregation."""
        monthly_revenue = self.analyzer.get_monthly_revenue()
        
        self.assertIsInstance(monthly_revenue, dict)
        self.assertIn('2024-01', monthly_revenue)
        
        # All sales are in January 2024
        self.assertEqual(len(monthly_revenue), 1)
    
    def test_get_average_order_value_by_category(self):
        """Test average order value calculation by category."""
        avg_by_category = self.analyzer.get_average_order_value_by_category()
        
        self.assertIsInstance(avg_by_category, dict)
        self.assertGreater(len(avg_by_category), 0)
        
        # All averages should be positive
        for avg in avg_by_category.values():
            self.assertGreater(avg, 0)
    
    def test_get_orders_above_threshold_with_filter(self):
        """Test filtering orders above threshold using lambda."""
        high_value_orders = self.analyzer.get_orders_above_threshold(500.0)
        
        self.assertIsInstance(high_value_orders, list)
        
        # Verify all orders are above threshold
        for order in high_value_orders:
            self.assertGreater(order.total_price, 500.0)
        
        # Should be sorted in descending order
        if len(high_value_orders) > 1:
            for i in range(len(high_value_orders) - 1):
                self.assertGreaterEqual(high_value_orders[i].total_price, 
                                       high_value_orders[i + 1].total_price)
    
    def test_get_customer_purchase_frequency(self):
        """Test customer purchase frequency counting."""
        frequency = self.analyzer.get_customer_purchase_frequency()
        
        self.assertIsInstance(frequency, dict)
        self.assertGreater(len(frequency), 0)
        
        # John Smith has 2 orders
        self.assertEqual(frequency['John Smith'], 2)
        
        # Emma Johnson has 2 orders
        self.assertEqual(frequency['Emma Johnson'], 2)
    
    def test_get_quantity_sold_by_category(self):
        """Test quantity aggregation by category."""
        quantity_by_category = self.analyzer.get_quantity_sold_by_category()
        
        self.assertIsInstance(quantity_by_category, dict)
        self.assertGreater(len(quantity_by_category), 0)
        
        # All quantities should be positive
        for qty in quantity_by_category.values():
            self.assertGreater(qty, 0)
    
    def test_get_revenue_by_region_and_category(self):
        """Test multi-level grouping (region and category)."""
        revenue_by_region_category = self.analyzer.get_revenue_by_region_and_category()
        
        self.assertIsInstance(revenue_by_region_category, dict)
        self.assertGreater(len(revenue_by_region_category), 0)
        
        # North region should have data
        self.assertIn('North', revenue_by_region_category)
        
        # North should have Electronics
        self.assertIn('Electronics', revenue_by_region_category['North'])
    
    def test_get_distinct_customers_count(self):
        """Test distinct customer counting using map."""
        distinct_customers = self.analyzer.get_distinct_customers_count()
        
        self.assertEqual(distinct_customers, 7)
    
    def test_get_revenue_statistics(self):
        """Test statistics summary."""
        stats = self.analyzer.get_revenue_statistics()
        
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['count'], 10)
        self.assertAlmostEqual(stats['sum'], 3491.41, places=2)
        self.assertAlmostEqual(stats['min'], 55.00, places=2)
        self.assertAlmostEqual(stats['max'], 1200.00, places=2)
        self.assertAlmostEqual(stats['average'], 349.141, places=2)
        self.assertGreater(stats['std_dev'], 0)
    
    def test_apply_discount_higher_order_function(self):
        """Test higher-order function with custom discount logic."""
        # 10% discount on all items
        discount_fn = lambda record: record.total_price * 0.1
        
        discounted = self.analyzer.apply_discount(discount_fn)
        
        self.assertEqual(len(discounted), 10)
        
        # Verify discount applied
        for order_id, original, discounted_price in discounted:
            self.assertAlmostEqual(discounted_price, original * 0.9, places=2)
    
    def test_apply_conditional_discount(self):
        """Test conditional discount using lambda."""
        # 20% discount on Electronics, 10% on others
        discount_fn = lambda record: (
            record.total_price * 0.2 if record.product_category == 'Electronics'
            else record.total_price * 0.1
        )
        
        discounted = self.analyzer.apply_discount(discount_fn)
        
        # Find an electronics item
        electronics_found = False
        for order_id, original, discounted_price in discounted:
            record = next(r for r in self.analyzer.sales_data if r.order_id == order_id)
            if record.product_category == 'Electronics':
                electronics_found = True
                self.assertAlmostEqual(discounted_price, original * 0.8, places=2)
        
        self.assertTrue(electronics_found)
    
    def test_filter_and_transform_composition(self):
        """Test function composition with filter and map."""
        # Filter Electronics and transform to product names
        result = self.analyzer.filter_and_transform(
            filter_fn=lambda r: r.product_category == 'Electronics',
            transform_fn=lambda r: r.product_name
        )
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # All should be electronics product names
        electronics_products = ['Laptop', 'Smartphone', 'Headphones', 'Tablet']
        for product in result:
            self.assertIn(product, electronics_products)
    
    def test_empty_dataset(self):
        """Test with empty dataset."""
        empty_analyzer = SalesAnalyzer()
        
        self.assertEqual(empty_analyzer.calculate_total_revenue(), 0.0)
        self.assertEqual(empty_analyzer.calculate_average_order_value(), 0.0)
        self.assertEqual(empty_analyzer.get_distinct_customers_count(), 0)

class TestSalesRecord(unittest.TestCase):
    """Test cases for SalesRecord dataclass."""
    
    def test_sales_record_creation(self):
        """Test SalesRecord creation."""
        record = SalesRecord(
            order_id='1001',
            date=datetime(2024, 1, 15),
            customer_id='C001',
            customer_name='John Smith',
            product_category='Electronics',
            product_name='Laptop',
            quantity=1,
            unit_price=1200.00,
            total_price=1200.00,
            region='North',
            payment_method='Credit Card'
        )
        
        self.assertEqual(record.order_id, '1001')
        self.assertEqual(record.customer_name, 'John Smith')
        self.assertEqual(record.total_price, 1200.00)
    
    def test_sales_record_string_representation(self):
        """Test SalesRecord __str__ method."""
        record = SalesRecord(
            order_id='1001',
            date=datetime(2024, 1, 15),
            customer_id='C001',
            customer_name='John Smith',
            product_category='Electronics',
            product_name='Laptop',
            quantity=1,
            unit_price=1200.00,
            total_price=1200.00,
            region='North',
            payment_method='Credit Card'
        )
        
        str_repr = str(record)
        self.assertIn('1001', str_repr)
        self.assertIn('Laptop', str_repr)
        self.assertIn('1200.00', str_repr)


def suite():
    """Create test suite."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSalesAnalyzer))
    test_suite.addTest(unittest.makeSuite(TestSalesRecord))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())