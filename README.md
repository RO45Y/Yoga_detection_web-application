# 🧘 Yoga Detection and Correction App

This project is a computer vision-based Yoga Detection and Correction application built using **MediaPipe** for pose detection and **Django** for backend logic. It offers personalized yoga pose recommendations and provides real-time feedback to help users improve their posture.

---

## 🚀 Features

- ✅ User Signup with fitness profile (Age, Gender, Weight, Yoga Level, Injury History)
- 🎯 Personalized yoga pose recommendations
- 📸 Real-time pose detection using webcam
- 🔁 Pose comparison with reference image
- ✅ Visual feedback (Landmarks turn green on correct pose)
- 🔊 3-second audio alert when pose is matched
- 🧠 Feedback stored in database (e.g., "Done", "90% Correct")
- 📦 Admin panel for yoga pose management (if needed)

---

## 📽️ Demo Video

👉 [Click here to watch the demo video](https://youtu.be/rV_VCi2HrVg?si=ZA0epIeLAgGF7Y8E)

---

## 🛠️ Technologies Used

- Python
- Django
- MediaPipe Pose
- OpenCV
- HTML/CSS (Django templates)
- PostgreSQL

---

## ⚙️ Setup Instructions


Setup Instructions (Yoga Detection and Correction App)
------------------------------------------------------

🅐 Clone the Repository
-----------------------
git clone https://github.com/RO45Y/Yoga_detection_web-application.git
cd yoga-detection-app

🅑 Create and Activate a Virtual Environment
-------------------------------------------
# Create virtual environment
python -m venv env

# Activate it
# For Windows:
env\Scripts\activate

# For macOS/Linux:
source env/bin/activate

🅒 Install Required Packages
----------------------------
pip install -r requirements.txt

🅓 Apply Database Migrations
----------------------------
python manage.py makemigrations
python manage.py migrate

🅔 Run the Development Server
-----------------------------
python manage.py runserver

🅕 Access the App
-----------------
Open your browser and go to:
http://127.0.0.1:8000/


## 📜 License

This project is licensed under the MIT License. See the (LICENSE) file for more details.

   

