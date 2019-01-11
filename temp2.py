from flask import Flask, request
import time
import threading

app = Flask(__name__)
lck = threading.Lock()
playing = 0

current_index = 0
current_changed = 0


@app.route('/play', methods=['POST'])
def play():
    mediaFiles = request.json
    global playing, current_index, current_changed
    playing = 1
    while playing == 1:
        print('Outside')
        print(current_index)
        for current_index, file in syncenumerate(lck, mediaFiles['mediaFiles'][current_index:], current_index):
            if current_changed == 1:    # restart enumeration is current was changed
                current_changed = 0
                break
            if playing == 0:
                break
            print(file['path'])
            current_index += 1
            time.sleep(5)
        current_index = 0            # loop back to 0 after last file
    return 'Played'


@app.route('/next')
def nextPlay():
    global current_index, current_changed
    lck.acquire()
    current_index += 1
    if current_index >= 4: current_index = 0
    current_changed = 1
    lck.release()
    return 'Next...'


if __name__ == '__main__':
    app.run()


class syncenumerate:
    def __init__(self, lock, iterable, start=current_index):
        self.lock = lock
        self.iter = enumerate(iterable, start)

    def __iter__(self):
        return self

    def __next__(self):
        self.lock.acquire()
        try:
            ret = next(self.iter)
        finally:
            self.lock.release()    # ensure that the lock is released at StopIteration
        return ret
