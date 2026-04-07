# app.py

# app.py

from flask import Flask, request, jsonify, render_template
import base64
import numpy as np
import cv2
import pickle
import face_recognition
from firebase_config import ref
from datetime import datetime

app = Flask(__name__)

# ✅ CORRECT LOAD
with open("encodings.pkl", "rb") as f:
    data = pickle.load(f)
    known_encodings = [np.array(enc, dtype=np.float64) for enc in data["encodings"]]
    known_names = data["names"]

marked = set()  # duplicate attendance avoid


# 🔥 HTML page serve karega
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        data = request.json.get('image')

        if not data:
            return jsonify({"error": "No image received ❌"})

        # decode base64 image
        img_data = base64.b64decode(data.split(',')[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Image decode failed ❌"})

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        if len(encodings) == 0:
            return jsonify({"message": "No face detected 😐"})

        for encode in encodings:
            encode = np.array(encode, dtype=np.float64)  # 🔥 FIX

            matches = face_recognition.compare_faces(known_encodings, encode)
            face_distances = face_recognition.face_distance(known_encodings, encode)

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_names[best_match_index]

                if name not in marked:
                    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    ref.push({
                        "name": name,
                        "time": time
                    })

                    marked.add(name)

                    return jsonify({"message": f"{name} marked ✅"})
                else:
                    return jsonify({"message": f"{name} already marked ⚠️"})

        return jsonify({"message": "Unknown face ❌"})

    except Exception as e:
        return jsonify({"error": str(e)})


# 🔥 RUN SERVER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)