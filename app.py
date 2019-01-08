from flask import Flask
import pygame

app = Flask(__name__)
pygame.init()

@app.route('/')
def hello_world():
    pygame.mixer.music.load('50cent.mp3')
    pygame.mixer.music.play(0)
    return 'Played'


@app.route('/stop')
def stop():
    pygame.mixer.music.stop()
    return 'Stopped...'


if __name__ == '__main__':
    app.run()
