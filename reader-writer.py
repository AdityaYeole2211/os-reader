import threading

mutex = threading.Lock()
write = threading.Semaphore(1)
read = threading.Semaphore(10)  # Allow up to 10 readers simultaneously

no_of_active_readers = 0
shared_file = 'demo_file.txt'

def reader(id):
    global mutex, read, no_of_active_readers
    read.acquire()
    mutex.acquire()
    no_of_active_readers += 1
    if no_of_active_readers == 1:
        write.acquire()  # If this is the first reader, acquire the write semaphore to block writers
    mutex.release()
    
    try:
        with open(shared_file, 'r') as file:
            data = file.read()
            print(f"Reader {id} read: {data}")
    finally:
        mutex.acquire()
        no_of_active_readers -= 1
        if no_of_active_readers == 0:
            write.release()  # If this is the last reader, release the write semaphore to allow writers
        mutex.release()
        read.release()

def writer(id, data):
    global write
    write.acquire()  # Acquire the write semaphore to block other writers and readers
    try:
        with open(shared_file, 'a') as file:
            file.write(data + '\n')
            print(f"Writer {id} wrote: {data}")
    finally:
        write.release()  # Release the write semaphore

if __name__ == "__main__":
    num_readers = 3
    num_writers = 3

    reader_threads = [threading.Thread(target=reader, args=(i+1,)) for i in range(num_readers)]
    writer_threads = [threading.Thread(target=writer, args=(i+1, f"Written by writer {i+1}")) for i in range(num_writers)]

    # Start the threads
    for thread in reader_threads + writer_threads:
        thread.start()

    # Wait for the threads to finish
    for thread in reader_threads + writer_threads:
        thread.join()

    print("Execution is finished.")
