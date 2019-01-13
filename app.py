from flask import Flask, request
import threading
import subprocess
import time
import sys
app = Flask(__name__)

playing = 0
duration = 5
current_index = 0
touched = 0
original_duration = 5
media_files = []
original_media_files = []
condition = threading.Condition()
splash_image = '/home/pi/jp/SmartPlay/assets/logosmartplay.png'


def shift(key, array, next_event):
    # Used to shift array to start from the specific index(key)
    if next_event == 1:
        key = len(array) - key
    else:
        key = len(array) - key + 2
    return array[-key:]+array[:-key]


def init_screen():
    # Terminate processes if they are active
    subprocess.Popen('pkill -9 omxiv', shell=True)
    subprocess.Popen('pkill -9 omxplayer', shell=True)
    # Sets the background image in omxiv
    subprocess.Popen('omxiv -b ' + splash_image, shell=True)


def get_video_length(filename):
    # Get video duration of a file
    video_duration = subprocess.check_output(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
         filename]).decode(sys.stdout.encoding)
    # The output received is like b'11.06900\n'  -- Therefore the formatting is needed
    print(video_duration)
    return video_duration


def play_media():
    global playing, current_index, touched
    playing = 1
    while playing == 1:
        print('start from stracth')
        for file in media_files:
            # Start from start if it's a last media file
            if current_index > (len(media_files) - 1):
                current_index = 0
            # Exit the loop if playing is stopped (playing) or if next or prev functions are called (touched)
            if (playing == 0) or (touched == 1):
                touched = 0
                break
            file_type = ''
            # Start the omxiv for image
            if file['type'] == 'photo':
                global file_type
                file_type = 'photo'
                subprocess.Popen("omxiv --blank --duration 300 " + file['path'], shell=True)
            # Start the omxplayer for video
            else:
                global file_type
                file_type = 'video'
                subprocess.Popen("omxplayer -b " + file['path'], shell=True)
                video_length = get_video_length(file['path'])
            current_index += 1
            with condition:
                global file_type
                # Set the timeout between images
                if file_type == 'photo':
                    condition.wait(timeout=duration)
                # The timeout for a video is its duration
                else:
                    condition.wait(timeout=float(video_length))
                # Kill both processes after the timeout
                if file_type == 'photo':
                    subprocess.Popen('pkill -n omxiv', shell=True)
                else:
                    subprocess.Popen('pkill -9 omxplayer', shell=True)
                time.sleep(0.1) # Without this the process might get killed before it finishes
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
