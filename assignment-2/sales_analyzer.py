import csv
from datetime import datetime
from functools import reduce
from typing import List, Dict, Tuple, Callable
from collections import defaultdict
from dataclasses import dataclass
import statistics


@dataclass(frozen=True)
class SalesRecord:
    """Immutable sales record representing a single transaction."""
    order_id: str
    date: datetime
    customer_id: str
    customer_name: str
    product_category: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float
    region: str
    payment_method: str
    
    def __str__(self):
        return f"Order {self.order_id}: {self.product_name} - ${self.total_price:.2f}"


class SalesAnalyzer:
    """Sales data analyzer using functional programming paradigms."""
    
    def __init__(self):
        self.sales_data: List[SalesRecord] = []
    
    def load_data(self, file_path: str) -> None:
        """Load sales data from CSV file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.sales_data = list(map(self._parse_row, reader))
        
        # Filter out any None values from parsing errors
        self.sales_data = list(filter(lambda x: x is not None, self.sales_data))
    
    def _parse_row(self, row: Dict[str, str]) -> SalesRecord:
        """Parse a CSV row into a SalesRecord."""
        try:
            return SalesRecord(
                order_id=row['order_id'],
                date=datetime.strptime(row['date'], '%Y-%m-%d'),
                customer_id=row['customer_id'],
                customer_name=row['customer_name'],
                product_category=row['product_category'],
                product_name=row['product_name'],
                quantity=int(row['quantity']),
                unit_price=float(row['unit_price']),
                total_price=float(row['total_price']),
                region=row['region'],
                payment_method=row['payment_method']
            )
        except (KeyError, ValueError) as e:
            print(f"Error parsing row: {e}")
            return None
    
    def calculate_total_revenue(self) -> float:
        """Calculate total revenue using reduce."""
        return reduce(
            lambda acc, record: acc + record.total_price,
            self.sales_data,
            0.0
        )
    
    def calculate_average_order_value(self) -> float:
        """Calculate average order value."""
        if not self.sales_data:
            return 0.0
        return self.calculate_total_revenue() / len(self.sales_data)
    
    # Helper function
    def group_sum(self, key_fn: Callable, value_fn: Callable) -> Dict:
        """Generic function to sum values grouped by a key."""
        result = defaultdict(float)
        for record in self.sales_data:
            result[key_fn(record)] += value_fn(record)
        return dict(result)

    
    def get_total_sales_by_category(self) -> Dict[str, float]:
        """Find total sales by category using functional approach."""
        return self.group_sum(
        key_fn=lambda r: r.product_category,
        value_fn=lambda r: r.total_price
    )
    
    def get_total_sales_by_region(self) -> Dict[str, float]:
        """Find total sales by region."""
        return self.group_sum(
        key_fn=lambda r: r.region,
        value_fn=lambda r: r.total_price
    )

    def get_quantity_sold_by_category(self) -> Dict[str, int]:
        """Get total quantity sold by category."""
        return self.group_sum(
        key_fn=lambda r: r.product_category,
        value_fn=lambda r: r.quantity
    )
    
    def get_revenue_by_region_and_category(self) -> Dict[str, Dict[str, float]]:
        """Calculate revenue per region per category (multi-level grouping)."""
        result = defaultdict(lambda: defaultdict(float))
        
        for record in self.sales_data:
            result[record.region][record.product_category] += record.total_price
        
        # Convert to regular dict
        return {
            region: dict(categories)
            for region, categories in result.items()
        }
    
    def get_order_count_by_payment_method(self) -> Dict[str, int]:
        """Count orders by payment method."""
        payment_counts = defaultdict(int)
        
        for record in self.sales_data:
            payment_counts[record.payment_method] += 1
        
        return dict(payment_counts)
    
    # Helper function
    def top_n(self, key_fn: Callable, value_fn: Callable, n: int):
        """Generic function to compute top-N based on aggregated values."""
        agg = defaultdict(float)
        for record in self.sales_data:
            agg[key_fn(record)] += value_fn(record)

        return sorted(
            agg.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n]
    
    def get_top_customers(self, n: int = 10) -> List[Tuple[str, float]]:
        """Find top N customers by total spending."""
        return self.top_n(
        key_fn=lambda r: r.customer_name,
        value_fn=lambda r: r.total_price,
        n=n
    )
    
    def get_top_products_by_quantity(self, n: int = 10) -> List[Tuple[str, int]]:
        """Find top N products by quantity sold."""
        return self.top_n(
        key_fn=lambda r: r.product_name,
        value_fn=lambda r: r.quantity,
        n=n
    )
    
    def get_top_products_by_revenue(self, n: int = 10) -> List[Tuple[str, float]]:
        """Find top N products by revenue."""
        return self.top_n(
        key_fn=lambda r: r.product_name,
        value_fn=lambda r: r.total_price,
        n=n
    )
    
    def get_monthly_revenue(self) -> Dict[str, float]:
        """Calculate monthly revenue."""
        monthly_revenue = defaultdict(float)
        
        for record in self.sales_data:
            month_key = record.date.strftime('%Y-%m')
            monthly_revenue[month_key] += record.total_price
        
        return dict(monthly_revenue)
    
    def get_average_order_value_by_category(self) -> Dict[str, float]:
        """Get average order value by category."""
        category_totals = defaultdict(float)
        category_counts = defaultdict(int)
        
        for record in self.sales_data:
            category_totals[record.product_category] += record.total_price
            category_counts[record.product_category] += 1
        
        return {
            category: category_totals[category] / category_counts[category]
            for category in category_totals
        }
    
    def get_orders_above_threshold(self, threshold: float) -> List[SalesRecord]:
        """Find orders above a certain threshold using filter."""
        return sorted(
            filter(lambda record: record.total_price > threshold, self.sales_data),
            key=lambda record: record.total_price,
            reverse=True
        )
    
    def get_customer_purchase_frequency(self) -> Dict[str, int]:
        """Get customer purchase frequency."""
        frequency = defaultdict(int)
        
        for record in self.sales_data:
            frequency[record.customer_name] += 1
        
        return dict(frequency)
    
    def get_distinct_customers_count(self) -> int:
        """Find distinct customers count."""
        return len(set(map(lambda record: record.customer_id, self.sales_data)))
    
    def get_revenue_statistics(self) -> Dict[str, float]:
        """Get statistics summary."""
        if not self.sales_data:
            return {
                'count': 0, 'sum': 0.0, 'min': 0.0, 
                'max': 0.0, 'average': 0.0, 'std_dev': 0.0
            }
        
        revenues = list(map(lambda r: r.total_price, self.sales_data))
        
        return {
            'count': len(revenues),
            'sum': sum(revenues),
            'min': min(revenues),
            'max': max(revenues),
            'average': statistics.mean(revenues),
            'std_dev': statistics.stdev(revenues) if len(revenues) > 1 else 0.0
        }
    
    def apply_discount(self, discount_fn: Callable[[SalesRecord], float]) -> List[Tuple[str, float, float]]:
        """
        Apply a discount function to all records (demonstrates higher-order functions).
        Returns list of (order_id, original_price, discounted_price).
        """
        return list(map(
            lambda record: (
                record.order_id,
                record.total_price,
                record.total_price - discount_fn(record)
            ),
            self.sales_data
        ))
    
    def filter_and_transform(
        self,
        filter_fn: Callable[[SalesRecord], bool],
        transform_fn: Callable[[SalesRecord], any]
    ) -> List[any]:
        """
        Generic filter and transform using functional composition.
        Demonstrates function composition and higher-order functions.
        """
        return list(map(transform_fn, filter(filter_fn, self.sales_data)))
    
    def display_all_analyses(self) -> None:
        """Display all analyses with formatted output."""
        print("SALES DATA ANALYSIS RESULTS")
        
        # 1. Total Revenue
        print("\n1. TOTAL REVENUE")
        print(f"Total Revenue: ${self.calculate_total_revenue():.2f}")
        
        # 2. Average Order Value
        print("\n2. AVERAGE ORDER VALUE")
        print(f"Average Order Value: ${self.calculate_average_order_value():.2f}")
        
        # 3. Sales by Category
        print("\n3. TOTAL SALES BY CATEGORY")
        category_sales = self.get_total_sales_by_category()
        for category, sales in sorted(category_sales.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:<20}: ${sales:>10.2f}")
        
        # 4. Sales by Region
        print("\n4. TOTAL SALES BY REGION")
        region_sales = self.get_total_sales_by_region()
        for region, sales in sorted(region_sales.items(), key=lambda x: x[1], reverse=True):
            print(f"{region:<20}: ${sales:>10.2f}")
        
        # 5. Payment Methods
        print("\n5. ORDER COUNT BY PAYMENT METHOD")
        payment_counts = self.get_order_count_by_payment_method()
        for method, count in sorted(payment_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{method:<20}: {count:>10} orders")
        
        # 6. Top Customers
        print("\n6. TOP 10 CUSTOMERS BY SPENDING")
        for customer, spending in self.get_top_customers(10):
            print(f"{customer:<20}: ${spending:>10.2f}")
        
        # 7. Top Products by Quantity
        print("\n7. TOP 10 PRODUCTS BY QUANTITY SOLD")
        for product, quantity in self.get_top_products_by_quantity(10):
            print(f"{product:<25}: {quantity:>8} units")
        
        # 8. Top Products by Revenue
        print("\n8. TOP 10 PRODUCTS BY REVENUE")
        for product, revenue in self.get_top_products_by_revenue(10):
            print(f"{product:<25}: ${revenue:>10.2f}")
        
        # 9. Monthly Revenue
        print("\n9. MONTHLY REVENUE")
        monthly_revenue = self.get_monthly_revenue()
        for month, revenue in sorted(monthly_revenue.items()):
            print(f"{month:<20}: ${revenue:>10.2f}")
        
        # 10. Average Order Value by Category
        print("\n10. AVERAGE ORDER VALUE BY CATEGORY")
        avg_by_category = self.get_average_order_value_by_category()
        for category, avg in sorted(avg_by_category.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:<20}: ${avg:>10.2f}")
        
        # 11. High-Value Orders
        print("\n11. ORDERS ABOVE $500")
        high_value_orders = self.get_orders_above_threshold(500.0)
        for record in high_value_orders[:10]:
            print(f"Order {record.order_id}: {record.product_name:<25} ${record.total_price:.2f}")
        
        # 12. Customer Purchase Frequency
        print("\n12. CUSTOMER PURCHASE FREQUENCY (Top 10)")
        frequency = self.get_customer_purchase_frequency()
        for customer, count in sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"{customer:<20}: {count:>8} orders")
        
        # 13. Quantity by Category
        print("\n13. TOTAL QUANTITY SOLD BY CATEGORY")
        quantity_by_category = self.get_quantity_sold_by_category()
        for category, quantity in sorted(quantity_by_category.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:<20}: {quantity:>8} units")
        
        # 14. Statistics Summary
        print("\n14. REVENUE STATISTICS")
        stats = self.get_revenue_statistics()
        print(f"Count  : {stats['count']}")
        print(f"Sum    : ${stats['sum']:.2f}")
        print(f"Min    : ${stats['min']:.2f}")
        print(f"Max    : ${stats['max']:.2f}")
        print(f"Average: ${stats['average']:.2f}")
        print(f"Std Dev: ${stats['std_dev']:.2f}")
        
        # 15. Customer Metrics
        print("\n15. CUSTOMER METRICS")
        distinct_customers = self.get_distinct_customers_count()
        print(f"Distinct Customers: {distinct_customers}")
        print(f"Total Orders: {len(self.sales_data)}")
        print(f"Average Orders per Customer: {len(self.sales_data) / distinct_customers:.2f}")


def main():
    import sys
    analyzer = SalesAnalyzer()
    
    # Load data
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'sales_data.csv'
    print(f"Loading sales data from: {file_path}")
    analyzer.load_data(file_path)
    print(f"Loaded {len(analyzer.sales_data)} sales records\n")
    
    # Display all analyses
    analyzer.display_all_analyses()
    
    # Demonstrate higher-order functions    
    # Example 1: Apply discount using lambda
    print("\n\nApply 10% Discount to Electronics (using higher-order functions)\n")
    discount_fn = lambda record: record.total_price * 0.1 if record.product_category == "Electronics" else 0.0
    discounted = analyzer.apply_discount(discount_fn)
    for order_id, original, discounted_price in discounted[:5]:
        if original != discounted_price:
            print(f"Order {order_id}: ${original:.2f} -> ${discounted_price:.2f} (saved ${original - discounted_price:.2f})")
    
    # Example 2: Function composition
    print("\nHigh-Value Electronics Orders (using function composition)\n")
    high_value_electronics = analyzer.filter_and_transform(
        filter_fn=lambda r: r.product_category == "Electronics" and r.total_price > 200,
        transform_fn=lambda r: f"{r.product_name}: ${r.total_price:.2f}"
    )
    for item in high_value_electronics[:5]:
        print(item)

if __name__ == "__main__":
    main()