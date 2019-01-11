from flask import Flask, request
import time
import threading

app = Flask(__name__)

playing = 0
current_index = 0
duration = 5
media_files = []


def play_media():
    global playing
    playing = 1
    print(duration)
    while playing == 1:
        for file in media_files:
            print(file['path'])
            time.sleep(duration)
    print('Finished')


thread1 = threading.Thread(name='playMedia', target=play_media)


@app.route('/play', methods=['POST'])
def play():
    global duration, media_files
    media = request.json
    duration = media['duration']
    media_files = media['mediaFiles']
    thread1.start()
    return 'Played'


if __name__ == '__main__':
    app.run()
