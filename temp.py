from flask import Flask, request
import time
import threading

app = Flask(__name__)

playing = 0
current_index = 0
duration = 5


def play_media():
    global playing
    playing = 1
    print(duration)
    while playing == 1:
        print('Playing...')
        time.sleep(duration)
    print('Finished')


thread1 = threading.Thread(name='playMedia', target=play_media)


@app.route('/play', methods=['POST'])
def play():
    global duration
    media = request.json
    duration = media['duration']
    thread1.start()
    return 'Played'


if __name__ == '__main__':
    app.run()
