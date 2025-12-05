import unittest
import threading
import time
from producer_consumer import (
    SharedBuffer, Producer, Consumer, ProducerConsumerQueue
)


class TestSharedBuffer(unittest.TestCase):
    """Unit tests for low-level SharedBuffer operations (FIFO queue behavior)."""
    
    def setUp(self):
        """Create a fresh buffer before each test."""
        self.buffer = SharedBuffer(5)
    
    def test_put_and_take(self):
        """
        Ensure put() inserts items and take() retrieves them correctly.
        Validates correct basic signaling and storage.
        """
        self.buffer.put(1)
        self.buffer.put(2)
        
        self.assertEqual(self.buffer.take(), 1)
        self.assertEqual(self.buffer.take(), 2)
    
    def test_buffer_size(self):
        """Verify that the size() method accurately tracks buffer length."""
        self.assertEqual(self.buffer.size(), 0)
        
        self.buffer.put(1)
        self.assertEqual(self.buffer.size(), 1)
        
        self.buffer.put(2)
        self.assertEqual(self.buffer.size(), 2)
        
        self.buffer.take()
        self.assertEqual(self.buffer.size(), 1)
    
    def test_fifo_order(self):
        """
        The buffer must behave as a FIFO structure.
        This validates general queue semantics independent of threading.
        """
        items = [1, 2, 3, 4, 5]
        
        for item in items:
            self.buffer.put(item)
        
        result = []
        for _ in range(len(items)):
            result.append(self.buffer.take())
        
        self.assertEqual(items, result)


class TestProducerConsumer(unittest.TestCase):
    """Integration tests validating Producer + Consumer thread behavior."""
    
    def test_basic_producer_consumer(self):
        """
        Full pipeline test with matching producer/consumer speeds.
        Ensures all items move through the buffer correctly.
        """
        source = list(range(1, 11))
        destination = []
        buffer = SharedBuffer(5)
        
        producer = Producer(buffer, source, 0.01)
        consumer = Consumer(buffer, destination, len(source), 0.01)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=5)
        consumer.join(timeout=5)
        
        # Validate complete and ordered transfer
        self.assertEqual(len(source), len(destination))
        self.assertEqual(source, destination)
    
    def test_fast_producer_slow_consumer(self):
        """
        Producer outpaces consumer.
        Ensures buffer blocking (not_full.wait) functions correctly.
        """
        source = list(range(1, 21))
        destination = []
        buffer = SharedBuffer(5)
        
        producer = Producer(buffer, source, 0.01) # fast
        consumer = Consumer(buffer, destination, len(source), 0.05) # slow
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=10)
        consumer.join(timeout=10)
        
        # All items must still transfer correctly
        self.assertEqual(source, destination)
    
    def test_empty_source(self):
        """Test with empty source list."""
        source = []
        destination = []
        buffer = SharedBuffer(5)
        
        producer = Producer(buffer, source, 0.01)
        consumer = Consumer(buffer, destination, len(source), 0.01)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=2)
        consumer.join(timeout=2)
        
        self.assertEqual(0, len(destination))
        self.assertEqual([], destination)
    
    def test_single_item(self):
        """Test with single item."""
        source = [42]
        destination = []
        buffer = SharedBuffer(5)
        
        producer = Producer(buffer, source, 0.01)
        consumer = Consumer(buffer, destination, len(source), 0.01)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=2)
        consumer.join(timeout=2)
        
        self.assertEqual(1, len(destination))
        self.assertEqual(42, destination[0])
    
    def test_thread_synchronization(self):
        """
        Ensures no duplicates and no lost items — critical for verifying
        lock correctness and correct wait/notify semantics.
        """
        source = list(range(1, 101))
        destination = []
        buffer = SharedBuffer(5)
        
        producer = Producer(buffer, source, 0.001)
        consumer = Consumer(buffer, destination, len(source), 0.001)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=10)
        consumer.join(timeout=10)
        
        # Check no duplicates
        self.assertEqual(len(destination), len(set(destination)))
        
        # Check no items lost
        self.assertEqual(sorted(source), sorted(destination))


class TestProducerConsumerQueue(unittest.TestCase):
    """Tests for the queue.Queue-backed producer-consumer implementation."""
    
    def test_queue_basic_functionality(self):
        """Simple test validating end-to-end queue behavior."""
        source = list(range(1, 11))
        destination = []
        pc = ProducerConsumerQueue(5)
        
        producer_thread = threading.Thread(
            target=pc.producer,
            args=(source, 0.01)
        )
        consumer_thread = threading.Thread(
            target=pc.consumer,
            args=(destination, len(source), 0.01)
        )
        
        producer_thread.start()
        consumer_thread.start()
        
        producer_thread.join(timeout=5)
        consumer_thread.join(timeout=5)
        
        self.assertEqual(source, destination)
    
    def test_queue_empty_source(self):
        """Edge case: empty source list should produce empty results."""
        source = []
        destination = []
        pc = ProducerConsumerQueue(5)
        
        producer_thread = threading.Thread(
            target=pc.producer,
            args=(source, 0.01)
        )
        consumer_thread = threading.Thread(
            target=pc.consumer,
            args=(destination, len(source), 0.01)
        )
        
        producer_thread.start()
        consumer_thread.start()
        
        producer_thread.join(timeout=2)
        consumer_thread.join(timeout=2)
        
        self.assertEqual([], destination)


class TestConcurrency(unittest.TestCase):
    """Advanced tests that ensure correct synchronization."""
    
    def test_buffer_capacity_not_exceeded(self):
        """
        Ensures that the producer is correctly blocked when buffer is full.
        Observes max size seen during runtime — must never exceed capacity.
        """
        capacity = 5
        buffer = SharedBuffer(capacity)
        source = list(range(1, 51))
        destination = []
        max_size_observed = [0]
        
        # Create a custom producer that checks buffer size
        class MonitoringProducer(Producer):
            def run(self):
                try:
                    for item in self.source:
                        self.buffer.put(item)
                        current_size = self.buffer.size()
                        max_size_observed[0] = max(max_size_observed[0], current_size)
                        time.sleep(0.01)
                except Exception as e:
                    print(f"Producer error: {e}")
        
        producer = MonitoringProducer(buffer, source, 0.01)
        consumer = Consumer(buffer, destination, len(source), 0.05)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=10)
        consumer.join(timeout=10)
        
        self.assertLessEqual(max_size_observed[0], capacity)
    
    def test_no_race_conditions(self):
        """
        Detects subtle race bugs by checking:
        - no lost items
        - no duplicates
        - all items transferred exactly once
        """
        buffer = SharedBuffer(5)
        source = list(range(1, 101))
        destination = []
        
        producer = Producer(buffer, source, 0.001)
        consumer = Consumer(buffer, destination, len(source), 0.001)
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=10)
        consumer.join(timeout=10)
        
        # Verify data integrity
        self.assertEqual(len(source), len(destination))
        self.assertEqual(sorted(source), sorted(destination))


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestSharedBuffer))
    test_suite.addTest(unittest.makeSuite(TestProducerConsumer))
    test_suite.addTest(unittest.makeSuite(TestProducerConsumerQueue))
    test_suite.addTest(unittest.makeSuite(TestConcurrency))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())