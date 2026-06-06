import threading
import requests
import time


def downloadImage(imagePath, fileName):
    print("Downloading Image from", imagePath)
    response = requests.get(imagePath)
    with open(fileName, "wb") as f:
        f.write(response.content)
    print("Completed Download")


def executeThread(i):
    imageName = f"/tmp/image-{str(i)}.jpg"
    downloadImage("http://lorempixel.com/400/200/sports", imageName)


def main():
    t0 = time.time()
    threads = []

    for i in range(10):
        thread = threading.Thread(target=executeThread, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    t1 = time.time()
    totalTime = t1 - t0
    print(f"Total Execution Time: {totalTime}")


if __name__ == "__main__":
    main()
