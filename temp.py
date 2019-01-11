from flask import Flask, request
import threading

app = Flask(__name__)

playing = 0
duration = 5
media_files = []
condition = threading.Condition()


def play_media():
    global playing
    playing = 1
    print(duration)
    while playing == 1:
        for file in media_files:
            if playing == 0:
                break
            print(file['path'])
            with condition:
                condition.wait(timeout=duration)
    print('Finished')


@app.route('/play', methods=['POST'])
def play():
    global duration, media_files, playing
    media = request.json
    duration = media['duration']
    media_files = media['mediaFiles']
    threading.Thread(name='playMedia', target=play_media).start()
    return 'Played'


@app.route('/stop')
def stop_media():
    global playing
    playing = 0
    with condition:
        condition.notify()
    return 'Stopped'


@app.route('/test')
def test():
    global playing
    playing = 1
    threading.Thread(name='playMedia', target=play_media).start()
    return 'test'


if __name__ == '__main__':
    app.run()
