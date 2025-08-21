import threading
import time
import requests

# Worker function for downloading a single URL
def download_url(url):
    try:
        print(f"Started downloading: {url}")
        response = requests.get(url, timeout=10)
        print(f"Finished downloading: {url} (size: {len(response.content)} bytes)")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# List of URLs to download
urls = [
    "https://www.example.com",
    "https://www.python.org",
    "https://httpbin.org/get",
    "https://www.wikipedia.org"
]

# Start time
start_time = time.time()

# List to keep track of threads
threads = []

# Creating and starting threads
for url in urls:
    thread = threading.Thread(target=download_url, args=(url,))
    thread.start()
    threads.append(thread) 

# Wait for all threads to complete
for thread in threads:
    thread.join()

# End time
end_time = time.time()
print(f"\nAll downloads completed in {end_time - start_time:.2f} seconds")
