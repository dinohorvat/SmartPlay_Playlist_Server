from flask import Flask, request, jsonify
import time
import json

app = Flask(__name__)
playing = 0
current_index = 0

@app.route('/play', methods=['POST'])
def play():
    mediaFiles = request.json
    global current_index
    global playing
    playing = 1
    while playing == 1:
        for current_index, file in enumerate(mediaFiles['mediaFiles'][current_index:], current_index):
            if playing == 0:
                break
            print(file['path'])
            time.sleep(5)
        current_index = 0            # loop back to 0 after last file
    return 'Played'


@app.route('/stop')
def stop():
    global playing
    playing = 0
    return 'Stopped...'


@app.route('/pause')
def pause():
    global playing
    playing = 0
    return 'Stopped...'


@app.route('/next')
def stop():
    global current_index
    current_index += 1
    return 'Stopped...'


if __name__ == '__main__':
    app.run()
