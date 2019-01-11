from flask import Flask, request
from collections import deque

import time
import threading

app = Flask(__name__)
lck = threading.Lock()

items = [1, 2, 3, 4]
curr = 2

prebaci = len(items) - 4 + 2

def shift(key, array):
    return array[-key:]+array[:-key]


print(shift(1, items))

if __name__ == '__main__':
    app.run()


