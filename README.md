# MedTrack – AWS Cloud Enabled Healthcare Management System

MedTrack is a web-based Healthcare Management System built using Flask, MongoDB, HTML, CSS, and Python.  
The system helps manage hospital operations such as patient appointments, diagnosis records, and administrative tasks.

This project supports role-based access for Admin, Doctor, Patient, and Receptionist.

--------------------------------------------------

FEATURES

Admin
- View all appointments
- Manage billing
- View lab reports

Doctor
- View patient appointments
- Add diagnosis reports

Patient
- Book appointments
- View diagnosis results

Receptionist
- Book appointments
- View appointments
- Generate billing

--------------------------------------------------

TECHNOLOGIES USED

Frontend
- HTML
- CSS
- Jinja2 Templates

Backend
- Python
- Flask

Database
- MongoDB (PyMongo)

Tools
- Git
- GitHub
- VS Code

--------------------------------------------------

PROJECT STRUCTURE

MedTrack
│
├── app.py
├── requirements.txt
├── config.py
│
├── static
│   └── style.css
│
├── templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── doctor_dashboard.html
│   ├── patient_dashboard.html
│   ├── receptionist_dashboard.html
│   ├── book_appointment.html
│   ├── view_appointment.html
│   ├── view_appointment_doctor.html
│   ├── add_diagnosis.html
│   ├── diagnosis_result.html
│   ├── billing.html
│   └── lab_report.html

--------------------------------------------------

INSTALLATION

1. Clone the repository

git clone https://github.com/thrishashetty1210-rgb/MedTrack-AWS-Cloud-Enabled-Healthcare-Management-System.git

cd MedTrack-AWS-Cloud-Enabled-Healthcare-Management-System

--------------------------------------------------

2. Install dependencies

pip install -r requirements.txt

--------------------------------------------------

3. Install MongoDB

Download MongoDB Community Server from:
https://www.mongodb.com/try/download/community

Start MongoDB server:

mongod

--------------------------------------------------

4. Run the application

python app.py

--------------------------------------------------

5. Open the application in browser

http://127.0.0.1:5000

--------------------------------------------------

DATABASE

MongoDB Database: medtrack

Collections:
- users
- appointments
- diagnosis

--------------------------------------------------

USER ROLES

When registering a user choose one of the following roles:

- admin
- doctor
- patient
- receptionist

--------------------------------------------------

FUTURE ENHANCEMENTS

- AWS cloud deployment
- Secure authentication
- Online payment integration
- Lab report upload
- Email notifications
- Patient history tracking

--------------------------------------------------


AUTHORS

This project was developed as a group project.

Team Members:

- Thrisha
- Navyashree
- Krithi
- Nidhi

GitHub:
https://github.com/thrishashetty1210-rgb
