# Producer-Consumer Pattern Implementation

## Overview
This project implements the classic Producer-Consumer pattern demonstrating thread synchronization and communication in Python. The implementation simulates concurrent data transfer between producer threads that generate items and consumer threads that process them through a shared, bounded buffer.

## Key Features

### Thread Synchronization
- Uses `threading.Lock` and `threading.Condition`
- Producers block when buffer is full
- Consumers block when buffer is empty
- Implements correct `wait()` / `notify()` mechanics

### Concurrent Programming
- Multiple producer and consumer threads
- Thread-safe shared buffer with capacity constraints
- FIFO ordering guaranteed
- No data loss or duplication

### Blocking Queues
- Custom implementation using synchronized collections
- Alternative Python implementation using built-in `queue.Queue`
- Bounded buffer with configurable capacity

## Project Structure

```
├── producer_consumer.py           # Python main implementation
├── test_producer_consumer.py      # Python unit tests
└── README.md                      # README file
```

## Quick start

**Clone the repository:**
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>/assignment-1

**Run the Producer–Consumer Simulation:**
python3 producer_consumer.py

**Running Python Unit Tests:**
- Run all tests: python3 -m unittest discover -v
- Run a specific test class: python3 -m unittest test_producer_consumer.TestProducerConsumer
- Run a single test: python3 -m unittest test_producer_consumer.TestProducerConsumer.test_basic_producer_consumer

## Python Implementation

### Classes

#### `SharedBuffer`
Thread-safe bounded buffer using threading.Lock and Condition variables.

**Key Methods:**
- `put(item: int)`: Add item to buffer (blocks if full)
- `take() -> int`: Remove and return item (blocks if empty)
- `size() -> int`: Return current buffer size

#### `Producer`
A thread that places items from a source list into the shared buffer. This handles production delay and blocking behavior when buffer is full.

#### `Consumer`
A thread that removes items from the shared buffer and stores them into a destination list. This handles consumption delay and blocking on empty buffer.

#### `ProducerConsumerQueue`
Alternative implementation using Python's built-in `queue.Queue` (recommended for production).

### Python Test Cases
- `test_put_and_take`
- `test_buffer_size`
- `test_fifo_order`
- `test_basic_producer_consumer`
- `test_fast_producer_slow_consumer`
- `test_empty_source`
- `test_single_item`
- `test_thread_synchronization` 
- `test_queue_basic_functionality`
- `test_queue_empty_source`
- `test_buffer_capacity_not_exceeded`
- `test_no_race_conditions`

## Design Patterns and Concepts

### Producer-Consumer Pattern
The classic concurrency pattern where:
- **Producers** generate data and place it in a shared buffer
- **Consumers** retrieve and process data from the buffer
- **Buffer** decouples producers from consumers

### Thread Synchronization Mechanisms

- `threading.Lock` for mutual exclusion
- `threading.Condition` for wait/notify operations
- Context managers (`with` statement) for automatic lock management

### Key Synchronization Principles

1. **Mutual Exclusion**: Only one thread can modify buffer at a time
2. **Condition Synchronization**: Threads wait for specific conditions
3. **Bounded Buffer**: Fixed capacity prevents unbounded growth
4. **FIFO Ordering**: First-in, first-out queue semantics
5. **Deadlock Prevention**: Proper lock ordering and timeout handling

## Example Output

```
Starting Producer-Consumer simulation...

Produced: 1 | Buffer size: 1
Consumed: 1 | Buffer size: 0
Produced: 2 | Buffer size: 1
Consumed: 2 | Buffer size: 0
Produced: 3 | Buffer size: 1
Consumed: 3 | Buffer size: 0
Produced: 4 | Buffer size: 1
Produced: 5 | Buffer size: 2
Consumed: 4 | Buffer size: 1
Produced: 6 | Buffer size: 2
Consumed: 5 | Buffer size: 1
Produced: 7 | Buffer size: 2
Produced: 8 | Buffer size: 3
Consumed: 6 | Buffer size: 2
Produced: 9 | Buffer size: 3
Consumed: 7 | Buffer size: 2
Produced: 10 | Buffer size: 3
Produced: 11 | Buffer size: 4
Consumed: 8 | Buffer size: 3
Produced: 12 | Buffer size: 4
Consumed: 9 | Buffer size: 3
Produced: 13 | Buffer size: 4
Produced: 14 | Buffer size: 5
Consumed: 10 | Buffer size: 4
Produced: 15 | Buffer size: 5
Consumed: 11 | Buffer size: 4
Produced: 16 | Buffer size: 5
Buffer full. Producer waiting...
Consumed: 12 | Buffer size: 4
Produced: 17 | Buffer size: 5
Buffer full. Producer waiting...
Consumed: 13 | Buffer size: 4
Produced: 18 | Buffer size: 5
Buffer full. Producer waiting...
Consumed: 14 | Buffer size: 4
Produced: 19 | Buffer size: 5
Buffer full. Producer waiting...
Consumed: 15 | Buffer size: 4
Produced: 20 | Buffer size: 5
Producer finished producing all items
Consumed: 16 | Buffer size: 4
Consumed: 17 | Buffer size: 3
Consumed: 18 | Buffer size: 2
Consumed: 19 | Buffer size: 1
Consumed: 20 | Buffer size: 0
Consumer finished consuming all items
Simulation complete!
Items produced: 20
Items consumed: 20
Source matches destination: True
```

## Performance Characteristics (Python)

- Uses Python list with O(1) append, O(n) pop(0)
- GIL limits true parallelism but synchronization still needed
- Built-in `queue.Queue` is optimized and recommended

## Best Practices Demonstrated

1. **Encapsulation**: Buffer logic encapsulated in dedicated class
2. **Thread Safety**: All shared state properly synchronized
3. **Resource Management**: Threads properly started and joined
4. **Error Handling**: InterruptedException properly caught and handled
5. **Testing**: Comprehensive test coverage including edge cases
6. **Documentation**: Clear comments and docstrings
7. **SOLID Principles**: Single responsibility, open-closed principle

## Common Issues and Solutions

### Problem: Deadlock
**Solution**: Always use proper lock ordering, use timeouts, prefer higher-level constructs

### Problem: Lost Updates
**Solution**: Synchronize all access to shared state

### Problem: Thread Starvation
**Solution**: Use fair locks or queues, avoid indefinite blocking

### Problem: Buffer Overflow
**Solution**: Enforce capacity limits with blocking operations

## Extensions and Improvements

- Add priority queue for priority-based consumption
- Implement multiple buffer types (stack, circular buffer)
- Add timeout capabilities for put/take operations
- Use thread pools for better resource management

## Requirements

### Python
- Python 3.7 or higher
- No external dependencies for main implementation
- unittest (standard library) for tests

## License
This is an educational implementation for demonstrating concurrent programming concepts.

## References
- Python Threading Documentation
- Producer-Consumer Pattern (Gang of Four)