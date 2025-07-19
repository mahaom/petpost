
# PetPost 🐾

A simple pet listing website hosted on AWS EC2 that allows volunteers to:
- ✅ Upload adoptable pet details (name, age, breed) along with images
- ✅ View a list of submitted pets with images
- ✅ Store pet info in a JSON file and images in an S3 bucket
- ✅ Access the site publicly via EC2 with NGINX + Gunicorn + Flask

## 🚀 Technologies Used
- **Flask** – lightweight web framework
- **Amazon EC2** – hosting the web server
- **Amazon S3** – image storage
- **NGINX** – reverse proxy
- **Gunicorn** – WSGI server
- **HTML/CSS** – basic frontend design

## 📁 Project Structure
```
PetPost/
├── app.py              # Main Flask app
├── pets.json           # JSON file storing pet data
├── static/             # Static files (CSS, uploaded images)
├── templates/          # HTML templates
└── README.md           # Project overview (this file)
```

## 🛠 Deployment Steps Summary
1. Launch an EC2 instance and SSH into it
2. Set up Python virtual environment and install dependencies
3. Configure AWS credentials for `boto3`
4. Start the Flask app using Gunicorn
5. Configure NGINX to serve the app over port 80
6. Open port 80 in EC2 security group

## 📸 Screenshot / Demo
Include a screenshot or short video showing:
- Uploading pet details
- Pet list page displaying entries

## 📝 Instructor Notes
This project meets the following goals:
- Low-cost, browser-accessible app for a volunteer team
- No database used — flat file + S3 only
- Simple to maintain and deploy

---

Built with ❤️ by Rashid Shafiq
