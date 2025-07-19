from flask import Flask, render_template, request, redirect
import boto3, os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)
S3_BUCKET = 'your-s3-bucket-name'  # Replace this
DATA_FILE = 'pets.json'

s3 = boto3.client('s3')

# Load pets from JSON file
def load_pets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save pets to JSON file
def save_pets(pets):
    with open(DATA_FILE, 'w') as f:
        json.dump(pets, f)

@app.route('/')
def index():
    pets = load_pets()
    return render_template('index.html', pets=pets)

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    age = request.form['age']
    breed = request.form['breed']
    photo = request.files['photo']

    filename = secure_filename(photo.filename)
    s3.upload_fileobj(photo, S3_BUCKET, filename)
    image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

    pet = {'name': name, 'age': age, 'breed': breed, 'image': image_url}
    pets = load_pets()
    pets.append(pet)
    save_pets(pets)

    return redirect('/')
