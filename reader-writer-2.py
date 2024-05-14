import threading
import time

# Shared resource
shared_file = "demo_file.txt"

# Mutex
mutex = threading.Lock()

# Semaphore for writers
write = threading.Semaphore(1)

# Semaphore for readers
read = threading.Semaphore(1)

# Function for readers
def reader(id):
    global mutex, write
    read.acquire()
    mutex.acquire()
    print(f"Reader {id} is reading..." + '\n') 
    with open(shared_file, "r") as file:
        data = file.read()
        print(f"Reader {id} read: {data}" + '\n')
    mutex.release()
    read.release()

# Function for writers
def writer(id, data):
    global write
    write.acquire()
    print(f"Writer {id} is writing..." + '\n')
    with open(shared_file, "a") as file:
        file.write(data + "\n")  # Append data to the file
    write.release()

# Test the reader-writer problem
if __name__ == "__main__":
    # Create some reader and writer threads
    num_readers = 3
    num_writers = 3

    reader_threads = []
    writer_threads = []

    for i in range(num_readers):
        reader_threads.append(threading.Thread(target=reader, args=(i+1,)))

    for i in range(num_writers):
        writer_threads.append(threading.Thread(target=writer, args=(i+1, f"Data written by writer {i+1}")))

    # Start all reader threads
    for thread in reader_threads:
        thread.start()

    # Start all writer threads
    for thread in writer_threads:
        thread.start()

    # Wait for all threads to finish
    for thread in reader_threads:
        thread.join()

    for thread in writer_threads:
        thread.join()

    print("All readers and writers have finished.")
