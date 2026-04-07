import firebase_admin
from firebase_admin import credentials, db

# Load service account key (updated path)
cred = credentials.Certificate(r"C:\Attendance_Project_Local\serviceAccountKey.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://attendance-system-f06ed-default-rtdb.firebaseio.com/'
})

# Reference to 'attendance' node
ref = db.reference('attendance')

# Test push (optional)
if __name__ == "__main__":
    from datetime import datetime
    ref.push({
        "name": "Test User",
        "time": datetime.now().strftime("%H:%M:%S")
    })
    print("Firebase connected ✅ Data inserted")