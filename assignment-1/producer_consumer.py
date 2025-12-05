import threading
import queue
import time
from typing import List


class SharedBuffer:

    """
    A manually implemented thread-safe bounded buffer that supports blocking
    put() and take() operations. This demonstrates classic producer–consumer
    synchronization using Lock, Condition variables, and wait/notify.
    """

    def __init__(self, capacity: int):
        """
        Creates thread-safe communication channel between producer and consumer threads.
        
        Args:
            capacity: Maximum number of items the buffer can hold
        """
        self.capacity = capacity
        self.buffer = []
        self.lock = threading.Lock() # Mutual exclusion lock

        # Condition variables for communication between producer and consumer
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def put(self, item: int) -> None:
        """
        Allows producers to safely insert items, blocking when the buffer is full.
        
        Args:
            item: The item to add to the buffer
        """
        with self.not_full: # Acquire lock through condition
            while len(self.buffer) >= self.capacity:
                print(f"Buffer full. Producer waiting...")
                self.not_full.wait()
            
            # Insert item into buffer
            self.buffer.append(item)
            print(f"Produced: {item} | Buffer size: {len(self.buffer)}")
            
            # Notify consumers that an item is available
            self.not_empty.notify()
    
    def take(self) -> int:
        """
        Allows consumers to safely remove items, blocking when buffer is empty.
        
        Returns:
            The item removed from the buffer
        """
        with self.not_empty:
            # Wait until buffer has at least one item
            while len(self.buffer) == 0:
                print(f"Buffer empty. Consumer waiting...")
                self.not_empty.wait()
            
            # Remove and return first item
            item = self.buffer.pop(0)
            print(f"Consumed: {item} | Buffer size: {len(self.buffer)}")
            
            # Notify producers that space is available
            self.not_full.notify()
            return item
    
    def size(self) -> int:
        """
        Simple helper to return current buffer length (thread-safe).
        """
        with self.lock:
            return len(self.buffer)


class Producer(threading.Thread):
    
    """
    Thread class that acts as a producer. It reads from a source list and
    inserts items into the shared buffer.
    """
    
    def __init__(self, buffer: SharedBuffer, source: List[int], 
                 production_delay: float = 0):
        """
        Args:
            buffer: Shared buffer to produce items into
            source: List of items to produce
            production_delay: Delay in seconds between productions
        """
        super().__init__()
        self.buffer = buffer
        self.source = source
        self.production_delay = production_delay
    
    def run(self) -> None:
        """
        Thread's execution logic. Produces items one-by-one and places them
        into the buffer, blocking if necessary.
        """
        try:
            for item in self.source:
                self.buffer.put(item)
                
                # Simulate production time
                if self.production_delay > 0:
                    time.sleep(self.production_delay)
            
            print("Producer finished producing all items")
        except Exception as e:
            print(f"Producer error: {e}")


class Consumer(threading.Thread):
    
    """
    Thread class that acts as a consumer. It retrieves items from the shared
    buffer and stores them into a destination container.
    """
    
    def __init__(self, buffer: SharedBuffer, destination: List[int], 
                 item_count: int, consumption_delay: float = 0):
        """
        Args:
            buffer: Shared buffer to consume items from
            destination: List to store consumed items
            item_count: Number of items to consume
            consumption_delay: Delay in seconds between consumptions
        """
        super().__init__()
        self.buffer = buffer
        self.destination = destination
        self.item_count = item_count
        self.consumption_delay = consumption_delay
    
    def run(self) -> None:
        """
        Thread's execution logic. Repeatedly removes items from the buffer,
        blocking if necessary, and stores them in the destination list.
        """
        try:
            for _ in range(self.item_count):
                item = self.buffer.take()
                self.destination.append(item)
                
                # Simulate consumption time
                if self.consumption_delay > 0:
                    time.sleep(self.consumption_delay)
            
            print("Consumer finished consuming all items")
        except Exception as e:
            print(f"Consumer error: {e}")


class ProducerConsumerQueue:
    
    """
    A simpler and more robust implementation using Python's built-in
    queue.Queue, which already handles locking and condition synchronization.
    """
    
    def __init__(self, capacity: int):
        """
        Args:
            capacity: Maximum queue size
        """
        self.queue = queue.Queue(maxsize=capacity)
    
    def producer(self, source: List[int], production_delay: float = 0) -> None:
        """
        Producer function that puts items into the queue.
        
        Args:
            source: List of items to produce
            production_delay: Delay between productions
        """
        for item in source:
            self.queue.put(item) # Blocks automatically if full
            print(f"Produced: {item} | Queue size: {self.queue.qsize()}")
            
            if production_delay > 0:
                time.sleep(production_delay)
        
        print("Producer finished producing all items")
    
    def consumer(self, destination: List[int], item_count: int, 
                 consumption_delay: float = 0) -> None:
        """
        Consumer function that takes items from the queue.
        
        Args:
            destination: List to store consumed items
            item_count: Number of items to consume
            consumption_delay: Delay between consumptions
        """
        for _ in range(item_count):
            item = self.queue.get() # Blocks automatically if empty
            destination.append(item)
            print(f"Consumed: {item} | Queue size: {self.queue.qsize()}")
            
            if consumption_delay > 0:
                time.sleep(consumption_delay)
            
            self.queue.task_done()
        
        print("Consumer finished consuming all items")


def main():

    """Demonstrate the Producer-Consumer pattern using the custom SharedBuffer."""

    # Configuration with delay in seconds
    buffer_capacity = 5
    production_delay = 0.1  
    consumption_delay = 0.15  
    
    # Prepare data and shared objects
    source = list(range(1, 21))
    buffer = SharedBuffer(buffer_capacity)
    destination = []

    print("Starting Producer-Consumer simulation...\n")
    
    # Create and start producer + consumer threads
    producer = Producer(buffer, source, production_delay)
    consumer = Consumer(buffer, destination, len(source), consumption_delay)
    
    producer.start()
    consumer.start()
    
    # Wait for threads to complete
    producer.join()
    consumer.join()
    
    # Final results
    print("Simulation complete!")
    print(f"Items produced: {len(source)}")
    print(f"Items consumed: {len(destination)}")
    print(f"Source matches destination: {source == destination}")


def demo_queue_implementation():

    """Demonstrate the built-in Queue-based producer-consumer implementation."""

    print("\nQueue-based Implementation Demo\n")
    
    capacity = 5
    source = list(range(1, 11))
    destination = []
    pc = ProducerConsumerQueue(capacity)
    
    producer_thread = threading.Thread(target=pc.producer, args=(source, 0.1))
    consumer_thread = threading.Thread(target=pc.consumer, args=(destination, len(source), 0.15))
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
    
    print(f"\nResult: {destination}")
    print(f"Success: {source == destination}")


if __name__ == "__main__":
    main()
    demo_queue_implementation()