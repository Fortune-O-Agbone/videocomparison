from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)

#Route to serve the index.html

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    #Get the uploaded files
    file1 = request.files.get('video1')
    file2 = request.files.get('video2')

    if not file1 or not file2:
        return jsonify({'error': 'Missing files(s)'}), 400

    #Save the files
    file1.save('video1.mp4')
    file2.save('video2.mp4')

    #Process the videos (add yoru comparison logic here)
    try:
        comparison_result = compare_videos('video1.mp4', 'video2.mp4')
        return jsonify({'result' : comparison_result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def compare_videos(video_path1, video_path2):
    #Add your video comparison logic here
    #For simplicity, let's just return a placeholder result
    cap1 = cv2.VideoCapture(video_path1)
    cap2 = cv2.VideoCapture(video_path2)

    if not cap1.isOpened() or not cap2.isOpened():
        raise Exception('Error opening video files')

    differences = []

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        #Resize frames to the same size
        frame1 = cv2.resize(frame1, (640, 480))
        frame2 = cv2.resize(frame2, (640, 480))

        #Calculate the absolute differences between the frames
        diff = cv2.absdiff(frame1, frame2)
        differences.append(np.mean(diff))

    cap1.release()
    cap2.release()

    #Return average difference as a simple comparison result
    return np.mean(differences)

if __name__ == '__main__':
    app.run(debug=True)