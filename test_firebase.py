from firebase_config import ref
from datetime import datetime

# Test data push
ref.push({
    "name": "Test User",
    "time": datetime.now().strftime("%H:%M:%S")
})

print("Firebase connected ✅ Data inserted")