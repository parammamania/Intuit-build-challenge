# Sales Data Analysis with Functional Programming

## Overview

This project demonstrates proficiency in functional programming to perform comprehensive data analysis on sales data from a CSV file. The implementation showcases advanced stream operations, lambda expressions, data aggregation, functional composition, and higher-order functions.

## Project Structure

```
├── sales_data.csv              # Sample e-commerce sales dataset (50 records)
├── sales_analyzer.py           # Python implementation with functional programming
├── test_sales_analyzer.py      # Python unittest tests
└── README.md                   # README file
```

## Dataset Description

Each row in `sales_data.csv` represents a transaction with:
- order_id
- date
- customer_id
- customer_name
- product_category
- product_name
- quantity
- unit_price
- total_price
- region
- payment_method

These fields are parsed into an immutable SalesRecord using a frozen dataclass.

## Implemented Analyses

### Aggregation Functions
- Total revenue (using reduce)
- Average order value
- Revenue statistics (min, max, avg, std-dev)

### Grouping & Summaries
- Sales by category
- Sales by region
- Orders by payment method
- Monthly revenue
- Quantity sold per category

### Ranking
- Top customers (sorted by spending)
- Top products by quantity
- Top products by revenue

### Filtering
- Orders above a given threshold (using filter)

### Advanced Functional Operations
- Customer purchase frequency
- Multi-level grouping (region → category)
- Higher-order discount functions
- Combined filter + transform operations (function composition)

## Quick start

**Clone the repository:**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/assignment-2
```

**Run the Analyzer:**
```bash
python3 sales_analyzer.py
```

**Running Python Unit Tests:**
```bash
python3 -m unittest test_sales_analyzer -v
- Run all tests: python3 -m unittest test_sales_analyzer -v
- Run a specific test class: python3 -m unittest test_sales_analyzer.TestSalesAnalyzer -v
- Run a single test: python3 -m unittest test_sales_analyzer.TestSalesAnalyzer.test_calculate_total_revenue
```

## Python Test Cases

- `test_load_data`
- `test_calculate_total_revenue`
- `test_calculate_average_order_value`
- `test_get_total_sales_by_category`
- `test_get_total_sales_by_region`
- `test_get_order_count_by_payment_method`
- `test_get_top_customers`
- `test_get_top_products_by_quantity`
- `test_get_top_products_by_revenue`
- `test_get_monthly_revenue`
- `test_get_average_order_value_by_category`
- `test_get_revenue_statistics`
- `test_get_orders_above_threshold_with_filter`
- `test_empty_dataset`
- `test_get_customer_purchase_frequency`
- `test_get_quantity_sold_by_category`
- `test_get_distinct_customers_count`
- `test_get_revenue_by_region_and_category`
- `test_apply_discount_higher_order_function`
- `test_apply_conditional_discount`
- `test_filter_and_transform_composition`
- `test_sales_record_creation`
- `test_sales_record_string_representation`

## Example Output

```
Loading sales data from: sales_data.csv
Loaded 50 sales records

SALES DATA ANALYSIS RESULTS

1. TOTAL REVENUE
Total Revenue: $8635.96

2. AVERAGE ORDER VALUE
Average Order Value: $172.72

3. TOTAL SALES BY CATEGORY
Electronics         : $   5203.70
Home & Garden       : $   1184.84
Clothing            : $   1148.42
Books               : $   1099.00

4. TOTAL SALES BY REGION
North               : $   3486.34
East                : $   2290.91
South               : $   1768.82
West                : $   1089.89

5. ORDER COUNT BY PAYMENT METHOD
Credit Card         :         27 orders
Debit Card          :         12 orders
PayPal              :         11 orders

6. TOP 10 CUSTOMERS BY SPENDING
John Smith          : $   1962.45
Michael Brown       : $   1489.97
Nancy Rodriguez     : $    814.96
James Wilson        : $    738.97
David Martinez      : $    524.98
Emma Johnson        : $    508.92
Maria Garcia        : $    444.94
Sarah Davis         : $    367.48
Jennifer Lee        : $    365.98
Lisa Anderson       : $    289.96

