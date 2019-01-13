from flask import Flask


app = Flask(__name__)

video_duration = "b'17.681667\\n'"
print(video_duration)
video_duration = video_duration[2:]
print(video_duration)
video_duration = video_duration[:-3]
print(video_duration)


if __name__ == '__main__':
    app.run()


