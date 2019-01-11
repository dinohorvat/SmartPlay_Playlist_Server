from flask import Flask, request
import threading

app = Flask(__name__)

playing = 0
duration = 5
current_index = 0
touched = 0
original_duration = 5
media_files = []
original_media_files = []
condition = threading.Condition()


def shift(key, array, next_event):
    if next_event == 1:
        key = len(array) - key
    else:
        key = len(array) - key + 2
    return array[-key:]+array[:-key]


def play_media():
    global playing, current_index, touched
    playing = 1
    print(duration)
    while playing == 1:
        print('start from stracth')
        for file in media_files:
            if current_index > (len(media_files) - 1):
                current_index = 0
            if (playing == 0) or (touched == 1):
                touched = 0
                break
            print(current_index)
            print(file['path'])
            current_index += 1
            with condition:
                condition.wait(timeout=duration)
    print('Finished')


@app.route('/play', methods=['POST'])
def play():
    global duration, media_files, playing, original_duration, original_media_files
    media = request.json
    duration = media['duration']
    original_duration = duration
    media_files = media['mediaFiles']
    original_media_files = media_files
    threading.Thread(name='playMedia', target=play_media).start()
    return 'Played'


@app.route('/stop')
def stop_media():
    global playing
    playing = 0
    with condition:
        condition.notify()
    return 'Stopped'


@app.route('/pause')
def pause_media():
    global duration
    duration = 1000000
    with condition:
        condition.notify()
    return 'Paused'


@app.route('/continue')
def continue_media():
    global duration
    duration = original_duration
    with condition:
        condition.notify()
    return 'Continued'


@app.route('/next')
def next_media():
    with condition:
        condition.notify()
    return 'Next'


@app.route('/previous')
def previous_media():
    global touched, media_files, current_index
    touched = 1
    media_files = shift(current_index, original_media_files, 0)
    current_index -= 2
    if current_index < 0:
        current_index = len(original_media_files) - 1
    with condition:
        condition.notify()
    return 'Prev'


@app.route('/test')
def test():
    global playing
    playing = 1
    threading.Thread(name='playMedia', target=play_media).start()
    return 'test'


if __name__ == '__main__':
    app.run()