7. TOP 10 PRODUCTS BY QUANTITY SOLD
Charger                  :      5.0 units
Shirt                    :      4.0 units
USB Hub                  :      4.0 units
Flash Drive              :      4.0 units
Python Programming       :      3.0 units
Wireless Mouse           :      3.0 units
Toaster                  :      3.0 units
Algorithm Design         :      3.0 units
Shorts                   :      3.0 units
Scarf                    :      3.0 units

8. TOP 10 PRODUCTS BY REVENUE
Laptop                   : $   1200.00
Smartphone               : $    799.99
Camera                   : $    599.99
Tablet                   : $    499.99
Monitor                  : $    349.99
Smart Watch              : $    299.99
Headphones               : $    299.98
Printer                  : $    249.99
Vacuum Cleaner           : $    189.99
Jacket                   : $    179.98

9. MONTHLY REVENUE
2024-01             : $   4526.35
2024-02             : $   3703.69
2024-03             : $    405.92

10. AVERAGE ORDER VALUE BY CATEGORY
Electronics         : $    306.10
Home & Garden       : $    107.71
Clothing            : $    104.40
Books               : $     99.91

11. ORDERS ABOVE $500
Order 1001: Laptop                    $1200.00
Order 1003: Smartphone                $799.99
Order 1022: Camera                    $599.99

12. CUSTOMER PURCHASE FREQUENCY (Top 10)
John Smith          :        6 orders
Emma Johnson        :        5 orders
Michael Brown       :        4 orders
Sarah Davis         :        4 orders
James Wilson        :        4 orders
Lisa Anderson       :        3 orders
Robert Taylor       :        3 orders
Maria Garcia        :        3 orders
David Martinez      :        3 orders
Jennifer Lee        :        3 orders

13. TOTAL QUANTITY SOLD BY CATEGORY
Electronics         :     31.0 units
Clothing            :     22.0 units
Books               :     19.0 units
Home & Garden       :     18.0 units

14. REVENUE STATISTICS
Count  : 50
Sum    : $8635.96
Min    : $36.00
Max    : $1200.00
Average: $172.72
Std Dev: $205.88

15. CUSTOMER METRICS
Distinct Customers: 15
Total Orders: 50
Average Orders per Customer: 3.33


Apply 10% Discount to Electronics (using higher-order functions)

Order 1001: $1200.00 -> $1080.00 (saved $120.00)
Order 1003: $799.99 -> $719.99 (saved $80.00)

High-Value Electronics Orders (using function composition)

Laptop: $1200.00
Smartphone: $799.99
Headphones: $299.98
Tablet: $499.99
Smart Watch: $299.99
```

## Performance Characteristics (Python)

### Time Complexity
- Most operations: **O(n)** where n = number of records
- Sorting operations: **O(n log n)**
- Grouping operations: **O(n)**
- Top-N queries: **O(n log n)** for sorting + **O(1)** for limit

### Space Complexity
- Original data: **O(n)**
- Grouped results: **O(k)** where k = number of groups
- Stream operations: Often **O(1)** additional space (lazy evaluation)

### Optimization Notes
- Lazy evaluation minimizes work until a terminal action is required.
- Parallel execution can speed up large datasets.
- Python generators reduce memory footprint.
- Caching can optimize repeated calculations.

## Functional Programming Concepts Demonstrated

- **Immutability:** Data is never modified; SalesRecord uses @dataclass(frozen=True).
- **Pure Functions:** Functions return consistent results without side effects.
- **Higher-Order Functions:** Functions accept other functions (e.g., custom discounts, transformations).
- **Lambda Expressions:** Concise anonymous functions used for filtering, sorting, and mapping.
- **Map, Filter, Reduce:** Transform, select, and aggregate data using functional operators.

## Extensions and Improvements
- Add new analytical functions
- Add additional functional queries (new filters, more aggregations)

## Requirements

### Python
- Python 3.7 or higher
- No external dependencies for main implementation
- unittest (standard library) for tests

## License
This is an educational implementation for demonstrating concurrent programming concepts.

## References
- Python Functional Programming: [Python HOWTO](https://docs.python.org/3/howto/functional.html)
- Functional Programming Principles
- Clean Code by Robert C. Martin