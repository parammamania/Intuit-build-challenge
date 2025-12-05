# Concurrent and Functional Programming Projects

This repository contains two programming assignments demonstrating advanced concepts in concurrent programming and functional data analysis using Python.

## Repository Structure

```
├── assignment-1/          # Producer-Consumer Pattern Implementation
│   ├── producer_consumer.py
│   ├── test_producer_consumer.py
│   └── README.md         # Detailed documentation
│
└── assignment-2/          # Sales Data Analysis with Functional Programming
    ├── sales_data.csv
    ├── sales_analyzer.py
    ├── test_sales_analyzer.py
    └── README.md         # Detailed documentation
```

## Assignment Overview

### Assignment 1: Producer-Consumer Pattern

A comprehensive implementation of the classic Producer-Consumer concurrency pattern in Python, demonstrating thread synchronization and inter-thread communication.

**Key Highlights:**
- Thread-safe bounded buffer with capacity constraints
- Multiple producer and consumer threads working concurrently
- Proper synchronization using `threading.Lock` and `threading.Condition`
- Custom implementation plus alternative using Python's `queue.Queue`
- Comprehensive unit tests covering edge cases and race conditions

**Concepts Demonstrated:**
- Mutual exclusion and critical sections
- Condition variables (wait/notify mechanisms)
- Deadlock prevention
- FIFO queue semantics
- Thread lifecycle management

**[View detailed README](assignment-1/README.md)**

---

### Assignment 2: Sales Data Analysis with Functional Programming

A functional programming approach to analyzing e-commerce sales data, showcasing advanced data transformation and aggregation techniques.

**Key Highlights:**
- Pure functional operations on 50-record sales dataset
- Immutable data structures using frozen dataclasses
- Advanced aggregations (revenue, statistics, grouping)
- Higher-order functions and function composition
- Lambda expressions for filtering, mapping, and sorting

**Analyses Implemented:**
- Revenue analytics (total, average, statistics)
- Multi-level grouping (by category, region, payment method)
- Top-N rankings (customers, products)
- Temporal analysis (monthly revenue)
- Functional transformations (discounts, conditional operations)

**[View detailed README](assignment-2/README.md)**

---

## Getting Started

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses standard library)

### Quick Start

**Clone the repository:**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

**Run Assignment 1:**
```bash
cd assignment-1
python3 producer_consumer.py
python3 -m unittest test_producer_consumer -v
```

**Run Assignment 2:**
```bash
cd assignment-2
python3 sales_analyzer.py
python3 -m unittest test_sales_analyzer -v
```

## Testing

Both assignments include comprehensive unit test suites:

- **Assignment 1**: 12 test cases covering thread synchronization, race conditions, and edge cases
- **Assignment 2**: 23 test cases validating functional operations, aggregations, and data transformations

Run all tests:
```bash
# From project root
python3 -m unittest discover -v
```

## Learning Outcomes

### Concurrent Programming (Assignment 1)
- Understanding thread synchronization primitives
- Implementing producer-consumer pattern correctly
- Avoiding common concurrency pitfalls (deadlock, race conditions)
- Using condition variables for efficient thread coordination

### Functional Programming (Assignment 2)
- Writing pure, side-effect-free functions
- Using immutable data structures
- Applying map, filter, reduce operations
- Composing functions for complex transformations
- Leveraging lazy evaluation for performance

## Documentation

Each assignment folder contains a detailed README with:
- Complete implementation details
- Design patterns and architecture
- Performance characteristics
- Example outputs
- API documentation
- Best practices demonstrated

## License

This is an educational implementation for demonstrating programming concepts.

## Additional Resources

- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [Python Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html)
- Producer-Consumer Pattern (Gang of Four)
- Clean Code by Robert C. Martin