from threading import Thread
import time
from time import sleep


class HelloThread(Thread):
    def run(self): 
        for _ in range(5):
            print("Hello from the thread!")
            time.sleep(1)


class HiThread(Thread):
    def run(self):
        for _ in range(5):
            print("Hi from another thread!")
            time.sleep(1)


# Create thread instances
hello_thread = HelloThread()
hi_thread = HiThread()

# Start the threads
hello_thread.start()    
sleep(0.2)  # Sleep for 2 seconds before starting the next thread    
hi_thread.start()


hello_thread.join()  # Wait for the hello thread to finish
hi_thread.join()    # Wait for the hi thread to finish

print("Bye from the main thread!")